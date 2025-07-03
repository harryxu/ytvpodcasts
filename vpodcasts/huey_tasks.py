from huey import SqliteHuey
import subprocess
from vpodcasts.config import DB_FILE, PROJECT_ROOT

huey = SqliteHuey(filename=DB_FILE)


@huey.task()
def add_video(youtube_url):
    command = ["uv", "run", "manager.py", "add", youtube_url]
    try:
        subprocess.run(
            command, check=True, cwd=PROJECT_ROOT, capture_output=True, text=True
        )
    except subprocess.CalledProcessError as e:
        raise Exception(
            f"""
Failed to add video
command: {e.cmd}
returncode: {e.returncode}
stdout:\n{e.stdout}
stderr:\n{e.stderr}
        """
        ) from e
