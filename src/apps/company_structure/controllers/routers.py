from litestar import Router

from apps.company_structure.controllers import http, web_interface

api_router = Router(
    path="/company_structure/api",
    route_handlers=[
        http.DepartmentHTTPController,
        http.EmployeeHTTPController,
    ],
)


templates_router = Router(
    path="/company_structure",
    route_handlers=[
        web_interface.IndexHTTPController,
        web_interface.OrgChartController,
        web_interface.CreateDepartmentController,
    ],
)
