from __future__ import annotations

import asyncio

from be.agents.graph import AgentRunner
from be.agents.tool_registry import ToolRegistry
from be.bootstrap import build_container
from be.domain.entities.execution import ExecutionStatus
from be.domain.events.entities import Event, EventStatus, NotifyTarget, Schedule, ScheduleType
from be.observability.metrics import MetricsRegistry
from be.presentation.grpc.server import GrpcServer
from be.scheduler.engine import collect_due_events
from proto.taskpulse.v1 import taskpulse_pb2, taskpulse_pb2_grpc


def _event(*, next_run_at=None) -> Event:
    from datetime import UTC, datetime

    now = datetime(2026, 3, 30, 0, 0, tzinfo=UTC)
    return Event(
        id="event-1",
        title="Morning Briefing",
        instruction="Summarize the top news",
        schedule=Schedule(type=ScheduleType.DAILY, timezone="UTC", time_of_day="09:00"),
        allowed_tools=["web_search"],
        notify_target=NotifyTarget.DASHBOARD,
        status=EventStatus.ACTIVE,
        created_at=now,
        updated_at=now,
        last_run_at=None,
        next_run_at=next_run_at,
    )


def test_instrumentation_smoke_for_scheduler_agent_and_grpc() -> None:
    async def scenario() -> None:
        metrics = MetricsRegistry()

        due_events = collect_due_events(
            [_event(next_run_at=__import__("datetime").datetime(2026, 3, 30, 8, 0, tzinfo=__import__("datetime").UTC))],
            now=__import__("datetime").datetime(2026, 3, 30, 8, 0, tzinfo=__import__("datetime").UTC),
            metrics=metrics,
        )
        assert len(due_events) == 1

        registry = ToolRegistry()
        registry.register("web_search", lambda instruction: f"search:{instruction}")
        runner = AgentRunner(registry=registry, metrics=metrics)
        execution = await runner.run(_event())
        assert execution.status == ExecutionStatus.SUCCEEDED

        container = build_container()
        container.observability.metrics = metrics
        server = GrpcServer(container, host="127.0.0.1", port=0)
        await server.start()
        try:
            import grpc

            async with grpc.aio.insecure_channel(server.target) as channel:
                stub = taskpulse_pb2_grpc.HealthServiceStub(channel)
                response = await stub.Check(taskpulse_pb2.HealthCheckRequest())
        finally:
            await server.stop()
            await container.infrastructure.redis.close()
            await container.infrastructure.database.dispose()

        assert response.status == "ok"
        snapshot = metrics.snapshot()
        assert snapshot["scheduler_ticks_total"][0]["value"] == 1
        assert snapshot["scheduler_due_events_total"][0]["value"] == 1
        assert snapshot["agent_execution_succeeded_total"][0]["value"] == 1
        assert snapshot["grpc_requests_total"][0]["value"] == 1

    asyncio.run(scenario())
