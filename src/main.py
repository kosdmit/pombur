from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from dishka import make_async_container
from dishka.integrations import litestar as litestar_integration
from litestar import Litestar
from litestar.contrib.sqlalchemy.plugins import SQLAlchemyInitPlugin
from litestar.openapi import OpenAPIConfig
from litestar.openapi.plugins import SwaggerRenderPlugin

import config
import litestar_utils
import logs
from apps.company_structure import (
    company_structure_router,
    ioc,
)

container = make_async_container(
    ioc.InfrastructureProvider(),
    ioc.LitestarRepositoryProvider(),
    ioc.AppProvider(),
    litestar_integration.LitestarProvider(),
)


@asynccontextmanager
async def app_lifespan(app: Litestar) -> AsyncGenerator[None]:
    yield
    await app.state.dishka_container.close()


def get_app() -> Litestar:
    litestar_app = Litestar(
        route_handlers=[company_structure_router],
        on_startup=[logs.log_on_startup],
        openapi_config=OpenAPIConfig(
            title="Pombur project",
            version="0.1.0",
            render_plugins=[SwaggerRenderPlugin()],
            path="/docs",
        ),
        lifespan=[app_lifespan],
        middleware=[config.rate_limit_config.middleware],
        plugins=[SQLAlchemyInitPlugin(config.db_config)],
        cors_config=config.cors_config,
        csrf_config=config.csrf_config,
        allowed_hosts=config.allowed_hosts,
        compression_config=config.compression_config,
        dependencies={"limit_offset": litestar_utils.provide_limit_offset_pagination},
        debug=config.service_config.debug,
    )

    litestar_integration.setup_dishka(container, litestar_app)

    return litestar_app
