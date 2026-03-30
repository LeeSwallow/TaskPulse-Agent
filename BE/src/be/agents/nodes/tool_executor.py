from __future__ import annotations

from be.agents.state import AgentRunContext, AgentRunState


async def execute_tools(state: AgentRunState, runtime: AgentRunContext) -> AgentRunState:
    steps = [*state["steps"], "execute_tools"]
    planned_tools = state["planned_tools"]
    tool_registry = runtime.context.tool_registry
    if not planned_tools:
        return {
            "tool_results": [],
            "steps": steps,
        }

    unknown_tools = [name for name in planned_tools if not tool_registry.has_tool(name)]
    if unknown_tools:
        return {
            "tool_results": [],
            "steps": steps,
            "error": f"Unknown tool(s): {', '.join(unknown_tools)}",
        }

    tool_results: list[dict[str, object | None]] = []
    for tool_name in planned_tools:
        try:
            output = await tool_registry.run_tool(tool_name, state["event"].instruction)
        except Exception as exc:
            tool_results.append(
                {
                    "tool": tool_name,
                    "status": "failed",
                    "output": None,
                    "error": str(exc),
                },
            )
            return {
                "tool_results": tool_results,
                "steps": steps,
                "error": str(exc),
            }

        tool_results.append(
            {
                "tool": tool_name,
                "status": "succeeded",
                "output": output,
            },
        )

    return {
        "tool_results": tool_results,
        "steps": steps,
    }
