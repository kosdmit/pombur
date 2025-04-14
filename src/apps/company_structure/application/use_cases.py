import uuid
from abc import abstractmethod
from typing import Protocol, TypeVar

from litestar.dto import DTOData
from litestar.repository import filters

from apps.company_structure.domain import entities

EntityT = TypeVar("EntityT")
IdentifierT = TypeVar("IdentifierT")


class GenericGetListUseCase[EntityT](Protocol):
    async def list(self) -> list[EntityT]:
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


class GetDepartmentsListUseCase(Protocol):
    @abstractmethod
    async def list(self) -> list[entities.DepartmentEntity | entities.RootDepartmentEntity]:
        raise NotImplementedError


class UpdateDepartmentUseCase(Protocol):
    @abstractmethod
    async def update(
        self,
        department_id: uuid.UUID,
        department_data: DTOData[entities.DepartmentEntity],
    ) -> entities.DepartmentEntity:
        raise NotImplementedError


class DeleteDepartmentUseCase(Protocol):
    @abstractmethod
    async def delete(self, department_id: uuid.UUID) -> None:
        raise NotImplementedError
