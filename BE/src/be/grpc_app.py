from __future__ import annotations

import asyncio

from be.bootstrap import build_container
from be.presentation.grpc.server import GrpcServer


async def serve() -> None:
    container = build_container()
    server = GrpcServer(container)
    await server.start()
    try:
        await asyncio.Future()
    finally:
        await server.stop()
        await container.infrastructure.redis.close()
        await container.infrastructure.database.dispose()


def main() -> None:
    asyncio.run(serve())
