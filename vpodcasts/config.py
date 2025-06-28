import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

# Determine the project root directory
# This assumes config.py is inside a package (e.g., vpodcasts/)
# and the project root is one level up from that package.
PROJECT_ROOT = Path(__file__).parent.parent.resolve()

# --- Database Configuration ---
DB_FILE = os.getenv("DB_FILE", str(PROJECT_ROOT / "data" / "vpodcasts.db"))

# --- Podcast Configuration ---
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
PODCAST_TITLE = os.getenv("PODCAST_TITLE", "My YouTube Podcast")
PODCAST_DESCRIPTION = os.getenv(
    "PODCAST_DESCRIPTION", "A podcast generated from YouTube videos."
)
PODCAST_LINK = os.getenv("PODCAST_LINK", "https://github.com/your_repo")

# --- File and Directory Paths ---
EPISODES_DIR = os.getenv("EPISODES_DIR", str(PROJECT_ROOT / "data" / "episodes"))
