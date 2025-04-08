import uuid
from abc import abstractmethod
from typing import Protocol, TypeVar

from apps.company_structure.domain import entities

EntityT = TypeVar("EntityT")


class GenericFetchAllPort[EntityT](Protocol):
    async def fetch_all(self) -> list[EntityT]:
        raise NotImplementedError


class GenericSavePort[EntityT](Protocol):
    async def save(self, entity: EntityT) -> None:
        raise NotImplementedError


class GenericDeletePort[EntityT](Protocol):
    @abstractmethod
    async def delete(self, entity_id: uuid.UUID) -> None:
        raise NotImplementedError


class GenericFetchOnePort[EntityT](Protocol):
    @abstractmethod
    async def fetch_one(self, entity_id: uuid.UUID) -> EntityT:
        raise NotImplementedError


class FetchAllDepartmentsPort(Protocol):
    @abstractmethod
    async def fetch_all(self) -> list[entities.DepartmentEntity | entities.RootDepartmentEntity]:
        raise NotImplementedError
