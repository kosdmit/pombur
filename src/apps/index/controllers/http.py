from litestar import Controller, MediaType, get
from litestar.response import Template
from pydantic import BaseModel


class HeadPageMetaContext(BaseModel):
    page_title: str
    page_description: str
    page_keywords: str


class IndexPageContext(HeadPageMetaContext):
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
        )

        return Template("index/index.html.jinja", context=context.model_dump())
