from litestar import Router

from apps.company_structure.controllers.api import route_handlers

router = Router(
    path="/company_structure/api",
    route_handlers=[
        route_handlers.DepartmentHTTPController,
        route_handlers.EmployeeHTTPController,
    ],
)
