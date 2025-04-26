import uuid

from pydantic import BaseModel


class DepartmentSchema(BaseModel):
    id: uuid.UUID
    title: str
    parent_id: uuid.UUID | None
