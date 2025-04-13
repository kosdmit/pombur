from litestar import Router

from apps.company_structure.controllers.http import DepartmentHTTPController, EmployeeHTTPController

router = Router(
    path="/company_structure",
    route_handlers=[DepartmentHTTPController, EmployeeHTTPController],
)
