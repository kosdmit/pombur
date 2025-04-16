from pydantic import BaseModel


class HeadPageMetaContext(BaseModel):
    page_title: str
    page_description: str
    page_keywords: str


class BreadcrumbItem(BaseModel):
    name: str
    url: str
    is_active: bool = False


class BreadcrumbsContext(BaseModel):
    breadcrumbs: list[BreadcrumbItem]
