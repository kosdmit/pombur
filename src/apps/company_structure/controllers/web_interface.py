import uuid
from datetime import UTC, datetime
from typing import Literal

import pydantic
from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import Controller, get, post
from litestar.dto import DTOData
from litestar.response import Template
from litestar_htmx import HTMXTemplate

from apps.company_structure.application import schemas, use_cases
from apps.company_structure.controllers import dtos
from apps.company_structure.domain import aggregates
from common.controllers import web_interface


class IndexPageContext(
    web_interface.HeadPageMetaContext,
    web_interface.BreadcrumbsContext,
    pydantic.BaseModel,
):
    """Index page context.

    Contains the data that is passed to the template as context.
    """

    tree_list: list[aggregates.DepartmentTreeAggregate]


class OrgChartDepartmentNodeSchema(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(serialize_by_alias=True)

    id: uuid.UUID
    title: str
    parent_id: uuid.UUID | None = pydantic.Field(serialization_alias="parentId")


class OrgChartComponentContext(pydantic.BaseModel):
    department_list: list[OrgChartDepartmentNodeSchema]


class IndexHTTPController(Controller):
    path = "/"

    @get(name="company_structure.index")
    @inject
    async def get_page(
        self,
        use_case: FromDishka[use_cases.GenericGetListUseCase[aggregates.DepartmentTreeAggregate]],
    ) -> Template:
        context = IndexPageContext(
            page_title="Home",
            page_description="Index page description",
            page_keywords="Index page keywords",
            breadcrumbs=[
                web_interface.BreadcrumbItem(name="Home", url="/"),
                web_interface.BreadcrumbItem(
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
        context = OrgChartComponentContext(
            department_list=[
                OrgChartDepartmentNodeSchema(**dep.model_dump()) for dep in department_list
            ]
        )
        return HTMXTemplate(
            template_name="company_structure/htmx/org-chart.html.jinja",
            context=context.model_dump(mode="json"),
        )


class CreateDepartmentModalContext(pydantic.BaseModel):
    selected_parent_department: schemas.DepartmentSchema
    department_list: list[schemas.DepartmentSchema]


class CreateDepartmentResultToastContext(pydantic.BaseModel):
    status: Literal["success", "error"]
    timestamp: datetime
    message: str
    details: str


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
        context = CreateDepartmentModalContext(
            selected_parent_department=await get_department_use_case.get(department_id),
            department_list=await get_departments_use_case.get_one_as_list(department_id),
        )
        return HTMXTemplate(
            template_name="company_structure/htmx/create_department_modal.html.jinja",
            context=context.model_dump(mode="json"),
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
        try:
            created_department = await use_case.create(data)
        except Exception as exc:  # noqa: BLE001  # TODO @kosdmit: Refactor with custom exceptions handler for template_router
            context = CreateDepartmentResultToastContext(
                status="error",
                timestamp=datetime.now(tz=UTC),
                message="Failed to create department",
                details=str(exc),
            )
        else:
            context = CreateDepartmentResultToastContext(
                status="success",
                timestamp=datetime.now(tz=UTC),
                message="Department created successfully",
                details=str(created_department),
            )

        return HTMXTemplate(
            template_name="company_structure/htmx/toast.html.jinja",
            context=context.model_dump(mode="json"),
        )
