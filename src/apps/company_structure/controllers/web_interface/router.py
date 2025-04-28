from litestar import Router

from apps.company_structure.controllers.web_interface import exception_handlers, route_handlers
from apps.company_structure.domain import exceptions as domain_exceptions

router = Router(
    path="/company_structure",
    route_handlers=[
        route_handlers.IndexHTTPController,
        route_handlers.OrgChartController,
        route_handlers.CreateDepartmentController,
        route_handlers.DeleteDepartmentController,
    ],
    exception_handlers={
        domain_exceptions.ForbiddenDeleteDepartmentWithChildrenError: exception_handlers.forbidden_delete_department_handler,  # noqa: E501
    },
)
