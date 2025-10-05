from sqlmodel import create_engine, SQLModel, Session, select, func
from vpodcasts.models import Episode
from vpodcasts.config import DB_FILE

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
        episodes = session.exec(
            select(Episode).order_by(Episode.create_date.desc())
        ).all()
        return episodes


def get_episodes(page: int = 1, per_page: int = 10):
    with Session(engine) as session:
        offset = (page - 1) * per_page

        count_statement = select(func.count()).select_from(Episode)
        total_count = session.exec(count_statement).one()

        episodes = session.exec(
            select(Episode)
            .order_by(Episode.create_date.desc())
            .offset(offset)
            .limit(per_page)
        ).all()
        return episodes, total_count


def episode_exists(video_id):
    with Session(engine) as session:
        return session.get(Episode, video_id) is not None


def delete_episode(video_id: str):
    with Session(engine) as session:
        episode = session.get(Episode, video_id)
        if episode:
            session.delete(episode)
            session.commit()
