import uuid
from abc import abstractmethod
from typing import Protocol

from apps.company_structure.application import dto
from apps.company_structure.domain import entities


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
