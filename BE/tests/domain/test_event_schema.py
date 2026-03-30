from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from be.presentation.api.v1.events.schemas import (
    EventCreateRequest,
    EventResponse,
    ScheduleDefinition,
    ScheduleType,
)


def test_once_schedule_requires_run_at() -> None:
    with pytest.raises(ValidationError):
        ScheduleDefinition(type=ScheduleType.ONCE, timezone="Asia/Seoul")


def test_daily_schedule_requires_time_of_day() -> None:
    with pytest.raises(ValidationError):
        ScheduleDefinition(type=ScheduleType.DAILY, timezone="Asia/Seoul")


def test_weekly_schedule_requires_days_of_week() -> None:
    with pytest.raises(ValidationError):
        ScheduleDefinition(
            type=ScheduleType.WEEKLY,
            time_of_day="09:00",
            timezone="Asia/Seoul",
        )


def test_event_create_serializes_expected_fields() -> None:
    payload = EventCreateRequest(
        title="Morning Briefing",
        instruction="Summarize the industry news",
        schedule=ScheduleDefinition(
            type=ScheduleType.DAILY,
            time_of_day="09:00",
            timezone="Asia/Seoul",
        ),
        allowed_tools=["web_search", "send_slack"],
        notify_target="slack",
    )

    assert payload.title == "Morning Briefing"
    assert payload.allowed_tools == ["web_search", "send_slack"]
    assert payload.notify_target == "slack"


def test_event_response_contains_status_fields() -> None:
    now = datetime.now(UTC)
    event = EventResponse(
        id="event-1",
        title="Morning Briefing",
        instruction="Summarize the industry news",
        schedule=ScheduleDefinition(
            type=ScheduleType.ONCE,
            run_at=now,
            timezone="Asia/Seoul",
        ),
        allowed_tools=["web_search"],
        notify_target="dashboard",
        status="active",
        created_at=now,
        updated_at=now,
        last_run_at=None,
        next_run_at=now,
    )

    assert event.status == "active"
    assert event.next_run_at == now
