from collections.abc import Coroutine
from datetime import datetime, timezone
from types import CoroutineType
from typing import Any, Union

from loguru import logger
from sqlmodel import Session, select
from taskiq import TaskiqMessage, TaskiqMiddleware, TaskiqResult
from taskiq_nats import PullBasedJetStreamBroker

import vpodcasts.database as db
from vpodcasts.config import NATS_URL
from vpodcasts.models import DownloadTask
from vpodcasts.ypd import add_episode


class DownloadTaskMiddleware(TaskiqMiddleware):
    def pre_execute(
        self,
        message: "TaskiqMessage",
    ) -> Union[
        "TaskiqMessage",
        "Coroutine[Any, Any, TaskiqMessage]",
        "CoroutineType[Any, Any, TaskiqMessage]",
    ]:
        """
        This hook is called before executing task.

        This is a worker-side hook, which means it
        executes in the worker process.

        :param message: incoming parsed taskiq message.
        :return: modified message.
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
                logger.info(f"Download task {message.task_id} started")

        return message

    def post_execute(
        self,
        message: "TaskiqMessage",
        result: "TaskiqResult[Any]",
    ) -> Union[None, Coroutine[Any, Any, None], "CoroutineType[Any, Any, None]"]:
        """
        This hook executes after task is complete.

        This is a worker-side hook. It's called
        in worker process.

        :param message: incoming message.
        :param result: result of execution for current task.
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

    def on_error(
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


broker = PullBasedJetStreamBroker(
    servers=[NATS_URL],
    queue="vpodcasts_download_queue",
).with_middlewares(DownloadTaskMiddleware())


@broker.task
async def add_video_task(youtube_url: str):
    def progress_cb(progress: dict):
        print(progress)

    return add_episode(youtube_url, progress_cb)


async def create_video_download_task(url: str):
    res = await add_video_task.kiq(url)
    logger.debug(f"Task created: {res.task_id}")
    with Session(db.engine) as session:
        task = DownloadTask(
            title=f"Download video: {url}", queue_task_id=res.task_id, status="pending"
        )
        session.add(task)
        session.commit()
    return res
