from __future__ import annotations

import asyncio

import grpc

from be.bootstrap import build_container
from be.presentation.grpc.server import GrpcServer
from proto.taskpulse.v1 import taskpulse_pb2, taskpulse_pb2_grpc


def test_grpc_health_service_returns_ok_status() -> None:
    async def scenario() -> None:
        container = build_container()
        server = GrpcServer(container, host="127.0.0.1", port=0)

        await server.start()
        try:
            async with grpc.aio.insecure_channel(server.target) as channel:
                stub = taskpulse_pb2_grpc.HealthServiceStub(channel)
                response = await stub.Check(taskpulse_pb2.HealthCheckRequest())
        finally:
            await server.stop()
            await container.infrastructure.redis.close()
            await container.infrastructure.database.dispose()

        assert response.status == "ok"
    asyncio.run(scenario())
