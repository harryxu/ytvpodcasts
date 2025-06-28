from flask import Flask, send_from_directory, Response
from datetime import datetime
from database import get_all_episodes, create_db_and_tables
from feedgen.feed import FeedGenerator
from config import (
    EPISODES_DIR,
    BASE_URL,
    PODCAST_TITLE,
    PODCAST_DESCRIPTION,
)

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
        fe.enclosure(
            url=audio_url,
            length=str(episode_info.audio_file_size),
            type=episode_info.audio_file_type,
        )

    return fg.rss_str(pretty=True)


@app.route("/")
def index():
    # Provide the RSS feed dynamically
    rss_feed = generate_rss_feed()
    return Response(rss_feed, mimetype="application/xml")


@app.route("/episodes/<path:filename>")
def download_episode(filename):
    # Provide the audio files
    return send_from_directory(EPISODES_DIR, filename)


def main():
    """Main function, starts the server"""
    create_db_and_tables()  # Ensure database and tables are created
    port = 8000
    print(f"Starting Flask server at http://localhost:{port}")
    print(f"Serving RSS feed: {BASE_URL}/")
    print(f"Serving episodes from: ./{EPISODES_DIR}/")
    print("Press Ctrl+C to stop the server.")
    app.run(host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
