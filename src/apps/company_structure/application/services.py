import builtins
import uuid
from typing import override

from litestar.dto import DTOData
from litestar.repository import filters

from apps.company_structure.application import ports, use_cases
from apps.company_structure.domain import entities


class DepartmentService(  # noqa: WPS215  # reason: explicit define implemented interfaces
    use_cases.GenericGetListUseCase[entities.DepartmentEntity],
    use_cases.GenericGetUseCase[uuid.UUID, entities.DepartmentEntity],
    use_cases.GetRootDepartmentUseCase,
    use_cases.GenericCreateUseCase[entities.DepartmentEntity],
    use_cases.UpdateDepartmentUseCase,
    use_cases.DeleteDepartmentUseCase,
):
    def __init__(
        self,
        fetch_port: ports.DepartmentsFetchPort,
        save_port: ports.GenericSavePort[entities.DepartmentEntity],
        delete_port: ports.GenericDeletePort[entities.DepartmentEntity],
    ) -> None:
        self._fetch_port = fetch_port
        self._save_port = save_port
        self._delete_port = delete_port

    @override
    async def list(self) -> list[entities.DepartmentEntity]:
        return await self._fetch_port.fetch_all()

    @override
    async def get(self, department_id: uuid.UUID) -> entities.DepartmentEntity:
        return await self._fetch_port.fetch_one(department_id)

    @override
    async def get_root(self) -> entities.RootDepartmentEntity:
        return await self._fetch_port.fetch_root()

    @override
    async def create(
        self,
        input_data: DTOData[entities.DepartmentEntity],
    ) -> entities.DepartmentEntity:
        department_entity = input_data.create_instance(id=uuid.uuid4())
        await self._save_port.save(department_entity)
        return department_entity

    @override
    async def update(
        self,
        department_id: uuid.UUID,
        department_data: DTOData[entities.DepartmentEntity],
    ) -> entities.DepartmentEntity:
        department_entity_to_update = await self._fetch_port.fetch_one(department_id)
        updated_department_entity = department_data.update_instance(department_entity_to_update)
        await self._save_port.save(updated_department_entity)
        return updated_department_entity

    @override
    async def delete(self, department_id: uuid.UUID) -> None:
        await self._delete_port.delete(department_id)


class EmployeeService(  # noqa: WPS215  # reason: explicit define implemented interfaces
    use_cases.GenericGetUseCase[str, entities.EmployeeEntity],
    use_cases.GenericGetListUseCase[entities.EmployeeEntity],
    use_cases.GenericCreateUseCase[entities.EmployeeEntity],
    use_cases.GenericGetPaginatedListUseCase[entities.EmployeeEntity],
):
    def __init__(
        self,
        fetch_port: ports.GenericFetchPort[str, entities.EmployeeEntity],
        save_port: ports.GenericSavePort[entities.EmployeeEntity],
    ) -> None:
        self._fetch_port = fetch_port
        self._save_port = save_port

    @override
    async def get(self, slug: str) -> entities.EmployeeEntity:
        return await self._fetch_port.fetch_one(slug)

    @override
    async def list(self) -> list[entities.EmployeeEntity]:
        return await self._fetch_port.fetch_all()

    @override
    async def paginated_list(
        self,
        limit_offset: filters.LimitOffset,
    ) -> tuple[builtins.list[entities.EmployeeEntity], int]:
        return await self._fetch_port.fetch_page(limit_offset)

    @override
    async def create(
        self, entity_data: DTOData[entities.EmployeeEntity]
    ) -> entities.EmployeeEntity:
        employee_entity = entity_data.create_instance(id=uuid.uuid4())
        await self._save_port.save(employee_entity)
        return employee_entity
