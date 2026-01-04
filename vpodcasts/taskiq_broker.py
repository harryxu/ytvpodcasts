import asyncio
import contextlib
import json
import time
from datetime import datetime, timezone
from typing import Any, Optional

from nats.aio.client import Client as NATS
from sqlmodel import Session, select
from taskiq import TaskiqMessage, TaskiqMiddleware, TaskiqResult
from taskiq_nats import PullBasedJetStreamBroker

import vpodcasts.database as db
from vpodcasts import logger
from vpodcasts.config import NATS_URL
from vpodcasts.models import DownloadTask
from vpodcasts.ypd import add_episode


class NatsPublisher:
    def __init__(self, servers: list[str]):
        self.servers = servers
        self.nc = NATS()
        self._lock = asyncio.Lock()

    async def _ensure_connected(self):
        async with self._lock:
            if self.nc.is_connected:
                return
            if self.nc.is_closed:
                self.nc = NATS()

        async def on_error(e):
            logger.error("NATS error:", e)

        async def on_disconnect():
            logger.warning("NATS disconnected")

        async def on_reconnect():
            logger.info("NATS reconnected")

        async def on_close():
            logger.info("NATS closed")

        await self.nc.connect(
            servers=[NATS_URL],
            max_reconnect_attempts=-1,
            reconnect_time_wait=5,
            error_cb=on_error,
            disconnected_cb=on_disconnect,
            reconnected_cb=on_reconnect,
            closed_cb=on_close,
        )

    async def publish(self, payload: dict):
        try:
            await self._ensure_connected()
            await self.nc.publish(
                "notification",
                json.dumps(payload).encode(),
            )
            await self.nc.flush(timeout=1)
        except Exception as e:
            logger.error("Failed to publish message to NATS:", e)

    async def shutdown(self):
        if self.nc.is_connected:
            try:
                await self.nc.drain()
            finally:
                await self.nc.close()


class ProgressQueuePublisher:
    def __init__(self, publisher: NatsPublisher):
        self.publisher = publisher
        self.queue: asyncio.Queue = asyncio.Queue()
        self._task: Optional[asyncio.Task] = None
        self._stopping = False

    async def start(self):
        if self._task is None:
            self._task = asyncio.create_task(self._run())

    async def _run(self):
        while True:
            payload = await self.queue.get()
            try:
                await self.publisher.publish(payload)
            finally:
                self.queue.task_done()

    def enqueue(self, payload: dict):
        if self._stopping:
            return

        if self._task is None:
            raise RuntimeError("Publisher not started")

        self.queue.put_nowait(payload)

    async def shutdown(self, timeout: float = 5.0):
        if self._task is None:
            return

        self._stopping = True

        try:
            await asyncio.wait_for(self.queue.join(), timeout)
        except asyncio.TimeoutError:
            pass

        self._task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await self._task
            self._stopping = False
            self._task = None


nats_publisher = NatsPublisher([NATS_URL])
progress_publisher = ProgressQueuePublisher(nats_publisher)


class DownloadTaskMiddleware(TaskiqMiddleware):
    def __init__(
        self, nats_publisher: NatsPublisher, progress_publisher: ProgressQueuePublisher
    ):
        self.nats_publisher = nats_publisher
        self.progress_publisher = progress_publisher

    async def startup(self):
        await self.progress_publisher.start()

    async def shutdown(self):
        await self.nats_publisher.shutdown()
        await self.progress_publisher.shutdown()

    async def pre_execute(
        self,
        message: "TaskiqMessage",
    ) -> "TaskiqMessage":
        """
        This hook is called before executing task. This is a worker-side hook.
        """
        with Session(db.engine) as session:
            download_task = session.exec(
                select(DownloadTask).where(
                    DownloadTask.queue_task_id == message.task_id
                )
            ).first()
            if download_task:
                download_task.status = "processing"
                session.add(download_task)
                session.commit()
                session.refresh(download_task)
                await self.nats_publisher.publish(
                    {
                        "type": "task",
                        "task": download_task.model_dump(
                            mode="json", exclude_unset=False
                        ),
                        "status": "processing",
                    }
                )
                logger.info(f"Download task {message.task_id} started")

        return message

    async def post_execute(
        self,
        message: "TaskiqMessage",
        result: "TaskiqResult[Any]",
    ):
        """
        This hook executes after task is complete. This is a worker-side hook.
        """
        with Session(db.engine) as session:
            download_task: DownloadTask | None = session.exec(
                select(DownloadTask).where(
                    DownloadTask.queue_task_id == message.task_id
                )
            ).first()
            if download_task and download_task.status != "failed":
                download_task.status = "success"
                if result and isinstance(result, dict) and "id" in result:
                    download_task.episode_id = result["id"]
                download_task.completed_at = datetime.now(timezone.utc)
                session.add(download_task)
                session.commit()
                session.refresh(download_task)
                await self.nats_publisher.publish(
                    {
                        "type": "task",
                        "task": download_task.model_dump(
                            mode="json", exclude_unset=False
                        ),
                        "status": "success",
                    }
                )

    async def on_error(
        self,
        message: "TaskiqMessage",
        result: "TaskiqResult[Any]",
        exception: BaseException,
    ):
        logger.error(f"Task Error occurred: [{message.task_id}] {exception}")
        with Session(db.engine) as session:
            download_task = session.exec(
                select(DownloadTask).where(
                    DownloadTask.queue_task_id == message.task_id
                )
            ).first()
            if download_task:
                download_task.status = "failed"
                download_task.description = str(exception)
                session.add(download_task)
                session.commit()
                session.refresh(download_task)
                await self.nats_publisher.publish(
                    {
                        "type": "task",
                        "task": download_task.model_dump(
                            mode="json", exclude_unset=False
                        ),
                        "status": "failed",
                    }
                )


broker = PullBasedJetStreamBroker(
    servers=[NATS_URL],
    queue="vpodcasts_download_queue",
).with_middlewares(DownloadTaskMiddleware(nats_publisher, progress_publisher))


def download_video_handler(youtube_url: str, download_task: DownloadTask):
    last_publish_time = 0

    def progress_cb(progress: dict):
        nonlocal last_publish_time
        now = time.time()
        if now - last_publish_time <= 0.5:
            return
        last_publish_time = now
        remove_keys = ["info_dict", "tmpfilename", "filename"]
        for k in remove_keys:
            progress.pop(k, None)
        progress_publisher.enqueue(
            {
                "type": "task",
                "progress": progress,
                "task": download_task.model_dump(mode="json", exclude_unset=False),
                "status": "progress",
            }
        )

    return add_episode(youtube_url, progress_cb)


@broker.task
async def add_video_task(youtube_url: str, download_task_id: int):
    await progress_publisher.start()
    loop = asyncio.get_running_loop()

    with Session(db.engine) as session:
        download_task = session.get(DownloadTask, download_task_id)
        if download_task is not None:
            await loop.run_in_executor(
                None, download_video_handler, youtube_url, download_task
            )


async def create_video_download_task(url: str):
    with Session(db.engine) as session:
        task = DownloadTask(title=f"Download video: {url}", status="pending")
        session.add(task)
        session.commit()
        session.refresh(task)
        res = await add_video_task.kiq(url, task.id)
        task.queue_task_id = res.task_id
        session.add(task)
        session.commit()
        logger.debug(f"Task created: {res.task_id}")
    return res
