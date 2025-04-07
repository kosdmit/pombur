from uuid import UUID

from pydantic import BaseModel


class DepartmentSchema(BaseModel):
    id: UUID
    title: str
    parent_id: UUID | None
