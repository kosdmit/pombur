from datetime import UTC, datetime
from typing import Any

from litestar import Request
from litestar_htmx import HTMXTemplate

from apps.company_structure.controllers.web_interface import context_schemas
from apps.company_structure.domain import exceptions as domain_exceptions


def forbidden_delete_department_handler(
    request: Request[Any, Any, Any],
    exception: domain_exceptions.ForbiddenDeleteDepartmentError,
) -> HTMXTemplate:
    context = context_schemas.ResultToastContext(
        status="error",
        timestamp=datetime.now(tz=UTC),
        message="Failed to delete department",
        details={
            "exception": str(exception),
            "department_id": str(request.path_params["department_id"]),
        },
    )
    return HTMXTemplate(
        template_name="company_structure/htmx/toast.html.jinja",
        context=context.model_dump(mode="json"),
    )
