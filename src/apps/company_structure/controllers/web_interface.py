import uuid

import pydantic
from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import Controller, get
from litestar.response import Template
from litestar_htmx import HTMXTemplate

from apps.company_structure.application import use_cases
from apps.company_structure.application.schemas import DepartmentSchema
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


class OrgChartComponentContext(pydantic.BaseModel):
    department_list: list[DepartmentSchema]


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

    @get(path="/org-chart/{root_id:uuid}", name="company_structure.org_chart")
    @inject
    async def get_org_chart(
        self,
        root_id: uuid.UUID,
        use_case: FromDishka[use_cases.GetDepartmentTreeAsListUseCase],
    ) -> HTMXTemplate:
        context = OrgChartComponentContext(department_list=await use_case.get_one_as_list(root_id))
        return HTMXTemplate(
            template_name="company_structure/htmx/org-chart.html.jinja",
            context=context.model_dump(mode="json"),
        )
