"""
Shared pytest fixtures for vpodcasts API tests.

Strategy
--------
* Use an **in-memory SQLite** database so tests never touch the real DB file.
* Patch `vpodcasts.database.engine` and `vpodcasts.webapp.engine` so every
  code-path (both the db-helper functions and the inline Session() calls in
  webapp.py) use the test engine.
* Mock the NATS connection and Taskiq broker startup/shutdown so the test
  client doesn't require those external services.
* Provide a pre-seeded database with sample Episodes and DownloadTasks.
"""

from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine, StaticPool

# ---------------------------------------------------------------------------
# Test database engine (in-memory SQLite, shared across connections)
# ---------------------------------------------------------------------------

TEST_DB_URL = "sqlite://"  # pure in-memory


@pytest.fixture(scope="session")
def test_engine():
    """Create a shared in-memory SQLite engine for the entire test session."""
    # Import models first so SQLModel.metadata is populated before create_all
    import vpodcasts.models  # noqa: F401

    engine = create_engine(
        TEST_DB_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    return engine


# ---------------------------------------------------------------------------
# Sample fixture data
# ---------------------------------------------------------------------------

SAMPLE_EPISODES = [
    {
        "id": "test-episode-001",
        "title": "Test Episode One",
        "description": "First test episode description",
        "webpage_url": "https://www.youtube.com/watch?v=test001",
        "upload_date": "20240101",
        "duration": 3600,
        "thumbnail": "https://img.youtube.com/test001.jpg",
        "audio_file": "test001.m4a",
        "audio_file_size": 1024000,
        "audio_file_type": "audio/mp4",
        "create_date": datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc),
        "is_archived": False,
    },
    {
        "id": "test-episode-002",
        "title": "Test Episode Two",
        "description": "Second test episode description",
        "webpage_url": "https://www.youtube.com/watch?v=test002",
        "upload_date": "20240202",
        "duration": 1800,
        "thumbnail": "https://img.youtube.com/test002.jpg",
        "audio_file": "test002.m4a",
        "audio_file_size": 512000,
        "audio_file_type": "audio/mp4",
        "create_date": datetime(2024, 2, 2, 12, 0, 0, tzinfo=timezone.utc),
        "is_archived": False,
    },
    {
        "id": "test-episode-archived",
        "title": "Archived Episode",
        "description": "This episode has been archived",
        "webpage_url": "https://www.youtube.com/watch?v=testarchived",
        "upload_date": "20230101",
        "duration": 900,
        "thumbnail": None,
        "audio_file": "archived.m4a",
        "audio_file_size": 256000,
        "audio_file_type": "audio/mp4",
        "create_date": datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc),
        "is_archived": True,
    },
]

SAMPLE_TASKS = [
    {
        "title": "Download task 1",
        "description": "Processing video test001",
        "status": "success",
        "is_unread": False,
        "episode_id": "test-episode-001",
    },
    {
        "title": "Download task 2",
        "description": "Processing video test002",
        "status": "pending",
        "is_unread": True,
        "episode_id": None,
    },
    {
        "title": "Download task 3",
        "description": "Failed attempt",
        "status": "failed",
        "is_unread": True,
        "episode_id": None,
    },
]


@pytest.fixture(scope="session")
def seeded_engine(test_engine):
    """Seed the test database with sample episodes and download tasks."""
    from vpodcasts.models import DownloadTask, Episode

    with Session(test_engine) as session:
        for ep_data in SAMPLE_EPISODES:
            session.add(Episode(**ep_data))
        session.commit()

        for task_data in SAMPLE_TASKS:
            session.add(DownloadTask(**task_data))
        session.commit()

    return test_engine


# ---------------------------------------------------------------------------
# TestClient with all external dependencies mocked
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def client(seeded_engine):
    """
    Return a FastAPI TestClient backed by the seeded in-memory test engine.

    Patches applied for the duration of the session:
    - ``vpodcasts.database.engine`` — so db helper functions use the test engine
    - ``vpodcasts.webapp.engine``   — so inline Session(engine) calls use the test engine
    - NATS connect / drain           — replaced with no-op AsyncMocks
    - Taskiq broker startup/shutdown — replaced with no-op AsyncMocks
    """
    mock_nats = MagicMock()
    mock_nats.connect = AsyncMock()
    mock_nats.drain = AsyncMock()

    mock_broker = MagicMock()
    mock_broker.startup = AsyncMock()
    mock_broker.shutdown = AsyncMock()

    @asynccontextmanager
    async def mock_lifespan(app):
        yield

    with (
        patch("vpodcasts.database.engine", seeded_engine),
        patch("vpodcasts.webapp.engine", seeded_engine),
        patch("vpodcasts.webapp.nc", mock_nats),
        patch("vpodcasts.webapp.taskiq_broker", mock_broker),
        patch("vpodcasts.webapp.lifespan", mock_lifespan),
    ):
        from vpodcasts.webapp import app

        app.router.lifespan_context = mock_lifespan
        with TestClient(app, raise_server_exceptions=True) as c:
            yield c
