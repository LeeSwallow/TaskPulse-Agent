from __future__ import annotations

import asyncio

from be.agents.graph import AgentRunner
from be.agents.tool_registry import ToolRegistry
from be.domain.entities.execution import ExecutionStatus
from be.domain.events.entities import Event, EventStatus, NotifyTarget, Schedule, ScheduleType


def _event(*, allowed_tools: list[str]) -> Event:
    from datetime import UTC, datetime

    now = datetime(2026, 3, 30, 0, 0, tzinfo=UTC)
    return Event(
        id="event-1",
        title="Morning Briefing",
        instruction="Summarize the top news",
        schedule=Schedule(type=ScheduleType.DAILY, timezone="UTC", time_of_day="09:00"),
        allowed_tools=allowed_tools,
        notify_target=NotifyTarget.DASHBOARD,
        status=EventStatus.ACTIVE,
        created_at=now,
        updated_at=now,
        last_run_at=None,
        next_run_at=None,
    )


def test_runner_executes_only_allowlisted_tools() -> None:
    executed: list[str] = []
    registry = ToolRegistry()
    registry.register("web_search", lambda instruction: executed.append(f"web:{instruction}") or "news result")
    registry.register("send_slack", lambda instruction: executed.append(f"slack:{instruction}") or "sent")
    runner = AgentRunner(registry=registry)

    result = asyncio.run(runner.run(_event(allowed_tools=["web_search"])))

    assert result.status == ExecutionStatus.SUCCEEDED
    assert executed == ["web:Summarize the top news"]
    assert [item["tool"] for item in result.tool_results] == ["web_search"]


def test_runner_returns_summary_and_tool_log() -> None:
    registry = ToolRegistry()
    registry.register("web_search", lambda instruction: f"search:{instruction}")
    registry.register("calendar", lambda instruction: f"calendar:{instruction}")
    runner = AgentRunner(registry=registry)

    result = asyncio.run(runner.run(_event(allowed_tools=["web_search", "calendar"])))

    assert result.status == ExecutionStatus.SUCCEEDED
    assert result.summary == "Executed 2 tool(s): web_search, calendar"
    assert result.steps == ["plan", "execute_tools", "summarize"]
    assert result.tool_results == [
        {"tool": "web_search", "status": "succeeded", "output": "search:Summarize the top news"},
        {"tool": "calendar", "status": "succeeded", "output": "calendar:Summarize the top news"},
    ]


def test_runner_fails_when_allowed_tool_is_unknown() -> None:
    runner = AgentRunner(registry=ToolRegistry())

    result = asyncio.run(runner.run(_event(allowed_tools=["unknown_tool"])))

    assert result.status == ExecutionStatus.FAILED
    assert result.error == "Unknown tool(s): unknown_tool"
    assert result.tool_results == []


def test_runner_propagates_tool_failure() -> None:
    def boom(_: str) -> str:
        raise RuntimeError("tool exploded")

    registry = ToolRegistry()
    registry.register("web_search", boom)
    runner = AgentRunner(registry=registry)

    result = asyncio.run(runner.run(_event(allowed_tools=["web_search"])))

    assert result.status == ExecutionStatus.FAILED
    assert result.error == "tool exploded"
    assert result.tool_results == [
        {"tool": "web_search", "status": "failed", "output": None, "error": "tool exploded"},
    ]


def test_runner_handles_empty_allowlist() -> None:
    runner = AgentRunner(registry=ToolRegistry())

    result = asyncio.run(runner.run(_event(allowed_tools=[])))

    assert result.status == ExecutionStatus.SUCCEEDED
    assert result.summary == "No tools executed"
    assert result.tool_results == []
