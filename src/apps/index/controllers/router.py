from litestar import Router

from apps.index.controllers.http import IndexHTTPController

router = Router(
    path="/",
    route_handlers=[IndexHTTPController],
)
