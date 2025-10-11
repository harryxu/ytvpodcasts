from sqlmodel import Field, SQLModel
from datetime import datetime, timezone
import sqlalchemy as sa


class Episode(SQLModel, table=True):
    id: str = Field(default=None, primary_key=True)
    title: str
    description: str | None = None
    webpage_url: str = Field(unique=True)
    upload_date: str | None = None
    duration: int | None = None
    thumbnail: str | None = None
    audio_file: str | None = None
    audio_file_size: int | None = None
    audio_file_type: str | None = None
    create_date: datetime | None = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class DownloadTask(SQLModel, table=True):
    __tablename__: str = "download_tasks"

    id: int = Field(default=None, primary_key=True)
    queue_task_id: str = Field(max_length=100)
    title: str = Field(max_length=100)
    description: str | None = None
    status: str = Field(max_length=50)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=sa.Column(
            sa.DateTime(timezone=True),
            onupdate=datetime.now(timezone.utc),
            nullable=False,
        ),
    )
    completed_at: datetime | None = None
    episode_id: str | None = Field(default=None, foreign_key="episode.id")
