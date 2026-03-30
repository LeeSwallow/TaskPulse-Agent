from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum


class ScheduleType(StrEnum):
    ONCE = "once"
    DAILY = "daily"
    WEEKLY = "weekly"


class EventStatus(StrEnum):
    ACTIVE = "active"
    PAUSED = "paused"


class NotifyTarget(StrEnum):
    DASHBOARD = "dashboard"
    SLACK = "slack"
    NOTION = "notion"


@dataclass(frozen=True)
class Schedule:
    type: ScheduleType
    timezone: str
    run_at: datetime | None = None
    time_of_day: str | None = None
    days_of_week: list[int] = field(default_factory=list)


@dataclass(frozen=True)
class Event:
    id: str
    title: str
    instruction: str
    schedule: Schedule
    allowed_tools: list[str]
    notify_target: NotifyTarget
    status: EventStatus
    created_at: datetime
    updated_at: datetime
    last_run_at: datetime | None = None
    next_run_at: datetime | None = None
