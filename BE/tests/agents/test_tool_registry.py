from __future__ import annotations

import asyncio

from be.agents.tool_registry import ToolRegistry


def test_tool_registry_resolves_registered_tool() -> None:
    registry = ToolRegistry()
    registry.register("web_search", lambda instruction: f"ok:{instruction}")

    result = asyncio.run(registry.run_tool("web_search", "ping"))

    assert result == "ok:ping"


def test_tool_registry_lists_registered_tool_names() -> None:
    registry = ToolRegistry()
    registry.register("b", lambda _: "b")
    registry.register("a", lambda _: "a")

    assert registry.list_tools() == ["a", "b"]
