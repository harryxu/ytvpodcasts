from sqlmodel import Field, SQLModel
from datetime import datetime, timezone


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
