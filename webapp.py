import os
from flask import Flask, send_from_directory, Response
from dotenv import load_dotenv
from datetime import datetime
from database import get_all_episodes, create_db_and_tables
from feedgen.feed import FeedGenerator

load_dotenv()

# --- Configuration ---
# These values should be consistent with those in ypd.py
EPISODES_DIR = os.getenv("EPISODES_DIR", "episodes")
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
PODCAST_TITLE = os.getenv("PODCAST_TITLE", "My YouTube Podcast")
PODCAST_DESCRIPTION = os.getenv(
    "PODCAST_DESCRIPTION", "A podcast generated from YouTube videos."
)
PODCAST_LINK = os.getenv("PODCAST_LINK", "https://github.com/your_repo")

app = Flask(__name__)

def generate_rss_feed():
    episodes = get_all_episodes()

    fg = FeedGenerator()
    fg.title(PODCAST_TITLE)
    fg.link(href=BASE_URL, rel="alternate")
    fg.description(PODCAST_DESCRIPTION)
    fg.language("en")

    for episode_info in episodes:
        fe = fg.add_entry()
        fe.id(episode_info.webpage_url)
        fe.title(episode_info.title)
        fe.description(episode_info.description)
        pub_date = datetime.strptime(episode_info.upload_date, "%Y%m%d").strftime(
            "%a, %d %b %Y %H:%M:%S %z"
        )
        fe.published(pub_date + " +0000")
        audio_url = f"{BASE_URL}/episodes/{episode_info.audio_file}"
        # Ensure audio_file exists before trying to get its size
        audio_file_path = os.path.join(EPISODES_DIR, episode_info.audio_file)
        file_size = str(os.path.getsize(audio_file_path)) if os.path.exists(audio_file_path) else "0"
        fe.enclosure(url=audio_url, length=file_size, type="audio/mpeg")

    return fg.rss_str(pretty=True)

@app.route('/')
def index():
    # Provide the RSS feed dynamically
    rss_feed = generate_rss_feed()
    return Response(rss_feed, mimetype='application/xml')

@app.route('/episodes/<path:filename>')
def download_episode(filename):
    # Provide the audio files
    return send_from_directory(EPISODES_DIR, filename)



def main():
    """Main function, starts the server"""
    create_db_and_tables() # Ensure database and tables are created
    port = 8000
    print(f"Starting Flask server at http://localhost:{port}")
    print(f"Serving RSS feed: {BASE_URL}/")
    print(f"Serving episodes from: ./{EPISODES_DIR}/")
    print("Press Ctrl+C to stop the server.")
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    main()
