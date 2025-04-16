import pydantic
from litestar import Controller, get
from litestar.response import Template

from common.controllers import web_interface


class IndexPageContext(
    web_interface.HeadPageMetaContext,
    web_interface.BreadcrumbsContext,
    pydantic.BaseModel,
):
    """Index page context.

    Contains the data that is passed to the template as context.
    """


class IndexHTTPController(Controller):
    path = "/"

    @get(name="company_structure.index")
    async def get(self) -> Template:
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
        )

        return Template(
            template_name="company_structure/index.html.jinja",
            context=context.model_dump(),
        )
