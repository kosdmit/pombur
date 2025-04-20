import uuid

from pydantic import BaseModel, RootModel


class DepartmentSchema(BaseModel):
    id: uuid.UUID
    title: str
    parent_id: uuid.UUID | None


class DepartmentListSchema(RootModel[list[DepartmentSchema]]):
    root: list[DepartmentSchema]
