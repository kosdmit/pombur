import uuid
from abc import abstractmethod
from typing import Protocol, TypeVar

from litestar.repository import filters

from apps.company_structure.domain import entities

EntityT = TypeVar("EntityT")


class GenericFetchPort[EntityT](Protocol):
    @abstractmethod
    async def fetch_one(self, entity_id: uuid.UUID) -> EntityT:
        raise NotImplementedError

    async def fetch_all(self) -> list[EntityT]:
        raise NotImplementedError

    async def fetch_page(self, limit_offset: filters.LimitOffset) -> tuple[list[EntityT], int]:
        raise NotImplementedError


class GenericSavePort[EntityT](Protocol):
    async def save(self, entity: EntityT) -> None:
        raise NotImplementedError


class GenericDeletePort[EntityT](Protocol):
    @abstractmethod
    async def delete(self, entity_id: uuid.UUID) -> None:
        raise NotImplementedError


class DepartmentsFetchPort(Protocol):
    @abstractmethod
    async def fetch_one(self, entity_id: uuid.UUID) -> entities.DepartmentEntity:
        raise NotImplementedError

    @abstractmethod
    async def fetch_all(self) -> list[entities.DepartmentEntity | entities.RootDepartmentEntity]:
        raise NotImplementedError

    async def fetch_page(
        self,
        limit_offset: filters.LimitOffset,
    ) -> tuple[list[entities.DepartmentEntity], int]:
        raise NotImplementedError
