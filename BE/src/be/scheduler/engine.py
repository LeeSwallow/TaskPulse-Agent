from __future__ import annotations

from datetime import datetime

from be.domain.events.entities import Event, EventStatus
from be.observability.metrics import MetricsRegistry


def is_event_due(event: Event, *, now: datetime) -> bool:
    if event.status == EventStatus.PAUSED:
        return False
    if event.next_run_at is None:
        return False
    return event.next_run_at <= now


def collect_due_events(events: list[Event], *, now: datetime, metrics: MetricsRegistry | None = None) -> list[Event]:
    due_events = [event for event in events if is_event_due(event, now=now)]
    if metrics is not None:
        metrics.increment("scheduler_ticks_total")
        for _ in due_events:
            metrics.increment("scheduler_due_events_total")
    return due_events
