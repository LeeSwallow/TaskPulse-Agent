from __future__ import annotations

from dataclasses import dataclass
from typing import Any, TypedDict

from be.agents.tool_registry import ToolRegistry
from be.domain.entities.execution import ExecutionStatus
from be.domain.events.entities import Event


class AgentRunState(TypedDict, total=False):
    event: Event
    planned_tools: list[str]
    tool_results: list[dict[str, Any]]
    summary: str
    status: ExecutionStatus
    error: str | None
    steps: list[str]


@dataclass(frozen=True)
class AgentRunContext:
    tool_registry: ToolRegistry
