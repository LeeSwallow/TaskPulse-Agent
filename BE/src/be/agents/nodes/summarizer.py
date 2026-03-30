from __future__ import annotations

from be.agents.state import AgentRunState
from be.domain.entities.execution import ExecutionStatus


def summarize(state: AgentRunState) -> AgentRunState:
    steps = [*state["steps"], "summarize"]
    tool_results = state["tool_results"]
    error = state.get("error")

    if error:
        if tool_results:
            summary = f"Execution failed after {len(tool_results)} tool(s)"
        else:
            summary = "Execution failed before tool execution"
        status = ExecutionStatus.FAILED
    elif not tool_results:
        summary = "No tools executed"
        status = ExecutionStatus.SUCCEEDED
    else:
        tool_names = ", ".join(str(item["tool"]) for item in tool_results)
        summary = f"Executed {len(tool_results)} tool(s): {tool_names}"
        status = ExecutionStatus.SUCCEEDED

    return {
        "summary": summary,
        "status": status,
        "steps": steps,
    }
