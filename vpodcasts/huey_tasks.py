from huey import SqliteHuey

from vpodcasts.config import DB_FILE
from vpodcasts.models import DownloadTask
from vpodcasts.ypd import add_episode
from sqlmodel import Session
import vpodcasts.database as db


huey = SqliteHuey(filename=DB_FILE)


@huey.task()
def add_video(youtube_url: str):
    add_episode(youtube_url)


def create_video_download_task(url: str):
    res = add_video(url)
    with Session(db.engine) as session:
        task = DownloadTask(
            title=f"Download video: {url}", queue_task_id=res.id, status="pending"
        )
        session.add(task)
        session.commit()
    return res
