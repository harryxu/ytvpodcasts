import math
import flask
from feedgen.feed import FeedGenerator
from flask import Flask, Response, jsonify, request, send_from_directory

from vpodcasts.config import BASE_URL, EPISODES_DIR, PODCAST_DESCRIPTION, PODCAST_TITLE
from vpodcasts.database import (
    create_db_and_tables,
    get_all_episodes,
    get_episodes as db_get_episodes,
)
from vpodcasts.huey_tasks import add_video

app = Flask(__name__)


@app.route("/")
def index():
    return flask.render_template("index.html")


@app.route("/rss")
def rss():
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
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    episodes, total_items = db_get_episodes(page=page, per_page=per_page)
    total_pages = math.ceil(total_items / per_page)
    return (
        jsonify(
            {
                "data": [episode.model_dump(mode="json") for episode in episodes],
                "pagination": {
                    "page": page,
                    "per_page": per_page,
                    "total_pages": total_pages,
                    "total_items": total_items,
                },
            }
        ),
        200,
    )


def generate_rss_feed():
    episodes = get_all_episodes()

    fg = FeedGenerator()
    fg.load_extension("podcast")
    fg.title(PODCAST_TITLE)
    fg.link(href=BASE_URL, rel="alternate")
    fg.description(PODCAST_DESCRIPTION)
    fg.language("en")

    for episode_info in episodes:
        fe = fg.add_entry(order="append")
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
