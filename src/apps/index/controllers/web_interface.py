import pydantic
from litestar import Controller, MediaType, get
from litestar.response import Template

from common.controllers import context_schemas as common_context_schemas


class IndexPageContext(
    common_context_schemas.HeadPageMetaContext,
    common_context_schemas.BreadcrumbsContext,
    pydantic.BaseModel,
):
    """Index page context.

    Contains the data that is passed to the template as context.
    """


class IndexHTTPController(Controller):
    path = "/"

    @get(media_type=MediaType.HTML, name="index")
    async def get(self) -> Template:
        context = IndexPageContext(
            page_title="Home",
            page_description="Index page description",
            page_keywords="Index page keywords",
            breadcrumbs=[
                common_context_schemas.BreadcrumbItem(name="Home", url="/", is_active=True),
            ],
        )

        return Template("index/index.html.jinja", context=context.model_dump())
