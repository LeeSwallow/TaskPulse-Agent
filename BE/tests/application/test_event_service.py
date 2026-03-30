from __future__ import annotations

import asyncio
from collections.abc import Sequence
from datetime import UTC, datetime

from be.application.events.dto import CreateEventInput, ScheduleInput, UpdateEventInput
from be.application.events.service import EventService
from be.domain.events.entities import Event, EventStatus, NotifyTarget, Schedule, ScheduleType


class StubEventRepository:
    def __init__(self, initial_events: list[Event] | None = None) -> None:
        self._events = {event.id: event for event in initial_events or []}

    async def create(self, event: Event) -> Event:
        self._events[event.id] = event
        return event

    async def list_events(self) -> Sequence[Event]:
        return list(self._events.values())

    async def get_by_id(self, event_id: str) -> Event | None:
        return self._events.get(event_id)

    async def update(self, event: Event) -> Event:
        self._events[event.id] = event
        return event

    async def delete(self, event_id: str) -> None:
        self._events.pop(event_id, None)


def _event(event_id: str = "event-1") -> Event:
    now = datetime(2026, 3, 30, 0, 0, tzinfo=UTC)
    return Event(
        id=event_id,
        title="Morning Briefing",
        instruction="Summarize news",
        schedule=Schedule(
            type=ScheduleType.DAILY,
            timezone="Asia/Seoul",
            time_of_day="09:00",
        ),
        allowed_tools=["web_search"],
        notify_target=NotifyTarget.DASHBOARD,
        status=EventStatus.ACTIVE,
        created_at=now,
        updated_at=now,
        last_run_at=None,
        next_run_at=None,
    )


def test_create_event_sets_default_active_status() -> None:
    async def scenario() -> None:
        service = EventService(StubEventRepository())

        created = await service.create_event(
            CreateEventInput(
                title="Weekly Sync",
                instruction="Prepare agenda",
                schedule=ScheduleInput(
                    type=ScheduleType.WEEKLY,
                    timezone="Asia/Seoul",
                    time_of_day="10:30",
                    days_of_week=[0, 2],
                ),
                allowed_tools=["calendar"],
                notify_target=NotifyTarget.SLACK,
            ),
        )

        assert created.title == "Weekly Sync"
        assert created.status == EventStatus.ACTIVE
        assert created.allowed_tools == ["calendar"]
        assert created.notify_target == NotifyTarget.SLACK

    asyncio.run(scenario())


def test_update_event_replaces_selected_fields_only() -> None:
    async def scenario() -> None:
        service = EventService(StubEventRepository([_event()]))

        updated = await service.update_event(
            "event-1",
            UpdateEventInput(
                title="Updated Briefing",
                allowed_tools=["web_search", "send_slack"],
                status=EventStatus.PAUSED,
            ),
        )

        assert updated is not None
        assert updated.title == "Updated Briefing"
        assert updated.instruction == "Summarize news"
        assert updated.allowed_tools == ["web_search", "send_slack"]
        assert updated.status == EventStatus.PAUSED

    asyncio.run(scenario())


def test_update_event_returns_none_when_missing() -> None:
    async def scenario() -> None:
        service = EventService(StubEventRepository())

        updated = await service.update_event("missing", UpdateEventInput(title="noop"))

        assert updated is None

    asyncio.run(scenario())


def test_delete_event_returns_false_when_missing() -> None:
    async def scenario() -> None:
        service = EventService(StubEventRepository())

        deleted = await service.delete_event("missing")

        assert deleted is False

    asyncio.run(scenario())
