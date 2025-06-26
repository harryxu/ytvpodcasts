import os
import sys
import json
import subprocess
import click
from datetime import datetime
from feedgen.feed import FeedGenerator
from dotenv import load_dotenv

load_dotenv()

# --- Configuration ---
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
PODCAST_TITLE = os.getenv("PODCAST_TITLE", "My YouTube Podcast")
PODCAST_DESCRIPTION = os.getenv(
    "PODCAST_DESCRIPTION", "A podcast generated from YouTube videos."
)
PODCAST_LINK = os.getenv("PODCAST_LINK", "https://github.com/your_repo")

# --- File and Directory Paths ---
EPISODES_DIR = os.getenv("EPISODES_DIR", "episodes")
PODCAST_DATA_FILE = os.getenv("PODCAST_DATA_FILE", "podcast.json")
RSS_FILE = os.getenv("RSS_FILE", "feed.xml")


def initialize_project():
    """Check and create necessary directories and files"""
    if not os.path.exists(EPISODES_DIR):
        click.echo(f"Creating directory: {EPISODES_DIR}")
        os.makedirs(EPISODES_DIR)

    if not os.path.exists(PODCAST_DATA_FILE):
        click.echo(f"Creating empty database: {PODCAST_DATA_FILE}")
        with open(PODCAST_DATA_FILE, "w") as f:
            json.dump({"episodes": []}, f, indent=4)

    click.echo("Initialization complete.")


def get_video_info(youtube_url):
    """Get video metadata using yt-dlp"""
    click.echo(f"Fetching metadata for {youtube_url}...")
    command = ["yt-dlp", "--dump-json", youtube_url]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        click.echo(f"Error fetching video info: {e.stderr}", err=True)
        return None
    except FileNotFoundError:
        click.echo("Error: 'yt-dlp' command not found.", err=True)
        click.echo("Please install yt-dlp: pip install yt-dlp", err=True)
        sys.exit(1)


def download_audio(youtube_url):
    """Download the best quality audio and save it to the episodes directory"""
    click.echo(f"Starting audio download for {youtube_url}...")
    output_template = os.path.join(EPISODES_DIR, "%(id)s.%(ext)s")
    command = [
        "yt-dlp",
        "-f",
        "bestaudio[ext=m4a]",
        "-o",
        output_template,
        youtube_url,
    ]
    try:
        subprocess.run(command, check=True)
        click.echo("Download completed successfully.")
        info = get_video_info(youtube_url)
        if info:
            filename = f"{info['id']}.m4a"
            return os.path.join(EPISODES_DIR, filename)
    except subprocess.CalledProcessError as e:
        click.echo(f"Error downloading audio: {e}", err=True)
        return None
    except FileNotFoundError:
        click.echo("Error: 'yt-dlp' command not found.", err=True)
        click.echo("Please install yt-dlp: pip install yt-dlp", err=True)
        sys.exit(1)
    return None


def generate_rss():
    """Generate feed.xml from podcast.json"""
    click.echo("Generating RSS feed...")
    with open(PODCAST_DATA_FILE, "r") as f:
        data = json.load(f)

    fg = FeedGenerator()
    fg.title(PODCAST_TITLE)
    fg.link(href=BASE_URL, rel="alternate")
    fg.description(PODCAST_DESCRIPTION)
    fg.language("en")

    for episode_info in sorted(
        data["episodes"], key=lambda x: x["upload_date"], reverse=True
    ):
        fe = fg.add_entry()
        fe.id(episode_info["webpage_url"])
        fe.title(episode_info["title"])
        fe.description(episode_info["description"])
        pub_date = datetime.strptime(episode_info["upload_date"], "%Y%m%d").strftime(
            "%a, %d %b %Y %H:%M:%S %z"
        )
        fe.published(pub_date + " +0000")
        audio_url = f"{BASE_URL}/{episode_info['audio_file']}"
        file_size = str(os.path.getsize(episode_info["audio_file"]))
        fe.enclosure(url=audio_url, length=file_size, type="audio/x-m4a")

    fg.rss_file(RSS_FILE, pretty=True)
    click.echo(f"RSS feed saved to {RSS_FILE}")


def add_episode(youtube_url):
    """Handle the 'add' command: download, update database, regenerate RSS"""
    initialize_project()
    info = get_video_info(youtube_url)
    if not info:
        return

    with open(PODCAST_DATA_FILE, "r") as f:
        podcast_data = json.load(f)

    if any(ep["id"] == info["id"] for ep in podcast_data["episodes"]):
        click.echo(f"Video '{info['title']}' already exists in the podcast. Skipping.")
        return

    audio_path = download_audio(youtube_url)
    if not audio_path:
        return

    episode_data = {
        "id": info["id"],
        "title": info["title"],
        "description": info.get("description", "No description available."),
        "webpage_url": info["webpage_url"],
        "upload_date": info["upload_date"],
        "duration": info.get("duration"),
        "thumbnail": info.get("thumbnail"),
        "audio_file": audio_path,
    }

    podcast_data["episodes"].append(episode_data)
    with open(PODCAST_DATA_FILE, "w") as f:
        json.dump(podcast_data, f, indent=4)
    click.echo(f"Added '{info['title']}' to {PODCAST_DATA_FILE}")
    generate_rss()


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
def add(url):
    """Add a new YouTube video to the podcast."""
    add_episode(url)


@cli.command()
def generate():
    """Force regenerate the RSS feed from existing data."""
    generate_rss()


@cli.command()
def serve():
    """Instructions to run the web server."""
    click.echo("To run the web server, please use the following command:")
    click.echo("\n    python3 webapp.py\n")


if __name__ == "__main__":
    cli()