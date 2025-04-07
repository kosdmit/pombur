from dataclasses import dataclass
from uuid import UUID


@dataclass(slots=True)
class BaseDepartmentEntity:
    id: UUID
    title: str


@dataclass(slots=True)
class RootDepartmentEntity(BaseDepartmentEntity):
    parent_id: None


@dataclass(slots=True)
class DepartmentEntity(BaseDepartmentEntity):
    parent_id: UUID
