from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from be.domain.events.entities import EventStatus, NotifyTarget, ScheduleType


@dataclass(frozen=True)
class ScheduleInput:
    type: ScheduleType
    timezone: str
    run_at: datetime | None = None
    time_of_day: str | None = None
    days_of_week: list[int] = field(default_factory=list)


@dataclass(frozen=True)
class CreateEventInput:
    title: str
    instruction: str
    schedule: ScheduleInput
    allowed_tools: list[str] = field(default_factory=list)
    notify_target: NotifyTarget = NotifyTarget.DASHBOARD


@dataclass(frozen=True)
class UpdateEventInput:
    title: str | None = None
    instruction: str | None = None
    schedule: ScheduleInput | None = None
    allowed_tools: list[str] | None = None
    notify_target: NotifyTarget | None = None
    status: EventStatus | None = None
