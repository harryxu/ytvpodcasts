import asyncio
import json
from collections.abc import Coroutine
from datetime import datetime, timezone
from types import CoroutineType
from typing import Any, Union

from nats.aio.client import Client as NATS
from sqlmodel import Session, select
from taskiq import TaskiqMessage, TaskiqMiddleware, TaskiqResult
from taskiq_nats import PullBasedJetStreamBroker

import vpodcasts.database as db
from vpodcasts import logger
from vpodcasts.config import NATS_URL
from vpodcasts.models import DownloadTask
from vpodcasts.ypd import add_episode

nc = NATS()


class DownloadTaskMiddleware(TaskiqMiddleware):
    async def pre_execute(
        self,
        message: "TaskiqMessage",
    ) -> Union[
        "TaskiqMessage",
        "Coroutine[Any, Any, TaskiqMessage]",
        "CoroutineType[Any, Any, TaskiqMessage]",
    ]:
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
                await publish_notification(
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
    ) -> Union[None, Coroutine[Any, Any, None], "CoroutineType[Any, Any, None]"]:
        """
        This hook executes after task is complete. This is a worker-side hook.
        """
        with Session(db.engine) as session:
            download_task: DownloadTask | None = session.exec(
                select(DownloadTask).where(
                    DownloadTask.queue_task_id == message.task_id
                )
            ).first()
            if download_task:
                download_task.status = "success"
                if result and isinstance(result, dict) and "id" in result:
                    download_task.episode_id = result["id"]
                download_task.completed_at = datetime.now(timezone.utc)
                session.add(download_task)
                session.commit()
                await publish_notification(
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
    ) -> Union[None, Coroutine[Any, Any, None], "CoroutineType[Any, Any, None]"]:
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
                await publish_notification(
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
).with_middlewares(DownloadTaskMiddleware())


@broker.task
async def add_video_task(youtube_url: str, download_task: DownloadTask):
    async def publish_progress(progress: dict):
        await publish_notification(
            {
                "type": "task",
                "progress": progress,
                "status": "progress",
            }
        )

    def progress_cb(progress: dict):
        remove_keys = ["info_dict", "tmpfilename", "filename"]
        for k in remove_keys:
            progress.pop(k, None)
            asyncio.create_task(publish_progress(progress))

    return add_episode(youtube_url, progress_cb)


async def create_video_download_task(url: str):
    with Session(db.engine) as session:
        task = DownloadTask(title=f"Download video: {url}", status="pending")
        session.add(task)
        session.commit()
        session.refresh(task)
        res = await add_video_task.kiq(url, task)
        task.queue_task_id = res.task_id
        session.add(task)
        session.commit()
        logger.debug(f"Task created: {res.task_id}")
    return res


async def get_nats_connection():
    if nc.is_connected:
        return nc
    await nc.connect(NATS_URL)
    return nc


async def publish_notification(payload: Any, drain_after_publish: bool = False):
    nc = await get_nats_connection()
    await nc.publish("notification", json.dumps(payload).encode())
    await nc.flush()
    await nc.close()
    if drain_after_publish:
        await nc.drain()
