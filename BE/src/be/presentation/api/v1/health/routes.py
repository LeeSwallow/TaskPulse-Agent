from typing import Annotated

from fastapi import APIRouter, Depends

from be.application.health.service import HealthService
from be.presentation.api.v1.health.dependencies import get_health_service
from be.presentation.api.v1.health.schemas import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health(
    health_service: Annotated[HealthService, Depends(get_health_service)],
) -> HealthResponse:
    status = health_service.get_status()
    return HealthResponse(status=status.status)
