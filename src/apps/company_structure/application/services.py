import uuid

from apps.company_structure.application import dto, ports, use_cases
from apps.company_structure.domain import entities


class DepartmentService(
    use_cases.GetDepartmentsListUseCase,
    use_cases.CreateDepartmentUseCase,
):
    def __init__(
        self,
        fetch_all_port: ports.FetchAllDepartmentsPort,
        save_port: ports.SaveDepartmentPort,
    ) -> None:
        self._fetch_all_port = fetch_all_port
        self._save_port = save_port

    async def list(self) -> list[entities.DepartmentEntity]:
        return await self._fetch_all_port.fetch_all()

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
