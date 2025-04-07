import uuid

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
        fetch_one_port: ports.FetchOneDepartmentPort,
        save_port: ports.SaveDepartmentPort,
        delete_port: ports.DeleteDepartmentPort,
    ) -> None:
        self._fetch_all_port = fetch_all_port
        self._fetch_one_port = fetch_one_port
        self._save_port = save_port
        self._delete_port = delete_port

    async def list(self) -> list[entities.BaseDepartmentEntity]:
        return await self._fetch_all_port.fetch_all()

    async def get(self, department_id: uuid.UUID) -> entities.DepartmentEntity:
        return await self._fetch_one_port.fetch_one(department_id)

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

    async def delete(self, department_id: uuid.UUID) -> None:
        await self._delete_port.delete(department_id)
