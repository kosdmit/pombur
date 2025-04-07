from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from dishka import make_async_container
from dishka.integrations import litestar as litestar_integration
from litestar import Litestar
from litestar.openapi import OpenAPIConfig
from litestar.openapi.plugins import SwaggerRenderPlugin

from apps.company_structure.controllers.router import company_structure_router
from apps.company_structure.infrastructure.configs import AppConfig
from apps.company_structure.ioc import AppProvider, InfrastructureProvider

config = AppConfig()
container = make_async_container(
    InfrastructureProvider(),
    AppProvider(),
    litestar_integration.LitestarProvider(),
    context={AppConfig: config},
)


@asynccontextmanager
async def app_lifespan(app: Litestar) -> AsyncGenerator[None]:
    yield
    await app.state.dishka_container.close()


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
    )

    litestar_integration.setup_dishka(container, litestar_app)

    return litestar_app
