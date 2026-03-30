from fastapi import APIRouter

from be.presentation.api.v1.events.routes import router as events_router
from be.presentation.api.v1.health.routes import router as health_router

router = APIRouter()
router.include_router(health_router)
router.include_router(events_router)
