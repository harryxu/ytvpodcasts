from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import datetime, timezone


class Episode(SQLModel, table=True):
    id: str = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    webpage_url: str = Field(unique=True)
    upload_date: Optional[str] = None
    duration: Optional[int] = None
    thumbnail: Optional[str] = None
    audio_file: Optional[str] = None
    audio_file_size: Optional[int] = None
    audio_file_type: Optional[str] = None
    create_date: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
