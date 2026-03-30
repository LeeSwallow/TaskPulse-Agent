from __future__ import annotations

import grpc

from be.bootstrap import Container
from be.presentation.grpc.services.health_service import HealthGrpcService


class GrpcServer:
    def __init__(self, container: Container, host: str | None = None, port: int | None = None) -> None:
        self._container = container
        self._host = host or container.settings.grpc_host
        self._port = port if port is not None else container.settings.grpc_port
        self._server = grpc.aio.server()
        self._bound_port: int | None = None

        HealthGrpcService.register(self._server, container)

    @property
    def bound_port(self) -> int:
        if self._bound_port is None:
            msg = "gRPC server has not been started"
            raise RuntimeError(msg)
        return self._bound_port

    @property
    def target(self) -> str:
        return f"{self._host}:{self.bound_port}"

    async def start(self) -> None:
        self._bound_port = self._server.add_insecure_port(f"{self._host}:{self._port}")
        if self._bound_port <= 0:
            msg = "failed to bind gRPC server port"
            raise RuntimeError(msg)
        await self._server.start()

    async def stop(self, grace: float = 0) -> None:
        await self._server.stop(grace)
