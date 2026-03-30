from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock

import be.infrastructure.cache.redis_client as redis_client_module
from be.infrastructure.cache.redis_client import RedisClientManager


def test_redis_client_manager_builds_client_from_url(monkeypatch) -> None:
    fake_client = object()

    class FakeRedis:
        @staticmethod
        def from_url(redis_url: str, *, decode_responses: bool):
            assert redis_url == "redis://localhost:6379/0"
            assert decode_responses is True
            return fake_client

    monkeypatch.setattr(redis_client_module, "Redis", FakeRedis)

    manager = RedisClientManager("redis://localhost:6379/0")

    assert manager.client is fake_client


def test_redis_client_manager_closes_underlying_client(monkeypatch) -> None:
    async def scenario() -> None:
        fake_client = AsyncMock()

        class FakeRedis:
            @staticmethod
            def from_url(redis_url: str, *, decode_responses: bool):
                assert redis_url == "redis://localhost:6379/0"
                assert decode_responses is True
                return fake_client

        monkeypatch.setattr(redis_client_module, "Redis", FakeRedis)

        manager = RedisClientManager("redis://localhost:6379/0")
        await manager.close()

        fake_client.aclose.assert_awaited_once()

    asyncio.run(scenario())
