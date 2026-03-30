from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator

from be.application.events.dto import CreateEventInput, ScheduleInput, UpdateEventInput
from be.domain.events.entities import EventStatus, NotifyTarget, ScheduleType


class ScheduleDefinition(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    type: ScheduleType
    timezone: str = "Asia/Seoul"
    run_at: datetime | None = None
    time_of_day: str | None = None
    days_of_week: list[int] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_schedule(self) -> "ScheduleDefinition":
        if self.type == ScheduleType.ONCE and self.run_at is None:
            raise ValueError("run_at is required for once schedule")

        if self.type in {ScheduleType.DAILY, ScheduleType.WEEKLY} and not self.time_of_day:
            raise ValueError("time_of_day is required for recurring schedule")

        if self.type == ScheduleType.WEEKLY and not self.days_of_week:
            raise ValueError("days_of_week is required for weekly schedule")

        return self

    def to_input(self) -> ScheduleInput:
        return ScheduleInput(
            type=self.type,
            timezone=self.timezone,
            run_at=self.run_at,
            time_of_day=self.time_of_day,
            days_of_week=list(self.days_of_week),
        )


class EventCreateRequest(BaseModel):
    title: str
    instruction: str
    schedule: ScheduleDefinition
    allowed_tools: list[str] = Field(default_factory=list)
    notify_target: NotifyTarget = NotifyTarget.DASHBOARD

    def to_input(self) -> CreateEventInput:
        return CreateEventInput(
            title=self.title,
            instruction=self.instruction,
            schedule=self.schedule.to_input(),
            allowed_tools=list(self.allowed_tools),
            notify_target=self.notify_target,
        )


class EventUpdateRequest(BaseModel):
    title: str | None = None
    instruction: str | None = None
    schedule: ScheduleDefinition | None = None
    allowed_tools: list[str] | None = None
    notify_target: NotifyTarget | None = None
    status: EventStatus | None = None

    def to_input(self) -> UpdateEventInput:
        return UpdateEventInput(
            title=self.title,
            instruction=self.instruction,
            schedule=self.schedule.to_input() if self.schedule is not None else None,
            allowed_tools=list(self.allowed_tools) if self.allowed_tools is not None else None,
            notify_target=self.notify_target,
            status=self.status,
        )


class EventResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    instruction: str
    schedule: ScheduleDefinition
    allowed_tools: list[str]
    notify_target: NotifyTarget
    status: EventStatus
    created_at: datetime
    updated_at: datetime
    last_run_at: datetime | None = None
    next_run_at: datetime | None = None
