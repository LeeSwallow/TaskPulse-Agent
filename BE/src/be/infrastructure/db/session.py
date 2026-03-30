from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from be.infrastructure.db.base import Base
from be.infrastructure.db.models import EventModel, ExecutionRecordModel


class DatabaseSessionManager:
    def __init__(self, database_url: str) -> None:
        self._engine: AsyncEngine = create_async_engine(
            database_url,
            future=True,
            pool_pre_ping=True,
        )
        self._session_factory = async_sessionmaker(
            bind=self._engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    @property
    def engine(self) -> AsyncEngine:
        return self._engine

    async def session(self) -> AsyncIterator[AsyncSession]:
        async with self._session_factory() as session:
            yield session

    async def dispose(self) -> None:
        await self._engine.dispose()

    async def initialize_schema(self) -> None:
        async with self._engine.begin() as connection:
            await connection.run_sync(
                Base.metadata.create_all,
                tables=[
                    EventModel.__table__,
                    ExecutionRecordModel.__table__,
                ],
            )
