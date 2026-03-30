from __future__ import annotations

from be.agents.state import AgentRunState


def plan(state: AgentRunState) -> AgentRunState:
    planned_tools = list(state["event"].allowed_tools)
    return {
        "planned_tools": planned_tools,
        "steps": [*state["steps"], "plan"],
    }
