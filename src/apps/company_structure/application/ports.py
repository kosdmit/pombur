from abc import abstractmethod
from typing import Protocol, TypeVar

from litestar.repository import filters

EntityT = TypeVar("EntityT")
IdentifierT = TypeVar("IdentifierT")


class GenericFetchPort[IdentifierT, EntityT](Protocol):
    @abstractmethod
    async def fetch_one(self, identifier: IdentifierT, /) -> EntityT:
        raise NotImplementedError

    async def fetch_all(self) -> list[EntityT]:
        raise NotImplementedError

    async def fetch_page(self, limit_offset: filters.LimitOffset) -> tuple[list[EntityT], int]:
        raise NotImplementedError


class GenericSavePort[EntityT](Protocol):
    @abstractmethod
    async def save(self, entity: EntityT) -> None:
        raise NotImplementedError


class GenericDeletePort[IdentifierT](Protocol):
    @abstractmethod
    async def delete(self, entity_id: IdentifierT) -> None:
        raise NotImplementedError
