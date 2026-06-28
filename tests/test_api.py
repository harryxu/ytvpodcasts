"""
Tests for the vpodcasts FastAPI endpoints.

Endpoints covered
-----------------
GET  /rss
GET  /api/episodes
GET  /api/episodes?status=archived
GET  /api/episodes?status=all
POST /api/episodes/{id}/archive
POST /api/episodes/{id}/unarchive
DELETE /api/episodes/{id}
GET  /api/tasks

Excluded (as requested)
-----------------------
POST /api/add          – triggers external yt-dlp / Taskiq task
GET  /api/eventstream  – long-lived SSE stream backed by NATS
GET  /                 – Jinja2 template render
GET  /dashboard        – static file serve
GET  /assets/{path}    – static file serve
GET  /episodes/{file}  – audio file serve
"""

from __future__ import annotations


# ===========================================================================
# RSS feed
# ===========================================================================


class TestRssFeed:
    def test_rss_returns_xml(self, client):
        response = client.get("/rss")
        assert response.status_code == 200
        assert "application/xml" in response.headers["content-type"]

    def test_rss_contains_podcast_elements(self, client):
        response = client.get("/rss")
        content = response.text
        # Basic RSS structure
        assert "<rss" in content
        assert "<channel>" in content

    def test_rss_contains_active_episodes(self, client):
        """Non-archived episodes should appear in the feed."""
        response = client.get("/rss")
        content = response.text
        assert "Test Episode One" in content
        assert "Test Episode Two" in content

    def test_rss_excludes_archived_episodes(self, client):
        """Archived episodes should NOT appear in the default RSS feed."""
        response = client.get("/rss")
        content = response.text
        assert "Archived Episode" not in content


# ===========================================================================
# GET /api/episodes
# ===========================================================================


class TestGetEpisodes:
    def test_default_returns_active_episodes(self, client):
        response = client.get("/api/episodes")
        assert response.status_code == 200
        body = response.json()
        assert "data" in body
        assert "pagination" in body
        # Default status="default" means is_archived=False
        for ep in body["data"]:
            assert ep["is_archived"] is False

    def test_pagination_fields_present(self, client):
        response = client.get("/api/episodes")
        body = response.json()
        pagination = body["pagination"]
        assert "page" in pagination
        assert "per_page" in pagination
        assert "total_pages" in pagination
        assert "total_items" in pagination

    def test_pagination_defaults(self, client):
        response = client.get("/api/episodes")
        body = response.json()
        pagination = body["pagination"]
        assert pagination["page"] == 1
        assert pagination["per_page"] == 10

    def test_custom_pagination(self, client):
        response = client.get("/api/episodes?page=1&per_page=1")
        assert response.status_code == 200
        body = response.json()
        assert len(body["data"]) == 1
        assert body["pagination"]["per_page"] == 1

    def test_status_archived_filter(self, client):
        response = client.get("/api/episodes?status=archived")
        assert response.status_code == 200
        body = response.json()
        for ep in body["data"]:
            assert ep["is_archived"] is True
        titles = [ep["title"] for ep in body["data"]]
        assert "Archived Episode" in titles

    def test_status_all_returns_every_episode(self, client):
        response = client.get("/api/episodes?status=all")
        assert response.status_code == 200
        body = response.json()
        # All 3 seeded episodes should be returned in total
        assert body["pagination"]["total_items"] == 3

    def test_episode_fields(self, client):
        """Every episode object should contain the expected keys."""
        response = client.get("/api/episodes")
        body = response.json()
        assert len(body["data"]) > 0
        ep = body["data"][0]
        for key in ("id", "title", "webpage_url", "is_archived"):
            assert key in ep, f"Missing key: {key}"


# ===========================================================================
# POST /api/episodes/{id}/archive
# ===========================================================================


