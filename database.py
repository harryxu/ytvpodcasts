import os
from sqlmodel import create_engine, SQLModel, Session, select
from .models import Episode

DB_FILE = os.getenv("DB_FILE", "vpodcasts.db")
engine = create_engine(f"sqlite:///{DB_FILE}")

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def add_episode(episode_data):
    with Session(engine) as session:
        episode = Episode(**episode_data)
        session.add(episode)
        session.commit()

def get_all_episodes():
    with Session(engine) as session:
        episodes = session.exec(select(Episode).order_by(Episode.upload_date.desc())).all()
        return episodes

def episode_exists(video_id):
    with Session(engine) as session:
        return session.get(Episode, video_id) is not None