import json
import os
import subprocess
import sys

import click

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
    command = create_ytdlp_command(["yt-dlp", "--dump-json"], youtube_url)
    try:
        click.echo(f"Fetching metadata for {youtube_url} with command {command}")
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        error_message = f"Error fetching video info: {e.stderr}"
        click.echo(error_message, err=True)
        raise Exception(error_message)
    except FileNotFoundError:
        click.echo("Error: 'yt-dlp' command not found.", err=True)
        click.echo("Please install yt-dlp: pip install yt-dlp", err=True)
        sys.exit(1)


def download_audio(youtube_url: str, video_id: str):
    """Download the best quality audio and save it to the episodes directory"""
    audio_format = "mp3"
    output_template = os.path.join(EPISODES_DIR, "%(id)s.%(ext)s")
    command = create_ytdlp_command(
        [
            "yt-dlp",
            "-x",
            "--audio-format",
            audio_format,
            "--audio-quality",
            "5",
            "-o",
            output_template,
        ],
        youtube_url,
    )
    try:
        click.echo(f"Starting audio download for {youtube_url} with command: {command}")
        subprocess.run(command, check=True, capture_output=True, text=True)
        click.echo("Download completed successfully.")
        filename = f"{video_id}.{audio_format}"
        return filename
    except subprocess.CalledProcessError as e:
        error_message = f"Error downloading audio: {e.stderr}"
        click.echo(error_message, err=True)
        raise Exception(error_message)
    except FileNotFoundError:
        click.echo("Error: 'yt-dlp' command not found.", err=True)
        click.echo("Please install yt-dlp: pip install yt-dlp", err=True)
        sys.exit(1)


def add_episode(youtube_url: str):
    """Handle the 'add' command: download, update database, regenerate RSS"""
    initialize_project()
    info = get_video_info(youtube_url)

    if db.episode_exists(info["id"]):
        error_message = (
            f"Video '{info['title']}' already exists in the podcast. Skipping."
        )
        click.echo(error_message)
        raise Exception(error_message)

    audio_path = download_audio(youtube_url, info["id"])

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
        "title": info["title"],
        "description": info.get("description", "No description available."),
        "webpage_url": info["webpage_url"],
        "upload_date": info["upload_date"],
        "duration": info.get("duration"),
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
