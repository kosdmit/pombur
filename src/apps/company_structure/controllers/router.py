from litestar import Router

from apps.company_structure.controllers import http, web_interface

router = Router(
    path="/company_structure",
    route_handlers=[
        web_interface.IndexHTTPController,
        http.DepartmentHTTPController,
        http.EmployeeHTTPController,
    ],
)
