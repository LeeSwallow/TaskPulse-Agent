from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from be.app import create_app
from be.config import get_settings


def _make_test_client(tmp_path: Path) -> TestClient:
    get_settings.cache_clear()
    import os

    os.environ["DATABASE_URL"] = f"sqlite+aiosqlite:///{tmp_path / 'events.db'}"
    os.environ["REDIS_URL"] = "redis://localhost:6379/15"
    return TestClient(create_app())


def test_event_crud_flow(tmp_path: Path) -> None:
    with _make_test_client(tmp_path) as client:
        create_response = client.post(
            "/api/events",
            json={
                "title": "Morning Briefing",
                "instruction": "Summarize the industry news",
                "schedule": {
                    "type": "daily",
                    "time_of_day": "09:00",
                    "timezone": "Asia/Seoul",
                    "days_of_week": [],
                },
                "allowed_tools": ["web_search"],
                "notify_target": "dashboard",
            },
        )

        assert create_response.status_code == 201
        event = create_response.json()
        event_id = event["id"]
        assert event["title"] == "Morning Briefing"
        assert event["status"] == "active"

        list_response = client.get("/api/events")
        assert list_response.status_code == 200
        assert len(list_response.json()) == 1

        update_response = client.patch(
            f"/api/events/{event_id}",
            json={
                "title": "Updated Briefing",
                "allowed_tools": ["web_search", "send_slack"],
            },
        )
        assert update_response.status_code == 200
        assert update_response.json()["title"] == "Updated Briefing"
        assert update_response.json()["allowed_tools"] == ["web_search", "send_slack"]

        delete_response = client.delete(f"/api/events/{event_id}")
        assert delete_response.status_code == 204

        list_after_delete = client.get("/api/events")
        assert list_after_delete.status_code == 200
        assert list_after_delete.json() == []


def test_update_non_existing_event_returns_404(tmp_path: Path) -> None:
    with _make_test_client(tmp_path) as client:
        response = client.patch(
            "/api/events/does-not-exist",
            json={"title": "Updated"},
        )

        assert response.status_code == 404
        assert response.json() == {"detail": "Event not found"}


def test_create_event_with_invalid_schedule_returns_422(tmp_path: Path) -> None:
    with _make_test_client(tmp_path) as client:
        response = client.post(
            "/api/events",
            json={
                "title": "Weekly Briefing",
                "instruction": "Summarize the industry news",
                "schedule": {
                    "type": "weekly",
                    "time_of_day": "09:00",
                    "timezone": "Asia/Seoul",
                    "days_of_week": [],
                },
                "allowed_tools": ["web_search"],
                "notify_target": "dashboard",
            },
        )

        assert response.status_code == 422
