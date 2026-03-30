from contextlib import asynccontextmanager

from fastapi import FastAPI

from be.bootstrap import build_container
from be.presentation.api.router import api_router


def create_app() -> FastAPI:
    container = build_container()

    @asynccontextmanager
    async def lifespan(_: FastAPI):
        await container.infrastructure.database.initialize_schema()
        yield
        await container.infrastructure.database.dispose()
        await container.infrastructure.redis.close()

    app = FastAPI(title=container.settings.app_name, lifespan=lifespan)
    app.state.container = container
    app.include_router(api_router)

    return app


app = create_app()
