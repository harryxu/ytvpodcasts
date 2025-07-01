from huey import SqliteHuey
import subprocess
from vpodcasts.config import DB_FILE, PROJECT_ROOT

huey = SqliteHuey(filename=DB_FILE)

@huey.task()
def add_video(youtube_url):
    command = ["uv", "run", "manager.py", "add", youtube_url]
    subprocess.run(command, check=True, cwd=PROJECT_ROOT)
