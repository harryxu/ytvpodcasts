import asyncio
import json
from datetime import datetime, timezone
from typing import Any

from huey import SqliteHuey
from huey.api import Task
from huey.signals import SIGNAL_COMPLETE, SIGNAL_ERROR, SIGNAL_EXECUTING
from loguru import logger
from nats.aio.client import Client as NATS
from sqlmodel import Session, select

import vpodcasts.database as db
from vpodcasts.config import DB_FILE, NATS_URL
from vpodcasts.models import DownloadTask
from vpodcasts.ypd import add_episode

huey = SqliteHuey(filename=DB_FILE)

nc = NATS()


async def get_nats_connection():
    if nc.is_connected:
        return nc
    await nc.connect(NATS_URL)
    return nc


@huey.task()
def add_video(youtube_url: str):
    def progress_cb(progress: dict):
        print(progress)

    return add_episode(youtube_url, progress_cb)


def create_video_download_task(url: str):
    res = add_video(url)
    with Session(db.engine) as session:
        task = DownloadTask(
            title=f"Download video: {url}", queue_task_id=res.id, status="pending"
        )
        session.add(task)
        session.commit()
    return res


@huey.signal(SIGNAL_EXECUTING)
def _handle_download_executing(signal, task: Task):
    with Session(db.engine) as session:
        download_task = session.exec(
            select(DownloadTask).where(DownloadTask.queue_task_id == task.id)
        ).first()
        if download_task:
            download_task.status = "processing"
            session.add(download_task)
            session.commit()
            logger.info(f"Download task {task.id} started")
            asyncio.run(
                publish_notification(
                    {
                        "type": "task",
                        "task": download_task.model_dump_json(),
                        "status": "processing",
                    }
                )
            )
            logger.info(f"Download task {task.id} started notification")


@huey.signal(SIGNAL_COMPLETE)
def _handle_download_complete(signal, task: Task):
    result = huey.result(task.id, blocking=True)
    with Session(db.engine) as session:
        download_task: DownloadTask | None = session.exec(
            select(DownloadTask).where(DownloadTask.queue_task_id == task.id)
        ).first()
        if download_task:
            download_task.status = "success"
            if result and isinstance(result, dict) and "id" in result:
                download_task.episode_id = result["id"]
            download_task.completed_at = datetime.now(timezone.utc)
            session.add(download_task)
            session.commit()


@huey.signal(SIGNAL_ERROR)
def _handle_download_error(signal, task: Task, exc=None):
    with Session(db.engine) as session:
        download_task = session.exec(
            select(DownloadTask).where(DownloadTask.queue_task_id == task.id)
        ).first()
        if download_task:
            download_task.status = "failed"
            download_task.description = str(exc)
            session.add(download_task)
            session.commit()
            logger.info(f"Download task {task.id} failed")
            asyncio.run(
                publish_notification(
                    {
                        "type": "task",
                        "task": download_task.model_dump_json(),
                        "status": "failed",
                    }
                )
            )
            logger.info(f"Download task {task.id} failed notification")


async def publish_notification(payload: Any, drain_after_publish: bool = False):
    nc = await get_nats_connection()
    await nc.publish("notification", json.dumps(payload).encode())
    await nc.flush()
    await nc.close()
    if drain_after_publish:
        await nc.drain()
