from dataclasses import dataclass
from uuid import UUID


@dataclass(slots=True)
class NewDepartmentDTO:
    title: str
    parent_id: UUID


@dataclass(slots=True)
class UpdateDepartmentDTO:
    title: str
    parent_id: UUID


@dataclass(slots=True)
class NewEmployeeDTO:
    name: str
    manager_id: UUID | None
    department_id: UUID
