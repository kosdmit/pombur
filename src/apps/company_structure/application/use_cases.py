import uuid
from abc import abstractmethod
from typing import Protocol, TypeVar

from apps.company_structure.application import dto
from apps.company_structure.domain import entities

EntityT = TypeVar("EntityT")
DtoT = TypeVar("DtoT")


class GenericGetListUseCase[EntityT](Protocol):
    async def list(self) -> list[EntityT]:
        raise NotImplementedError


class GenericCreateUseCase[DtoT, EntityT](Protocol):
    async def create(self, input_data: DtoT) -> EntityT:
        raise NotImplementedError


class GetDepartmentsListUseCase(Protocol):
    @abstractmethod
    async def list(self) -> list[entities.DepartmentEntity | entities.RootDepartmentEntity]:
        raise NotImplementedError


class GetDepartmentUseCase(Protocol):
    @abstractmethod
    async def get(self, department_id: uuid.UUID) -> entities.DepartmentEntity:
        raise NotImplementedError


class CreateDepartmentUseCase(Protocol):
    @abstractmethod
    async def create(self, department_data: dto.NewDepartmentDTO) -> entities.DepartmentEntity:
        raise NotImplementedError


class UpdateDepartmentUseCase(Protocol):
    @abstractmethod
    async def update(
        self,
        department_id: uuid.UUID,
        department_data: dto.UpdateDepartmentDTO,
    ) -> entities.DepartmentEntity:
        raise NotImplementedError


class DeleteDepartmentUseCase(Protocol):
    @abstractmethod
    async def delete(self, department_id: uuid.UUID) -> None:
        raise NotImplementedError
