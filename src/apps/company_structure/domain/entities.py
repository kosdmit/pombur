from dataclasses import dataclass
from typing import Generic, TypeVar
from uuid import UUID

ParentIdT = TypeVar("ParentIdT", bound=UUID | None)


@dataclass(slots=True)
class _GenericDepartmentEntity(Generic[ParentIdT]):
    id: UUID
    title: str
    parent_id: ParentIdT


@dataclass(slots=True)
class RootDepartmentEntity(_GenericDepartmentEntity[None]):
    """Domain entity representing root department.

    Root department is a special department that has no parent.
    It is the root of the department tree.
    """


@dataclass(slots=True)
class DepartmentEntity(_GenericDepartmentEntity[UUID]):
    """Domain entity representing department. It is a node in the department tree."""
