from redis.asyncio import Redis


class RedisClientManager:
    def __init__(self, redis_url: str) -> None:
        self._client = Redis.from_url(redis_url, decode_responses=True)

    @property
    def client(self) -> Redis:
        return self._client

    async def close(self) -> None:
        await self._client.aclose()
