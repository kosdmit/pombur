from dataclasses import dataclass
from uuid import UUID


@dataclass(slots=True)
class DepartmentEntity:
    id: UUID
    title: str
    parent_id: UUID