from be.observability.metrics import MetricsRegistry


def test_metrics_registry_registers_expected_metric_names() -> None:
    registry = MetricsRegistry()

    assert sorted(registry.snapshot()) == [
        "agent_execution_failed_total",
        "agent_execution_succeeded_total",
        "grpc_requests_total",
        "scheduler_due_events_total",
        "scheduler_ticks_total",
    ]


def test_metrics_registry_counter_increments_with_labels() -> None:
    registry = MetricsRegistry()

    registry.increment("grpc_requests_total", service="HealthService", method="Check")
    registry.increment("grpc_requests_total", service="HealthService", method="Check")

    snapshot = registry.snapshot()

    assert snapshot["grpc_requests_total"][0]["value"] == 2
    assert snapshot["grpc_requests_total"][0]["labels"] == {
        "service": "HealthService",
        "method": "Check",
    }
