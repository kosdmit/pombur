import uuid
from datetime import datetime
from typing import Literal

import pydantic

from apps.company_structure.application import schemas
from apps.company_structure.domain import aggregates
from common.controllers import context_schemas as common_context_schemas


class IndexPageContext(
    common_context_schemas.HeadPageMetaContext,
    common_context_schemas.BreadcrumbsContext,
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


class CreateDepartmentModalContext(pydantic.BaseModel):
    selected_parent_department: schemas.DepartmentSchema
    department_list: list[schemas.DepartmentSchema]


class ResultToastContext(pydantic.BaseModel):
    status: Literal["success", "error"]
    timestamp: datetime
    message: str
    details: dict[str, str]


class DeleteDepartmentModalContext(pydantic.BaseModel):
    department_to_delete: schemas.DepartmentSchema
