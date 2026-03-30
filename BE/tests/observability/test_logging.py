from __future__ import annotations

import json
import logging

from be.observability.logging import JsonLogFormatter


def test_json_log_formatter_emits_structured_log_with_correlation_fields() -> None:
    formatter = JsonLogFormatter()
    record = logging.LogRecord(
        name="taskpulse",
        level=logging.INFO,
        pathname=__file__,
        lineno=10,
        msg="execution completed",
        args=(),
        exc_info=None,
    )
    record.event_id = "event-1"
    record.execution_id = "exec-1"
    record.status = "succeeded"
    record.tool_name = "web_search"

    payload = json.loads(formatter.format(record))

    assert payload["message"] == "execution completed"
    assert payload["event_id"] == "event-1"
    assert payload["execution_id"] == "exec-1"
    assert payload["status"] == "succeeded"
    assert payload["tool_name"] == "web_search"
    assert payload["level"] == "INFO"
