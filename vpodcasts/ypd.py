from typing import Callable
import os

from typing import Any

import click
from yt_dlp import YoutubeDL

import vpodcasts.database as db
from vpodcasts.config import EPISODES_DIR, YOUTUBE_COOKIES_FILE


def initialize_project():
    """Check and create necessary directories and files"""
    if not os.path.exists(EPISODES_DIR):
        click.echo(f"Creating directory: {EPISODES_DIR}")
        os.makedirs(EPISODES_DIR)

    # db.create_db_and_tables()
    click.echo("Initialization complete.")


def get_video_info(youtube_url: str):
    """Get video metadata using yt-dlp"""

    ydl_opts: Any = {
        "forcejson": True,
        "noprogress": True,
        "quiet": True,
        "simulate": True,
    }

    try:
        click.echo(
            f"Fetching metadata for {youtube_url} using yt-dlp library with options {ydl_opts}"
        )

        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtube_url, download=False)
            return ydl.sanitize_info(info_dict)

    except Exception as e:
        error_message = f"Error fetching video info: {e}"
        click.echo(error_message, err=True)
        raise Exception(error_message)


def download_audio(
    youtube_url: str, video_id: str, progress_cb: Callable[[dict], None] | None = None
):
    """Download the best quality audio and save it to the episodes directory"""
    audio_format = "mp3"
    output_template = os.path.join(EPISODES_DIR, "%(id)s.%(ext)s")

    ydl_opts: Any = {
        "final_ext": "mp3",
        "format": "bestaudio/best",
        "outtmpl": {"default": output_template},
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "nopostoverwrites": False,
                "preferredcodec": "mp3",
                "preferredquality": "5",
            }
        ],
    }
    if progress_cb:
        ydl_opts["progress_hooks"] = [progress_cb]

    try:
        click.echo(f"Starting audio download for {youtube_url}")
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])
        click.echo("Download completed successfully.")
        filename = f"{video_id}.{audio_format}"
        return filename
    except Exception as e:
        error_message = f"Error downloading audio: {e}"
        click.echo(error_message, err=True)
        raise Exception(error_message)


def add_episode(youtube_url: str, progress_cb: Callable[[dict], None] | None = None):
    """Handle the 'add' command: download, update database, regenerate RSS"""
    initialize_project()
    info = get_video_info(youtube_url)
    if not info:
        raise Exception("Failed to fetch video info.")

    if db.episode_exists(info["id"]):
        error_message = (
            f"Video '{info['title']}' already exists in the podcast. Skipping."
        )
        click.echo(error_message)
        raise Exception(error_message)

    audio_path = download_audio(youtube_url, info["id"], progress_cb)

    audio_file_path = os.path.join(EPISODES_DIR, audio_path)
    audio_file_size = os.path.getsize(audio_file_path)
    # Determine audio file type from file extension
    _, file_extension = os.path.splitext(audio_path)
    if file_extension == ".m4a":
        audio_file_type = "audio/mp4"
    elif file_extension == ".mp3":
        audio_file_type = "audio/mpeg"
    else:
        # Default or could be expanded
        audio_file_type = "audio/mpeg"

    episode_data = {
        "id": info["id"],
        "title": info.get("title"),
        "description": info.get("description", "No description available."),
        "webpage_url": info.get("webpage_url"),
        "upload_date": info.get("upload_date"),
        "duration": int(info.get("duration") or 0),
        "thumbnail": info.get("thumbnail"),
        "audio_file": audio_path,
        "audio_file_size": audio_file_size,
        "audio_file_type": audio_file_type,
    }

    db.add_episode(episode_data)
    click.echo(f"Added '{info['title']}' to the database.")
    return episode_data


def create_ytdlp_command(command: list[str], youtube_url: str):
    if YOUTUBE_COOKIES_FILE:
        command += ["--cookies", YOUTUBE_COOKIES_FILE]
    command.append(youtube_url)
    return command


@click.group()
def cli():
    """A command-line tool to generate a podcast RSS feed from YouTube videos."""
    pass


@cli.command()
def init():
    """Initialize the project structure."""
    initialize_project()


@cli.command()
@click.argument("url")
def add(url: str):
    """Add a new YouTube video to the podcast."""
    add_episode(url)


if __name__ == "__main__":
    cli()
