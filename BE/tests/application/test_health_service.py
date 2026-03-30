from be.application.health.service import HealthService
from be.config import Settings


def test_health_service_returns_ok_status() -> None:
    service = HealthService(Settings())

    result = service.get_status()

    assert result.status == "ok"
