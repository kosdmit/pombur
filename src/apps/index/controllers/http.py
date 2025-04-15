from litestar import Controller, MediaType, get
from litestar.response import Template


class IndexHTTPController(Controller):
    path = "/"

    @get(media_type=MediaType.HTML)
    async def get(self) -> Template:
        return Template("index/index.html.jinja")
