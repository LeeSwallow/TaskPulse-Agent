from __future__ import annotations

import asyncio
from datetime import UTC, datetime

from be.domain.events.entities import Event, EventStatus, NotifyTarget, Schedule, ScheduleType
from be.infrastructure.db.repositories.event_repository import SqlAlchemyEventRepository
from be.infrastructure.db.session import DatabaseSessionManager


def _event(event_id: str = "1f1e2d3c-4b5a-6789-8abc-def012345678") -> Event:
    now = datetime(2026, 3, 30, 0, 0, tzinfo=UTC)
    return Event(
        id=event_id,
        title="Morning Briefing",
        instruction="Summarize news",
        schedule=Schedule(
            type=ScheduleType.WEEKLY,
            timezone="Asia/Seoul",
            time_of_day="09:00",
            days_of_week=[0, 2],
        ),
        allowed_tools=["web_search"],
        notify_target=NotifyTarget.DASHBOARD,
        status=EventStatus.ACTIVE,
        created_at=now,
        updated_at=now,
        last_run_at=None,
        next_run_at=datetime(2026, 3, 31, 0, 0, tzinfo=UTC),
    )


def test_event_repository_crud_round_trip(tmp_path) -> None:
    async def scenario() -> None:
        manager = DatabaseSessionManager(f"sqlite+aiosqlite:///{tmp_path / 'repo.db'}")
        await manager.initialize_schema()
        repository = SqlAlchemyEventRepository(manager)

        created = await repository.create(_event())
        listed = await repository.list_events()
        fetched = await repository.get_by_id(created.id)

        updated_entity = Event(
            id=created.id,
            title="Updated Briefing",
            instruction=created.instruction,
            schedule=created.schedule,
            allowed_tools=["web_search", "send_slack"],
            notify_target=created.notify_target,
            status=EventStatus.PAUSED,
            created_at=created.created_at,
            updated_at=datetime(2026, 3, 30, 1, 0, tzinfo=UTC),
            last_run_at=created.last_run_at,
            next_run_at=created.next_run_at,
        )
        updated = await repository.update(updated_entity)
        await repository.delete(created.id)
        deleted = await repository.get_by_id(created.id)

        assert created.id == "1f1e2d3c-4b5a-6789-8abc-def012345678"
        assert len(listed) == 1
        assert fetched is not None
        assert fetched.schedule.days_of_week == [0, 2]
        assert updated.title == "Updated Briefing"
        assert updated.allowed_tools == ["web_search", "send_slack"]
        assert updated.status == EventStatus.PAUSED
        assert deleted is None

        await manager.dispose()

    asyncio.run(scenario())