class TestArchiveEpisode:
    def test_archive_existing_episode(self, client):
        response = client.post("/api/episodes/test-episode-002/archive")
        assert response.status_code == 200
        body = response.json()
        assert "data" in body

    def test_archive_not_found(self, client):
        response = client.post("/api/episodes/nonexistent-id/archive")
        assert response.status_code == 404
        body = response.json()
        assert body["detail"] == "Episode not found"

    def test_archived_episode_no_longer_in_active_list(self, client):
        """After archiving test-episode-002 above, it should not appear in default listing."""
        response = client.get("/api/episodes")
        body = response.json()
        ids = [ep["id"] for ep in body["data"]]
        # test-episode-002 was archived in the previous test
        assert "test-episode-002" not in ids


# ===========================================================================
# POST /api/episodes/{id}/unarchive
# ===========================================================================


class TestUnarchiveEpisode:
    def test_unarchive_archived_episode(self, client):
        # The "archived" episode was seeded with is_archived=True
        response = client.post("/api/episodes/test-episode-archived/unarchive")
        assert response.status_code == 200
        body = response.json()
        assert "data" in body

    def test_unarchive_not_found(self, client):
        response = client.post("/api/episodes/does-not-exist/unarchive")
        assert response.status_code == 404
        body = response.json()
        assert body["detail"] == "Episode not found"

    def test_unarchived_episode_appears_in_active_list(self, client):
        """After unarchiving, the episode should show up in the default listing."""
        response = client.get("/api/episodes?status=all")
        body = response.json()
        ids = [ep["id"] for ep in body["data"]]
        assert "test-episode-archived" in ids


# ===========================================================================
# DELETE /api/episodes/{id}
# ===========================================================================


class TestDeleteEpisode:
    def test_delete_episode_not_found(self, client):
        response = client.delete("/api/episodes/totally-missing")
        assert response.status_code == 404
        body = response.json()
        assert body["detail"] == "Episode not found"

    def test_delete_existing_episode(self, client):
        """Delete test-episode-001 (audio file won't exist on disk, that's fine)."""
        response = client.delete("/api/episodes/test-episode-001")
        assert response.status_code == 200
        body = response.json()
        assert body["data"] is True

    def test_deleted_episode_gone(self, client):
        response = client.get("/api/episodes?status=all")
        body = response.json()
        ids = [ep["id"] for ep in body["data"]]
        assert "test-episode-001" not in ids


# ===========================================================================
# GET /api/tasks
# ===========================================================================


class TestGetTasks:
    def test_returns_200(self, client):
        response = client.get("/api/tasks")
        assert response.status_code == 200

    def test_response_structure(self, client):
        response = client.get("/api/tasks")
        body = response.json()
        assert "data" in body
        assert "pagination" in body
        assert "notify_count" in body

    def test_pagination_defaults(self, client):
        response = client.get("/api/tasks")
        body = response.json()
        pagination = body["pagination"]
        assert pagination["page"] == 1
        assert pagination["per_page"] == 10

    def test_custom_per_page(self, client):
        response = client.get("/api/tasks?page=1&per_page=1")
        assert response.status_code == 200
        body = response.json()
        assert len(body["data"]) <= 1

    def test_notify_count_is_integer(self, client):
        response = client.get("/api/tasks")
        body = response.json()
        assert isinstance(body["notify_count"], int)

    def test_notify_count_reflects_pending_and_failed(self, client):
        """Seeds contain 1 pending + 1 failed task = 2 notify_count."""
        response = client.get("/api/tasks")
        body = response.json()
        # Seeds: pending=1, processing=0, failed=1  → notify_count=2
        assert body["notify_count"] == 2

    def test_queue_task_id_excluded(self, client):
        """queue_task_id should be stripped from the response."""
        response = client.get("/api/tasks")
        body = response.json()
        for task in body["data"]:
            assert "queue_task_id" not in task

    def test_task_fields(self, client):
        response = client.get("/api/tasks")
        body = response.json()
        if body["data"]:
            task = body["data"][0]
            for key in ("id", "title", "status"):
                assert key in task, f"Missing key: {key}"
