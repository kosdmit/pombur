import uuid
from abc import abstractmethod
from typing import Protocol

from apps.company_structure.domain import entities


class FetchAllDepartmentsPort(Protocol):
    @abstractmethod
    async def fetch_all(self) -> list[entities.DepartmentEntity | entities.RootDepartmentEntity]:
        raise NotImplementedError


class FetchOneDepartmentPort(Protocol):
    @abstractmethod
    async def fetch_one(self, department_id: uuid.UUID) -> entities.DepartmentEntity:
        raise NotImplementedError


class SaveDepartmentPort(Protocol):
    @abstractmethod
    async def save(self, department: entities.DepartmentEntity) -> None:
        raise NotImplementedError


class DeleteDepartmentPort(Protocol):
    @abstractmethod
    async def delete(self, department_id: uuid.UUID) -> None:
        raise NotImplementedError
