from pydantic import BaseModel, UUID4


class DepartmentSchema(BaseModel):
    id: UUID4
    title: str
    parent_id: UUID4
