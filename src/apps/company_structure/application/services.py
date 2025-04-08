import uuid
from typing import override

from apps.company_structure.application import dto, ports, use_cases
from apps.company_structure.domain import entities


class DepartmentService(  # noqa: WPS215  # reason: explicit define implemented interfaces
    use_cases.GetDepartmentsListUseCase,
    use_cases.GetDepartmentUseCase,
    use_cases.CreateDepartmentUseCase,
    use_cases.UpdateDepartmentUseCase,
    use_cases.DeleteDepartmentUseCase,
):
    def __init__(
        self,
        fetch_all_port: ports.FetchAllDepartmentsPort,
        fetch_one_port: ports.GenericFetchOnePort[entities.DepartmentEntity],
        save_port: ports.GenericSavePort[entities.DepartmentEntity],
        delete_port: ports.GenericDeletePort[entities.DepartmentEntity],
    ) -> None:
        self._fetch_all_port = fetch_all_port
        self._fetch_one_port = fetch_one_port
        self._save_port = save_port
        self._delete_port = delete_port

    @override
    async def list(self) -> list[entities.DepartmentEntity | entities.RootDepartmentEntity]:
        return await self._fetch_all_port.fetch_all()

    @override
    async def get(self, department_id: uuid.UUID) -> entities.DepartmentEntity:
        return await self._fetch_one_port.fetch_one(department_id)

    @override
    async def create(
        self,
        department_data: dto.NewDepartmentDTO,
    ) -> entities.DepartmentEntity:
        department_entity = entities.DepartmentEntity(
            id=uuid.uuid4(),
            title=department_data.title,
            parent_id=department_data.parent_id,
        )
        await self._save_port.save(department_entity)
        return department_entity

    @override
    async def update(
        self,
        department_id: uuid.UUID,
        department_data: dto.UpdateDepartmentDTO,
    ) -> entities.DepartmentEntity:
        department_entity = await self._fetch_one_port.fetch_one(department_id)
        department_entity.title = department_data.title
        department_entity.parent_id = department_data.parent_id
        await self._save_port.save(department_entity)
        return department_entity

    @override
    async def delete(self, department_id: uuid.UUID) -> None:
        await self._delete_port.delete(department_id)


class EmployeeService(
    use_cases.GenericGetListUseCase[entities.EmployeeEntity],
    use_cases.GenericCreateUseCase[dto.NewEmployeeDTO, entities.EmployeeEntity],
):
    def __init__(
        self,
        fetch_all_employees_port: ports.GenericFetchAllPort[entities.EmployeeEntity],
        save_port: ports.GenericSavePort[entities.EmployeeEntity],
    ) -> None:
        self._fetch_all_employees_port = fetch_all_employees_port
        self._save_port = save_port

    @override
    async def list(self) -> list[entities.EmployeeEntity]:
        return await self._fetch_all_employees_port.fetch_all()

    @override
    async def create(self, entity_data: dto.NewEmployeeDTO) -> entities.EmployeeEntity:
        employee_entity = entities.EmployeeEntity(
            id=uuid.uuid4(),
            name=entity_data.name,
            manager_id=entity_data.manager_id,
            department_id=entity_data.department_id,
        )
        await self._save_port.save(employee_entity)
        return employee_entity
