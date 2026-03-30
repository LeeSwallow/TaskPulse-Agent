from collections.abc import Sequence
from typing import Protocol

from be.domain.entities.execution import ExecutionRecord


class ExecutionRepository(Protocol):
    async def list_executions(self) -> Sequence[ExecutionRecord]: ...
