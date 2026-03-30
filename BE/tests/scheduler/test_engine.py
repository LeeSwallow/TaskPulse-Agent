from datetime import UTC, datetime

from be.domain.events.entities import Event, EventStatus, NotifyTarget, Schedule, ScheduleType
from be.scheduler.engine import collect_due_events, is_event_due


def _event(
    event_id: str,
    *,
    status: EventStatus = EventStatus.ACTIVE,
    next_run_at: datetime | None,
) -> Event:
    now = datetime(2026, 3, 30, 0, 0, tzinfo=UTC)
    return Event(
        id=event_id,
        title="Scheduled job",
        instruction="Run task",
        schedule=Schedule(type=ScheduleType.DAILY, timezone="UTC", time_of_day="09:00"),
        allowed_tools=["web_search"],
        notify_target=NotifyTarget.DASHBOARD,
        status=status,
        created_at=now,
        updated_at=now,
        last_run_at=None,
        next_run_at=next_run_at,
    )


def test_is_event_due_returns_true_only_for_active_due_event() -> None:
    now = datetime(2026, 3, 30, 8, 0, tzinfo=UTC)

    assert is_event_due(_event("due", next_run_at=datetime(2026, 3, 30, 8, 0, tzinfo=UTC)), now=now) is True
    assert is_event_due(_event("future", next_run_at=datetime(2026, 3, 30, 8, 1, tzinfo=UTC)), now=now) is False
    assert is_event_due(_event("missing", next_run_at=None), now=now) is False


def test_collect_due_events_excludes_paused_and_future_events() -> None:
    now = datetime(2026, 3, 30, 8, 0, tzinfo=UTC)
    events = [
        _event("due-1", next_run_at=datetime(2026, 3, 30, 7, 59, tzinfo=UTC)),
        _event("paused", status=EventStatus.PAUSED, next_run_at=datetime(2026, 3, 30, 7, 0, tzinfo=UTC)),
        _event("future", next_run_at=datetime(2026, 3, 30, 8, 1, tzinfo=UTC)),
    ]

    result = collect_due_events(events, now=now)

    assert [event.id for event in result] == ["due-1"]
