from loguru import logger
from sqlmodel import Session, select
from taskiq_nats import PushBasedJetStreamBroker

import vpodcasts.database as db
from vpodcasts.config import NATS_URL
from vpodcasts.models import DownloadTask
from vpodcasts.ypd import add_episode

broker = PushBasedJetStreamBroker(
    servers=[NATS_URL],
    queue="vpodcasts_download_queue",
)


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
