from __future__ import annotations

import grpc

from be.bootstrap import Container
from proto.taskpulse.v1 import taskpulse_pb2, taskpulse_pb2_grpc


class HealthGrpcService(taskpulse_pb2_grpc.HealthServiceServicer):
    def __init__(self, container: Container) -> None:
        self._container = container

    async def Check(
        self,
        request: taskpulse_pb2.HealthCheckRequest,
        context: grpc.aio.ServicerContext,
    ) -> taskpulse_pb2.HealthCheckResponse:
        _ = request, context
        self._container.observability.metrics.increment(
            "grpc_requests_total",
            service="HealthService",
            method="Check",
        )
        status = self._container.application.health_service.get_status()
        return taskpulse_pb2.HealthCheckResponse(status=status.status)

    @classmethod
    def register(cls, server: grpc.aio.Server, container: Container) -> None:
        taskpulse_pb2_grpc.add_HealthServiceServicer_to_server(cls(container), server)
