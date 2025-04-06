from pydantic import UUID4, BaseModel


class DepartmentSchema(BaseModel):
    id: UUID4
    title: str
    parent_id: UUID4
