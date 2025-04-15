from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from dishka.integrations import litestar as litestar_integration
from litestar import Litestar
from litestar.contrib.sqlalchemy.plugins import SQLAlchemyInitPlugin
from litestar.static_files import create_static_files_router

import config
import litestar_utils
import logs
from apps import company_structure, index
from ioc import container


@asynccontextmanager
async def app_lifespan(app: Litestar) -> AsyncGenerator[None]:
    yield
    await app.state.dishka_container.close()


def get_app() -> Litestar:
    litestar_app = Litestar(
        route_handlers=[
            index.router,
            company_structure.router,
            create_static_files_router(path="/", directories=["static"]),
        ],
        on_startup=[logs.log_on_startup],
        openapi_config=config.openapi_config,
        lifespan=[app_lifespan],
        middleware=[config.rate_limit_config.middleware],
        plugins=[SQLAlchemyInitPlugin(config.db_config)],
        cors_config=config.cors_config,
        csrf_config=config.csrf_config,
        allowed_hosts=config.allowed_hosts_config,
        compression_config=config.compression_config,
        dependencies={"limit_offset": litestar_utils.provide_limit_offset_pagination},
        debug=config.service_config.debug,
        template_config=config.template_config,
    )

    litestar_integration.setup_dishka(container, litestar_app)

    return litestar_app
