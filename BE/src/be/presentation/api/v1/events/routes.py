from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status

from be.application.events.service import EventService
from be.presentation.api.v1.events.dependencies import get_event_service
from be.presentation.api.v1.events.schemas import EventCreateRequest, EventResponse, EventUpdateRequest

router = APIRouter(prefix="/api/events", tags=["events"])


@router.get("", response_model=list[EventResponse])
async def list_events(
    event_service: Annotated[EventService, Depends(get_event_service)],
) -> list[EventResponse]:
    events = await event_service.list_events()
    return [EventResponse.model_validate(event) for event in events]


@router.post("", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
async def create_event(
    payload: EventCreateRequest,
    event_service: Annotated[EventService, Depends(get_event_service)],
) -> EventResponse:
    event = await event_service.create_event(payload.to_input())
    return EventResponse.model_validate(event)


@router.patch("/{event_id}", response_model=EventResponse)
async def update_event(
    event_id: str,
    payload: EventUpdateRequest,
    event_service: Annotated[EventService, Depends(get_event_service)],
) -> EventResponse:
    event = await event_service.update_event(event_id, payload.to_input())
    if event is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    return EventResponse.model_validate(event)


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(
    event_id: str,
    event_service: Annotated[EventService, Depends(get_event_service)],
) -> Response:
    deleted = await event_service.delete_event(event_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
