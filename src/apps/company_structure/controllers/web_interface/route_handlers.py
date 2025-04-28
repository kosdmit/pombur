import uuid
from datetime import UTC, datetime
from typing import Literal

from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import Controller, delete, get, post, status_codes
from litestar.dto import DTOData
from litestar.response import Template
from litestar_htmx import HTMXTemplate

from apps.company_structure.application import schemas, use_cases
from apps.company_structure.controllers import dtos
from apps.company_structure.controllers.web_interface import context_schemas
from apps.company_structure.domain import aggregates
from common.controllers import context_schemas as common_context_schemas

_CONTEXT_MODEL_SERIALIZATION_MODE: Literal["json", "python"] = "json"


class IndexHTTPController(Controller):
    path = "/"

    @get(name="company_structure.index")
    @inject
    async def get_page(
        self,
        use_case: FromDishka[use_cases.GenericGetListUseCase[aggregates.DepartmentTreeAggregate]],
    ) -> Template:
        context = context_schemas.IndexPageContext(
            page_title="Home",
            page_description="Index page description",
            page_keywords="Index page keywords",
            breadcrumbs=[
                common_context_schemas.BreadcrumbItem(name="Home", url="/"),
                common_context_schemas.BreadcrumbItem(
                    name="Company Structure",
                    url="/company_structure",
                    is_active=True,
                ),
            ],
            tree_list=await use_case.get_list(),
        )

        return Template(
            template_name="company_structure/index.html.jinja",
            context=context.model_dump(),
        )


class OrgChartController(Controller):
    @get(path="/org-chart/{root_id:uuid}", name="company_structure.org_chart")
    @inject
    async def get_org_chart(
        self,
        root_id: uuid.UUID,
        use_case: FromDishka[use_cases.GetDepartmentTreeAsListUseCase],
    ) -> HTMXTemplate:
        department_list = await use_case.get_one_as_list(root_id)
        context = context_schemas.OrgChartComponentContext(
            department_list=[
                context_schemas.OrgChartDepartmentNodeSchema(**department.model_dump())
                for department in department_list
            ]
        )
        return HTMXTemplate(
            template_name="company_structure/htmx/org-chart.html.jinja",
            context=context.model_dump(mode=_CONTEXT_MODEL_SERIALIZATION_MODE),
        )


class CreateDepartmentController(Controller):
    @get(
        path="departments/{department_id:uuid}/create_modal",
        name="company_structure.create_department_modal",
    )
    @inject
    async def get_create_department_modal(
        self,
        department_id: uuid.UUID,
        get_department_use_case: FromDishka[
            use_cases.GenericGetUseCase[uuid.UUID, schemas.DepartmentSchema]
        ],
        get_departments_use_case: FromDishka[use_cases.GetDepartmentTreeAsListUseCase],
    ) -> HTMXTemplate:
        context = context_schemas.CreateDepartmentModalContext(
            selected_parent_department=await get_department_use_case.get(department_id),
            department_list=await get_departments_use_case.get_one_as_list(department_id),
        )
        return HTMXTemplate(
            template_name="company_structure/htmx/create_department_modal.html.jinja",
            context=context.model_dump(mode=_CONTEXT_MODEL_SERIALIZATION_MODE),
        )

    @post(
        path="/departments",
        name="htmx.company_structure.create_department",
        dto=dtos.WriteDepartmentDTO,
    )
    @inject
    async def create_department(
        self,
        use_case: FromDishka[use_cases.GenericCreateUseCase[schemas.DepartmentSchema]],
        data: DTOData[schemas.DepartmentSchema],
    ) -> HTMXTemplate:
        created_department = await use_case.create(data)
        context = context_schemas.ResultToastContext(
            status="success",
            timestamp=datetime.now(tz=UTC),
            message="Department created successfully",
            details={"created_department": str(created_department)},
        )

        return HTMXTemplate(
            template_name="company_structure/htmx/toast.html.jinja",
            context=context.model_dump(mode=_CONTEXT_MODEL_SERIALIZATION_MODE),
        )


class DeleteDepartmentController(Controller):
    @get(
        path="/departments/{department_id:uuid}/delete_modal",
        name="htmx.company_structure.delete_modal",
    )
    @inject
    async def get_delete_modal(
        self,
        department_id: uuid.UUID,
        use_case: FromDishka[use_cases.GenericGetUseCase[uuid.UUID, schemas.DepartmentSchema]],
    ) -> HTMXTemplate:
        context = context_schemas.DeleteDepartmentModalContext(
            department_to_delete=await use_case.get(department_id),
        )
        return HTMXTemplate(
            template_name="company_structure/htmx/delete_department_modal.html.jinja",
            context=context.model_dump(mode="json"),
        )

    @delete(
        path="/departments/{department_id:uuid}",
        name="htmx.company_structure.delete_department",
        status_code=status_codes.HTTP_200_OK,
    )
    @inject
    async def delete_department(
        self,
        use_case: FromDishka[use_cases.GenericDeleteUseCase[uuid.UUID, schemas.DepartmentSchema]],
        department_id: uuid.UUID,
    ) -> HTMXTemplate:
        await use_case.delete(department_id)

        context = context_schemas.ResultToastContext(
            status="success",
            timestamp=datetime.now(tz=UTC),
            message="Department deleted successfully",
            details={"deleted_department_id": str(department_id)},
        )
        return HTMXTemplate(
            template_name="company_structure/htmx/toast.html.jinja",
            context=context.model_dump(mode=_CONTEXT_MODEL_SERIALIZATION_MODE),
        )
