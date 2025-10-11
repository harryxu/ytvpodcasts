from huey import SqliteHuey
from huey.api import Task
from huey.signals import SIGNAL_COMPLETE, SIGNAL_ERROR

from vpodcasts.config import DB_FILE
from vpodcasts.models import DownloadTask
from vpodcasts.ypd import add_episode
from sqlmodel import Session, select
import vpodcasts.database as db


huey = SqliteHuey(filename=DB_FILE)


@huey.signal(SIGNAL_COMPLETE)
def _handle_download_complete(signal, task: Task, exc=None):
    print(f"Download task {task.id} completed")


@huey.signal(SIGNAL_ERROR)
def _handle_download_error(signal, task: Task, exc=None):
    print(f"Download task {task.id} failed. {exc}")
    with Session(db.engine) as session:
        download_task = session.exec(
            select(DownloadTask).where(DownloadTask.queue_task_id == task.id)
        ).first()
        download_task.status = "failed"
        session.add(download_task)
        session.commit()


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
