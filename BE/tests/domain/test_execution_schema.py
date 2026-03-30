from datetime import UTC, datetime

from be.presentation.api.v1.executions.schemas import ExecutionRecordResponse


def test_execution_record_schema_defaults_and_fields() -> None:
    now = datetime.now(UTC)

    execution = ExecutionRecordResponse(
        id="execution-1",
        event_id="event-1",
        status="running",
        started_at=now,
        finished_at=None,
        summary="",
        steps=["planned"],
        tool_results=[],
        error=None,
    )

    assert execution.event_id == "event-1"
    assert execution.status == "running"
    assert execution.steps == ["planned"]
