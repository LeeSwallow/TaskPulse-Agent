from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from be.application.events.dto import CreateEventInput, UpdateEventInput
from be.domain.events.entities import Event, EventStatus, Schedule, ScheduleType
from be.domain.events.repository import EventRepository


class EventService:
    def __init__(self, event_repository: EventRepository) -> None:
        self._event_repository = event_repository

    async def list_events(self) -> list[Event]:
        events = await self._event_repository.list_events()
        return list(events)

    async def create_event(self, payload: CreateEventInput) -> Event:
        now = datetime.now(UTC)
        event = Event(
            id=str(uuid4()),
            title=payload.title,
            instruction=payload.instruction,
            schedule=Schedule(
                type=payload.schedule.type,
                timezone=payload.schedule.timezone,
                run_at=payload.schedule.run_at,
                time_of_day=payload.schedule.time_of_day,
                days_of_week=list(payload.schedule.days_of_week),
            ),
            allowed_tools=list(payload.allowed_tools),
            notify_target=payload.notify_target,
            status=EventStatus.ACTIVE,
            created_at=now,
            updated_at=now,
            last_run_at=None,
            next_run_at=payload.schedule.run_at,
        )
        return await self._event_repository.create(event)

    async def update_event(self, event_id: str, payload: UpdateEventInput) -> Event | None:
        current = await self._event_repository.get_by_id(event_id)
        if current is None:
            return None

        schedule = current.schedule
        if payload.schedule is not None:
            schedule = Schedule(
                type=payload.schedule.type,
                timezone=payload.schedule.timezone,
                run_at=payload.schedule.run_at,
                time_of_day=payload.schedule.time_of_day,
                days_of_week=list(payload.schedule.days_of_week),
            )

        updated = Event(
            id=current.id,
            title=payload.title or current.title,
            instruction=payload.instruction or current.instruction,
            schedule=schedule,
            allowed_tools=payload.allowed_tools if payload.allowed_tools is not None else current.allowed_tools,
            notify_target=payload.notify_target or current.notify_target,
            status=payload.status or current.status,
            created_at=current.created_at,
            updated_at=datetime.now(UTC),
            last_run_at=current.last_run_at,
            next_run_at=schedule.run_at if schedule.type == ScheduleType.ONCE else current.next_run_at,
        )
        return await self._event_repository.update(updated)

    async def delete_event(self, event_id: str) -> bool:
        current = await self._event_repository.get_by_id(event_id)
        if current is None:
            return False

        await self._event_repository.delete(event_id)
        return True
