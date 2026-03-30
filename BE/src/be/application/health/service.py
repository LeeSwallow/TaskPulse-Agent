from be.config import Settings
from be.domain.health.entities import HealthStatus


class HealthService:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def get_status(self) -> HealthStatus:
        _ = self._settings.app_name
        return HealthStatus(status="ok")
