from datetime import UTC, datetime

from be.domain.events.entities import Event, EventStatus, NotifyTarget, Schedule, ScheduleType
from be.scheduler.recurrence import compute_next_run


def _event(schedule: Schedule, *, status: EventStatus = EventStatus.ACTIVE) -> Event:
    now = datetime(2026, 3, 30, 0, 0, tzinfo=UTC)
    return Event(
        id="event-1",
        title="Scheduled job",
        instruction="Run task",
        schedule=schedule,
        allowed_tools=["web_search"],
        notify_target=NotifyTarget.DASHBOARD,
        status=status,
        created_at=now,
        updated_at=now,
        last_run_at=None,
        next_run_at=None,
    )


def test_compute_next_run_for_once_returns_run_at_when_future() -> None:
    run_at = datetime(2026, 3, 30, 9, 0, tzinfo=UTC)

    result = compute_next_run(
        _event(Schedule(type=ScheduleType.ONCE, timezone="UTC", run_at=run_at)),
        now=datetime(2026, 3, 30, 8, 0, tzinfo=UTC),
    )

    assert result == run_at


def test_compute_next_run_for_once_returns_none_when_past() -> None:
    result = compute_next_run(
        _event(
            Schedule(
                type=ScheduleType.ONCE,
                timezone="UTC",
                run_at=datetime(2026, 3, 30, 7, 0, tzinfo=UTC),
            ),
        ),
        now=datetime(2026, 3, 30, 8, 0, tzinfo=UTC),
    )

    assert result is None


def test_compute_next_run_for_daily_returns_same_day_slot_when_not_passed() -> None:
    result = compute_next_run(
        _event(
            Schedule(
                type=ScheduleType.DAILY,
                timezone="Asia/Seoul",
                time_of_day="09:00",
            ),
        ),
        now=datetime(2026, 3, 30, 23, 30, tzinfo=UTC),
    )

    assert result == datetime(2026, 3, 31, 0, 0, tzinfo=UTC)


def test_compute_next_run_for_daily_rolls_to_next_day_after_slot() -> None:
    result = compute_next_run(
        _event(
            Schedule(
                type=ScheduleType.DAILY,
                timezone="Asia/Seoul",
                time_of_day="09:00",
            ),
        ),
        now=datetime(2026, 3, 31, 0, 30, tzinfo=UTC),
    )

    assert result == datetime(2026, 4, 1, 0, 0, tzinfo=UTC)


def test_compute_next_run_for_weekly_returns_next_matching_weekday() -> None:
    result = compute_next_run(
        _event(
            Schedule(
                type=ScheduleType.WEEKLY,
                timezone="UTC",
                time_of_day="09:00",
                days_of_week=[2, 4],
            ),
        ),
        now=datetime(2026, 3, 30, 10, 0, tzinfo=UTC),
    )

    assert result == datetime(2026, 4, 1, 9, 0, tzinfo=UTC)


def test_compute_next_run_for_weekly_honors_timezone() -> None:
    result = compute_next_run(
        _event(
            Schedule(
                type=ScheduleType.WEEKLY,
                timezone="America/New_York",
                time_of_day="09:30",
                days_of_week=[0],
            ),
        ),
        now=datetime(2026, 3, 30, 12, 0, tzinfo=UTC),
    )

    assert result == datetime(2026, 3, 30, 13, 30, tzinfo=UTC)
