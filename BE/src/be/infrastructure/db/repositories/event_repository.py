from __future__ import annotations

from collections.abc import Sequence

from sqlalchemy import select

from be.domain.events.entities import Event, EventStatus, NotifyTarget, Schedule, ScheduleType
from be.infrastructure.db.models import EventModel
from be.infrastructure.db.session import DatabaseSessionManager


class SqlAlchemyEventRepository:
    def __init__(self, session_manager: DatabaseSessionManager) -> None:
        self._session_manager = session_manager

    async def create(self, event: Event) -> Event:
        async for session in self._session_manager.session():
            model = self._to_model(event)
            session.add(model)
            await session.commit()
            await session.refresh(model)
            return self._to_entity(model)
        raise RuntimeError("Database session was not created")

    async def list_events(self) -> Sequence[Event]:
        async for session in self._session_manager.session():
            result = await session.execute(select(EventModel).order_by(EventModel.created_at.desc()))
            models = result.scalars().all()
            return [self._to_entity(model) for model in models]
        raise RuntimeError("Database session was not created")

    async def get_by_id(self, event_id: str) -> Event | None:
        async for session in self._session_manager.session():
            result = await session.execute(select(EventModel).where(EventModel.id == event_id))
            model = result.scalar_one_or_none()
            return self._to_entity(model) if model else None
        raise RuntimeError("Database session was not created")

    async def update(self, event: Event) -> Event:
        async for session in self._session_manager.session():
            result = await session.execute(select(EventModel).where(EventModel.id == event.id))
            model = result.scalar_one()
            model.title = event.title
            model.instruction = event.instruction
            model.schedule_type = event.schedule.type.value
            model.run_at = event.schedule.run_at
            model.time_of_day = event.schedule.time_of_day
            model.days_of_week = list(event.schedule.days_of_week)
            model.timezone = event.schedule.timezone
            model.allowed_tools = list(event.allowed_tools)
            model.notify_target = event.notify_target.value
            model.status = event.status.value
            model.updated_at = event.updated_at
            model.last_run_at = event.last_run_at
            model.next_run_at = event.next_run_at
            await session.commit()
            await session.refresh(model)
            return self._to_entity(model)
        raise RuntimeError("Database session was not created")

    async def delete(self, event_id: str) -> None:
        async for session in self._session_manager.session():
            result = await session.execute(select(EventModel).where(EventModel.id == event_id))
            model = result.scalar_one()
            await session.delete(model)
            await session.commit()
            return
        raise RuntimeError("Database session was not created")

    def _to_model(self, event: Event) -> EventModel:
        return EventModel(
            id=event.id,
            title=event.title,
            instruction=event.instruction,
            schedule_type=event.schedule.type.value,
            run_at=event.schedule.run_at,
            time_of_day=event.schedule.time_of_day,
            days_of_week=list(event.schedule.days_of_week),
            timezone=event.schedule.timezone,
            allowed_tools=list(event.allowed_tools),
            notify_target=event.notify_target.value,
            status=event.status.value,
            created_at=event.created_at,
            updated_at=event.updated_at,
            last_run_at=event.last_run_at,
            next_run_at=event.next_run_at,
        )

    def _to_entity(self, model: EventModel) -> Event:
        return Event(
            id=model.id,
            title=model.title,
            instruction=model.instruction,
            schedule=Schedule(
                type=ScheduleType(model.schedule_type),
                timezone=model.timezone,
                run_at=model.run_at,
                time_of_day=model.time_of_day,
                days_of_week=list(model.days_of_week),
            ),
            allowed_tools=list(model.allowed_tools),
            notify_target=NotifyTarget(model.notify_target),
            status=EventStatus(model.status),
            created_at=model.created_at,
            updated_at=model.updated_at,
            last_run_at=model.last_run_at,
            next_run_at=model.next_run_at,
        )
