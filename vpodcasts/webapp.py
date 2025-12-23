from vpodcasts.taskiq_broker import create_video_download_task, broker as taskiq_broker
import asyncio
import json
import math
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, Response, StreamingResponse
from fastapi.templating import Jinja2Templates
from feedgen.feed import FeedGenerator
from loguru import logger
from nats.aio.client import Client as NATS
from pydantic import BaseModel
from sqlmodel import Session, select


import vpodcasts.database as db
from vpodcasts.config import (
    BASE_URL,
    EPISODES_DIR,
    NATS_URL,
    PODCAST_DESCRIPTION,
    PODCAST_TITLE,
)
from vpodcasts.database import engine
from vpodcasts.models import Episode

nc = NATS()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await nc.connect(NATS_URL)
    yield
    # Shutdown
    await nc.drain()


app = FastAPI(lifespan=lifespan)
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
async def add_episode(payload: AddEpisodePayload):
    if not payload.url:
        raise HTTPException(status_code=400, detail="Missing url")
    await create_video_download_task(payload.url)
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


@app.post("/api/episodes/{id}/archive")
def archive_episode(id):
    with Session(engine) as session:
        episode = session.exec(select(Episode).where(Episode.id == id)).first()
        if episode:
            episode.is_archived = True
            session.commit()
            return {"data": episode.model_dump_json()}
        else:
            raise HTTPException(status_code=404, detail="Episode not found")


@app.delete("/api/episodes/{id}")
def delete_episode(id):
    with Session(engine) as session:
        episode = session.exec(select(Episode).where(Episode.id == id)).first()
        if episode:
            file = f"{EPISODES_DIR}/{episode.audio_file}"
            if os.path.exists(file):
                os.remove(file)
            session.delete(episode)
            session.commit()
            return {"data": True}
        else:
            raise HTTPException(status_code=404, detail="Episode not found")


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


@app.get("/api/eventstream")
async def subscribe():
    queue: asyncio.Queue = asyncio.Queue()

    subject = "notification"

    async def handler(msg):
        data = msg.data.decode()
        logger.info(f"nats Received message: {data}")
        await queue.put(json.loads(data))

    sub = await nc.subscribe(subject, cb=handler)

    async def event_stream():
        try:
            while True:
                message = await queue.get()
                yield "data: " + json.dumps(message) + "\n\n"
        except asyncio.CancelledError:
            pass
        finally:
            await sub.unsubscribe()

    return StreamingResponse(
        event_stream(),
        # media_type="application/json",
        media_type="text/event-stream",
    )
