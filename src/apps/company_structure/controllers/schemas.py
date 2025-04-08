from uuid import UUID

from pydantic import BaseModel


class DepartmentSchema(BaseModel):
    id: UUID
    title: str
    parent_id: UUID | None


class EmployeeSchema(BaseModel):
    id: UUID
    name: str
    manager_id: UUID | None
    department_id: UUID
