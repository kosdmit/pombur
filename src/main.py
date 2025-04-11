from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from dishka import make_async_container
from dishka.integrations import litestar as litestar_integration
from litestar import Litestar
from litestar.contrib.sqlalchemy.plugins import SQLAlchemyAsyncConfig, SQLAlchemyInitPlugin
from litestar.openapi import OpenAPIConfig
from litestar.openapi.plugins import SwaggerRenderPlugin

from apps.company_structure.controllers.router import company_structure_router
from apps.company_structure.infrastructure.configs import AppConfig
from apps.company_structure.infrastructure.models import Base
from apps.company_structure.ioc import (
    AppProvider,
    InfrastructureProvider,
    LitestarRepositoryProvider,
)

config = AppConfig()
container = make_async_container(
    InfrastructureProvider(),
    LitestarRepositoryProvider(),
    AppProvider(),
    litestar_integration.LitestarProvider(),
)


@asynccontextmanager
async def app_lifespan(app: Litestar) -> AsyncGenerator[None]:
    yield
    await app.state.dishka_container.close()


litestar_db_config = SQLAlchemyAsyncConfig(
    connection_string=config.postgres.uri,
    metadata=Base.metadata,
    create_all=True,
)


def get_app() -> Litestar:
    litestar_app = Litestar(
        route_handlers=[company_structure_router],
        openapi_config=OpenAPIConfig(
            title="Pombur project",
            version="0.1.0",
            render_plugins=[SwaggerRenderPlugin()],
            path="/docs",
        ),
        lifespan=[app_lifespan],
        plugins=[SQLAlchemyInitPlugin(litestar_db_config)],
    )

    litestar_integration.setup_dishka(container, litestar_app)

    return litestar_app
