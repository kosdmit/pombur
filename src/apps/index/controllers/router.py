from litestar import Router

from apps.index.controllers import web_interface

router = Router(
    path="/",
    route_handlers=[web_interface.IndexHTTPController],
)
