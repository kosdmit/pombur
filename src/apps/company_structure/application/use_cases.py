import uuid
from abc import abstractmethod
from typing import Protocol, TypeVar

from litestar.dto import DTOData

from apps.company_structure.domain import entities

EntityT = TypeVar("EntityT")


class GenericGetListUseCase[EntityT](Protocol):
    async def list(self) -> list[EntityT]:
        raise NotImplementedError


class GenericGetUseCase[EntityT](Protocol):
    async def get(self, entity_id: uuid.UUID) -> EntityT:
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
