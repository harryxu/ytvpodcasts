# pyright: reportAttributeAccessIssue=false

from typing import Any
from sqlmodel import create_engine, SQLModel, Session, select, func
from vpodcasts.models import DownloadTask, Episode
from vpodcasts.config import DB_FILE

engine = create_engine(f"sqlite:///{DB_FILE}")


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def add_episode(episode_data: dict[str, Any]):
    with Session(engine) as session:
        episode = Episode(**episode_data)
        session.add(episode)
        session.commit()


def get_all_episodes(is_archived: bool = False):
    with Session(engine) as session:
        episodes = session.exec(
            select(Episode)
            .where(Episode.is_archived == is_archived)
            .order_by(Episode.create_date.desc())
        ).all()
        return episodes


def get_episodes(page: int = 1, per_page: int = 10, is_archived: bool = False):
    with Session(engine) as session:
        offset = (page - 1) * per_page

        count_statement = (
            select(func.count())
            .select_from(Episode)
            .where(Episode.is_archived == is_archived)
        )
        total_count = session.exec(count_statement).one()

        episodes = session.exec(
            select(Episode)
            .where(Episode.is_archived == is_archived)
            .order_by(Episode.create_date.desc())
            .offset(offset)
            .limit(per_page)
        ).all()
        return episodes, total_count


def episode_exists(video_id: str):
    with Session(engine) as session:
        return session.get(Episode, video_id) is not None


def delete_episode(video_id: str):
    with Session(engine) as session:
        episode = session.get(Episode, video_id)
        if episode:
            session.delete(episode)
            session.commit()


def get_download_tasks(page: int = 1, per_page: int = 10, status: str | None = None):
    with Session(engine) as session:
        offset = (page - 1) * per_page

        total_count = session.exec(select(func.count()).select_from(DownloadTask)).one()
        notify_count = session.exec(
            select(func.count())
            .select_from(DownloadTask)
            .where(DownloadTask.status.in_(["pending", "processing", "failed"]))
        ).one()

        statement = (
            select(DownloadTask)
            .order_by(DownloadTask.updated_at.desc())
            .offset(offset)
            .limit(per_page)
        )
        if status:
            statement = statement.where(DownloadTask.status == status)
        download_tasks = session.exec(statement).all()
        return download_tasks, total_count, notify_count
