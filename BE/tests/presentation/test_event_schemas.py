from datetime import UTC, datetime

from be.domain.events.entities import EventStatus, NotifyTarget, ScheduleType
from be.presentation.api.v1.events.schemas import EventCreateRequest, EventUpdateRequest, ScheduleDefinition


def test_event_create_request_converts_to_application_input() -> None:
    payload = EventCreateRequest(
        title="Morning Briefing",
        instruction="Summarize news",
        schedule=ScheduleDefinition(
            type=ScheduleType.DAILY,
            timezone="Asia/Seoul",
            time_of_day="09:00",
        ),
        allowed_tools=["web_search"],
        notify_target=NotifyTarget.DASHBOARD,
    )

    dto = payload.to_input()

    assert dto.title == "Morning Briefing"
    assert dto.schedule.type == ScheduleType.DAILY
    assert dto.schedule.time_of_day == "09:00"


def test_event_update_request_converts_optional_fields() -> None:
    run_at = datetime(2026, 3, 31, 9, 0, tzinfo=UTC)
    payload = EventUpdateRequest(
        status=EventStatus.PAUSED,
        schedule=ScheduleDefinition(
            type=ScheduleType.ONCE,
            timezone="UTC",
            run_at=run_at,
        ),
    )

    dto = payload.to_input()

    assert dto.status == EventStatus.PAUSED
    assert dto.schedule is not None
    assert dto.schedule.run_at == run_at
