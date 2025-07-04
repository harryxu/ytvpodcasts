from flask import Flask, send_from_directory, Response, request, jsonify
from datetime import datetime
from vpodcasts.database import get_all_episodes, create_db_and_tables
from feedgen.feed import FeedGenerator
from vpodcasts.config import (
    EPISODES_DIR,
    BASE_URL,
    PODCAST_TITLE,
    PODCAST_DESCRIPTION,
)
from vpodcasts.huey_tasks import add_video

app = Flask(__name__)


def generate_rss_feed():
    episodes = get_all_episodes()

    fg = FeedGenerator()
    fg.load_extension("podcast")
    fg.title(PODCAST_TITLE)
    fg.link(href=BASE_URL, rel="alternate")
    fg.description(PODCAST_DESCRIPTION)
    fg.language("en")

    for episode_info in episodes:
        fe = fg.add_entry()
        fe.id(episode_info.webpage_url)
        fe.title(episode_info.title)
        description = f"{episode_info.description}<br/><br/>Webpage: {episode_info.webpage_url}<br/>Upload Date: {episode_info.upload_date}"
        fe.description(description)
        pub_date = episode_info.create_date.strftime("%a, %d %b %Y %H:%M:%S")
        fe.published(pub_date + " GMT")
        audio_url = f"{BASE_URL}/episodes/{episode_info.audio_file}"
        fe.enclosure(
            url=audio_url,
            length=str(episode_info.audio_file_size),
            type=episode_info.audio_file_type,
        )
        if episode_info.duration:
            fe.podcast.itunes_duration(episode_info.duration)

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


@app.route("/api/add", methods=["POST"])
def add_episode():
    url = request.json.get("url")
    if not url:
        return jsonify({"error": "Missing url"}), 400
    add_video(url)
    return jsonify({"data": True}), 200


@app.route("/api/episodes", methods=["GET"])
def get_episodes():
    episodes = get_all_episodes()
    return (
        jsonify({"data": [episode.model_dump(mode="json") for episode in episodes]}),
        200,
    )


def main():
    """Main function, starts the server"""
    create_db_and_tables()  # Ensure database and tables are created
    port = 8000
    print(f"Starting Flask server at http://localhost:{port}")
    print(f"Serving RSS feed: {BASE_URL}/")
    print(f"Serving episodes from: ./{EPISODES_DIR}/")
    print("Press Ctrl+C to stop the server.")
    app.run(host="0.0.0.0", port=port, debug=True, use_reloader=True)


if __name__ == "__main__":
    main()
