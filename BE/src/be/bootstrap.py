from dataclasses import dataclass

from be.application.events.service import EventService
from be.application.health.service import HealthService
from be.config import Settings, get_settings
from be.infrastructure.cache.redis_client import RedisClientManager
from be.infrastructure.db.session import DatabaseSessionManager
from be.infrastructure.db.repositories.event_repository import SqlAlchemyEventRepository
from be.observability.logging import configure_structured_logging
from be.observability.metrics import MetricsRegistry


@dataclass
class InfrastructureContainer:
    database: DatabaseSessionManager
    redis: RedisClientManager


@dataclass
class ApplicationContainer:
    health_service: HealthService
    event_service: EventService


@dataclass
class ObservabilityContainer:
    logger: object
    metrics: MetricsRegistry


@dataclass
class Container:
    settings: Settings
    infrastructure: InfrastructureContainer
    application: ApplicationContainer
    observability: ObservabilityContainer


def build_container() -> Container:
    settings = get_settings()
    infrastructure = InfrastructureContainer(
        database=DatabaseSessionManager(settings.database_url),
        redis=RedisClientManager(settings.redis_url),
    )
    event_repository = SqlAlchemyEventRepository(infrastructure.database)
    application = ApplicationContainer(
        health_service=HealthService(settings=settings),
        event_service=EventService(event_repository=event_repository),
    )
    observability = ObservabilityContainer(
        logger=configure_structured_logging(),
        metrics=MetricsRegistry(),
    )
    return Container(
        settings=settings,
        infrastructure=infrastructure,
        application=application,
        observability=observability,
    )
