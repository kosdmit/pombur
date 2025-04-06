from dataclasses import dataclass
from uuid import UUID


@dataclass(slots=True)
class NewDepartmentDTO:
    title: str
    parent_id: UUID