from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class CounterMetric:
    name: str
    values: dict[tuple[tuple[str, str], ...], int] = field(default_factory=dict)

    def increment(self, **labels: str) -> None:
        key = tuple(sorted((key, value) for key, value in labels.items()))
        self.values[key] = self.values.get(key, 0) + 1

    def snapshot(self) -> list[dict[str, object]]:
        if not self.values:
            return [{"labels": {}, "value": 0}]
        return [
            {"labels": dict(key), "value": value}
            for key, value in sorted(self.values.items())
        ]


class MetricsRegistry:
    def __init__(self) -> None:
        self._metrics: dict[str, CounterMetric] = {
            "scheduler_ticks_total": CounterMetric("scheduler_ticks_total"),
            "scheduler_due_events_total": CounterMetric("scheduler_due_events_total"),
            "agent_execution_succeeded_total": CounterMetric("agent_execution_succeeded_total"),
            "agent_execution_failed_total": CounterMetric("agent_execution_failed_total"),
            "grpc_requests_total": CounterMetric("grpc_requests_total"),
        }

    def increment(self, name: str, **labels: str) -> None:
        self._metrics[name].increment(**labels)

    def snapshot(self) -> dict[str, list[dict[str, object]]]:
        return {name: metric.snapshot() for name, metric in self._metrics.items()}
