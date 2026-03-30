from __future__ import annotations

import asyncio

from be.bootstrap import build_container
from be.presentation.grpc.server import GrpcServer


def test_grpc_server_bootstrap_exposes_runtime_target() -> None:
    async def scenario() -> None:
        container = build_container()
        server = GrpcServer(container, host="127.0.0.1", port=0)

        await server.start()
        try:
            assert server.bound_port > 0
            assert server.target == f"127.0.0.1:{server.bound_port}"
        finally:
            await server.stop()
            await container.infrastructure.redis.close()
            await container.infrastructure.database.dispose()

    asyncio.run(scenario())
