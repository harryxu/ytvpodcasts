import math
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import Response, FileResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from feedgen.feed import FeedGenerator

from vpodcasts.config import BASE_URL, EPISODES_DIR, PODCAST_DESCRIPTION, PODCAST_TITLE
import vpodcasts.database as db
from vpodcasts.huey_tasks import create_video_download_task

app = FastAPI()
templates = Jinja2Templates(directory="vpodcasts/templates")


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/rss")
def rss():
    # Provide the RSS feed dynamically
    rss_feed = generate_rss_feed()
    return Response(content=rss_feed, media_type="application/xml")


@app.get("/episodes/{filename:path}")
def download_episode(filename: str):
    # Provide the audio files
    return FileResponse(f"{EPISODES_DIR}/{filename}")


class AddEpisodePayload(BaseModel):
    url: str


@app.post("/api/add")
def add_episode(payload: AddEpisodePayload):
    if not payload.url:
        raise HTTPException(status_code=400, detail="Missing url")
    create_video_download_task(payload.url)
    return {"data": True}


@app.get("/api/episodes")
def get_episodes(page: int = 1, per_page: int = 10):
    episodes, total_items = db.get_episodes(page=page, per_page=per_page)
    total_pages = math.ceil(total_items / per_page)
    return {
        "data": [episode.model_dump(mode="json") for episode in episodes],
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total_pages": total_pages,
            "total_items": total_items,
        },
    }


@app.get("/api/tasks")
def get_tasks(page: int = 1, per_page: int = 10):
    tasks, total_items, notify_count = db.get_download_tasks(
        page=page, per_page=per_page
    )
    total_pages = math.ceil(total_items / per_page)
    return {
        "data": [
            task.model_dump(mode="json", exclude={"queue_task_id"}) for task in tasks
        ],
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total_pages": total_pages,
            "total_items": total_items,
        },
        "notify_count": notify_count,
    }


def generate_rss_feed():
    episodes = db.get_all_episodes()

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
