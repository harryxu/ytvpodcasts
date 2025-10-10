from huey import SqliteHuey

from vpodcasts.config import DB_FILE
from vpodcasts.ypd import add_episode

huey = SqliteHuey(filename=DB_FILE)


@huey.task()
def add_video(youtube_url: str):
    add_episode(youtube_url)
