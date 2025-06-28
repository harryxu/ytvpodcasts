import os
from dotenv import load_dotenv

load_dotenv()

# --- Database Configuration ---
DB_FILE = os.getenv("DB_FILE", "data/vpodcasts.db")

# --- Podcast Configuration ---
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
PODCAST_TITLE = os.getenv("PODCAST_TITLE", "My YouTube Podcast")
PODCAST_DESCRIPTION = os.getenv(
    "PODCAST_DESCRIPTION", "A podcast generated from YouTube videos."
)
PODCAST_LINK = os.getenv("PODCAST_LINK", "https://github.com/your_repo")

# --- File and Directory Paths ---
EPISODES_DIR = os.getenv("EPISODES_DIR", "data/episodes")
