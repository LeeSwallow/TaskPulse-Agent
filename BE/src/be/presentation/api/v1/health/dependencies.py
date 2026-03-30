from fastapi import Request

from be.application.health.service import HealthService


def get_health_service(request: Request) -> HealthService:
    return request.app.state.container.application.health_service
