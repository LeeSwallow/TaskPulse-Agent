from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from langgraph.graph import END, START, StateGraph

from be.agents.nodes.planner import plan
from be.agents.nodes.summarizer import summarize
from be.agents.nodes.tool_executor import execute_tools
from be.agents.state import AgentRunContext, AgentRunState
from be.agents.tool_registry import ToolRegistry
from be.domain.entities.execution import ExecutionRecord, ExecutionStatus
from be.domain.events.entities import Event
from be.observability.metrics import MetricsRegistry


class AgentRunner:
    def __init__(self, registry: ToolRegistry, metrics: MetricsRegistry | None = None) -> None:
        self._registry = registry
        self._metrics = metrics
        self._graph = self._build_graph()

    async def run(self, event: Event) -> ExecutionRecord:
        started_at = datetime.now(UTC)
        state = await self._graph.ainvoke(
            {
                "event": event,
                "planned_tools": [],
                "tool_results": [],
                "summary": "",
                "status": ExecutionStatus.PENDING,
                "error": None,
                "steps": [],
            },
            context=AgentRunContext(tool_registry=self._registry),
        )
        finished_at = datetime.now(UTC)
        metric_name = (
            "agent_execution_succeeded_total"
            if state["status"] == ExecutionStatus.SUCCEEDED
            else "agent_execution_failed_total"
        )
        if self._metrics is not None:
            self._metrics.increment(metric_name)

        return ExecutionRecord(
            id=str(uuid4()),
            event_id=event.id,
            status=state["status"],
            started_at=started_at,
            finished_at=finished_at,
            summary=state["summary"],
            steps=state["steps"],
            tool_results=state["tool_results"],
            error=state.get("error"),
        )

    def _build_graph(self):
        graph = StateGraph(AgentRunState, context_schema=AgentRunContext)
        graph.add_node("plan", plan)
        graph.add_node("execute_tools", execute_tools)
        graph.add_node("summarize", summarize)
        graph.add_edge(START, "plan")
        graph.add_edge("plan", "execute_tools")
        graph.add_edge("execute_tools", "summarize")
        graph.add_edge("summarize", END)
        return graph.compile()
