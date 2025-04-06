from dishka import make_async_container
from litestar import Litestar
from litestar.openapi import OpenAPIConfig
from litestar.openapi.plugins import SwaggerRenderPlugin

from apps.company_structure.controllers.http import DepartmentHTTPController

from dishka.integrations import litestar as litestar_integration

from apps.company_structure.infrastructure.configs import AppConfig
from apps.company_structure.ioc import AppProvider, InfrastructureProvider

config = AppConfig()
container = make_async_container(
    InfrastructureProvider(),
    AppProvider(),
    context={AppConfig: config},
)


def get_app() -> Litestar:
    litestar_app = Litestar(
        route_handlers=[DepartmentHTTPController],
        openapi_config=OpenAPIConfig(
            title="Pombur project",
            version="0.1.0",
            render_plugins=[SwaggerRenderPlugin()],
            path="/docs",
        ),
    )

    litestar_integration.setup_dishka(container, litestar_app)

    return litestar_app
