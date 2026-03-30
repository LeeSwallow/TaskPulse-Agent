from __future__ import annotations

import asyncio
from sqlalchemy import inspect

from be.infrastructure.db.session import DatabaseSessionManager


def test_initialize_schema_creates_event_and_execution_tables(tmp_path) -> None:
    async def scenario() -> None:
        manager = DatabaseSessionManager(f"sqlite+aiosqlite:///{tmp_path / 'schema.db'}")

        await manager.initialize_schema()

        async with manager.engine.begin() as connection:
            table_names = await connection.run_sync(lambda sync_conn: inspect(sync_conn).get_table_names())

        assert "events" in table_names
        assert "execution_records" in table_names

        await manager.dispose()

    asyncio.run(scenario())
