from __future__ import annotations

from datetime import UTC, datetime, time, timedelta
from zoneinfo import ZoneInfo

from be.domain.events.entities import Event, ScheduleType


def compute_next_run(event: Event, *, now: datetime) -> datetime | None:
    if event.status.value == "paused":
        return None

    if now.tzinfo is None:
        msg = "now must be timezone-aware"
        raise ValueError(msg)

    schedule = event.schedule
    if schedule.type == ScheduleType.ONCE:
        if schedule.run_at is None:
            return None
        return schedule.run_at if schedule.run_at >= now else None

    timezone = ZoneInfo(schedule.timezone)
    local_now = now.astimezone(timezone)
    scheduled_time = _parse_time_of_day(schedule.time_of_day)

    if schedule.type == ScheduleType.DAILY:
        candidate = datetime.combine(local_now.date(), scheduled_time, tzinfo=timezone)
        if candidate < local_now:
            candidate += timedelta(days=1)
        return candidate.astimezone(UTC)

    if schedule.type == ScheduleType.WEEKLY:
        for offset in range(8):
            candidate_date = local_now.date() + timedelta(days=offset)
            if candidate_date.weekday() not in schedule.days_of_week:
                continue
            candidate = datetime.combine(candidate_date, scheduled_time, tzinfo=timezone)
            if candidate >= local_now:
                return candidate.astimezone(UTC)
        return None

    return None


def _parse_time_of_day(value: str | None) -> time:
    if value is None:
        msg = "time_of_day is required for recurring schedules"
        raise ValueError(msg)
    hour_text, minute_text = value.split(":", maxsplit=1)
    return time(hour=int(hour_text), minute=int(minute_text))
