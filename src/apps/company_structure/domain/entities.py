from dataclasses import dataclass, field
from uuid import UUID


@dataclass(slots=True)
class EmployeeEntity:
    id: UUID
    name: str
    department_id: UUID

    manager: "EmployeeEntity | None" = field(default=None)
