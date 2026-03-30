from __future__ import annotations

import inspect
from collections.abc import Awaitable, Callable
from typing import TypeAlias


ToolCallable: TypeAlias = Callable[[str], object | Awaitable[object]]


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, ToolCallable] = {}

    def register(self, name: str, tool: ToolCallable) -> None:
        self._tools[name] = tool

    def has_tool(self, name: str) -> bool:
        return name in self._tools

    def list_tools(self) -> list[str]:
        return sorted(self._tools)

    async def run_tool(self, name: str, instruction: str) -> object:
        try:
            tool = self._tools[name]
        except KeyError as exc:
            msg = f"Unknown tool: {name}"
            raise ValueError(msg) from exc

        result = tool(instruction)
        if inspect.isawaitable(result):
            return await result
        return result
