from abc import abstractmethod
from typing import Protocol, TypeVar

from litestar.dto import DTOData
from litestar.repository import filters

EntityT = TypeVar("EntityT")
IdentifierT = TypeVar("IdentifierT")


class GenericGetListUseCase[EntityT](Protocol):
    async def get_list(self) -> list[EntityT]:
        raise NotImplementedError


class GenericGetPaginatedListUseCase[EntityT](Protocol):
    async def paginated_list(self, limit_offset: filters.LimitOffset) -> tuple[list[EntityT], int]:
        raise NotImplementedError


class GenericGetUseCase[IdentifierT, EntityT](Protocol):
    async def get(self, identifier: IdentifierT, /) -> EntityT:
        raise NotImplementedError


class GenericCreateUseCase[EntityT](Protocol):
    async def create(self, input_data: DTOData[EntityT]) -> EntityT:
        raise NotImplementedError


class GenericUpdateUseCase[IdentifierT, EntityT](Protocol):
    @abstractmethod
    async def update(self, identifier: IdentifierT, input_data: DTOData[EntityT]) -> EntityT:
        raise NotImplementedError


class GenericDeleteUseCase[IdentifierT](Protocol):
    @abstractmethod
    async def delete(self, identifier: IdentifierT) -> None:
        raise NotImplementedError
