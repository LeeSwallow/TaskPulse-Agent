from fastapi import Request

from be.application.events.service import EventService


def get_event_service(request: Request) -> EventService:
    return request.app.state.container.application.event_service
