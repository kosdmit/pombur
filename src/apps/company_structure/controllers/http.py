import uuid
from collections.abc import Sequence
from enum import Enum

from advanced_alchemy.service import OffsetPagination
from dishka.integrations.litestar import FromDishka, inject
from litestar import Controller, delete, get, patch, post, put
from litestar.dto import AbstractDTO, DTOData
from litestar.repository import filters
from litestar.types.empty import EmptyType

from apps.company_structure.application import use_cases
from apps.company_structure.controllers import dtos
from apps.company_structure.domain import entities


class Tags(Enum):
    departments = "Departments"
    employees = "Employees"


class DepartmentHTTPController(Controller):
    path = "/departments"
    id_path_param = "/{department_id:uuid}"

    dto: type[AbstractDTO[entities.DepartmentEntity]] | None | EmptyType = dtos.WriteDepartmentDTO
    return_dto: type[AbstractDTO[entities.DepartmentEntity]] | None | EmptyType = (
        dtos.ReadDepartmentDTO
    )

    tags: Sequence[str] | None = [Tags.departments.value]

    @get()
    @inject
    async def list(
        self,
        use_case: FromDishka[use_cases.GetDepartmentsListUseCase],
    ) -> list[entities.DepartmentEntity | entities.RootDepartmentEntity]:
        return await use_case.list()

    @get(path=id_path_param)
    @inject
    async def get(
        self,
        use_case: FromDishka[use_cases.GenericGetUseCase[entities.DepartmentEntity]],
        department_id: uuid.UUID,
    ) -> entities.DepartmentEntity:
        return await use_case.get(department_id)

    @post()
    @inject
    async def create(
        self,
        use_case: FromDishka[use_cases.GenericCreateUseCase[entities.DepartmentEntity]],
        data: DTOData[entities.DepartmentEntity],
    ) -> entities.DepartmentEntity:
        return await use_case.create(data)

    @put(path=id_path_param)
    @inject
    async def update(
        self,
        use_case: FromDishka[use_cases.UpdateDepartmentUseCase],
        department_id: uuid.UUID,
        data: DTOData[entities.DepartmentEntity],
    ) -> entities.DepartmentEntity:
        return await use_case.update(department_id, data)

    @patch(path=id_path_param, dto=dtos.PatchDepartmentDTO)
    @inject
    async def partial_update(
        self,
        use_case: FromDishka[use_cases.UpdateDepartmentUseCase],
        department_id: uuid.UUID,
        data: DTOData[entities.DepartmentEntity],
    ) -> entities.DepartmentEntity:
        return await use_case.update(department_id, data)

    @delete(path=id_path_param)
    @inject
    async def delete(
        self,
        use_case: FromDishka[use_cases.DeleteDepartmentUseCase],
        department_id: uuid.UUID,
    ) -> None:
        await use_case.delete(department_id)


class EmployeeHTTPController(Controller):
    path = "/employees"
    id_path_param = "/{employee_id:uuid}"

    dto: type[AbstractDTO[entities.EmployeeEntity]] | None | EmptyType = dtos.WriteEmployeeDTO
    return_dto: type[AbstractDTO[entities.EmployeeEntity]] | None | EmptyType = dtos.ReadEmployeeDTO

    tags: Sequence[str] | None = [Tags.employees.value]

    @get()
    @inject
    async def list(
        self,
        use_case: FromDishka[use_cases.GenericGetPaginatedListUseCase[entities.EmployeeEntity]],
        limit_offset: filters.LimitOffset,
    ) -> OffsetPagination[entities.EmployeeEntity]:
        results, total = await use_case.paginated_list(limit_offset)
        return OffsetPagination(
            items=results,
            total=total,
            limit=limit_offset.limit,
            offset=limit_offset.offset,
        )

    @post()
    @inject
    async def create(
        self,
        use_case: FromDishka[use_cases.GenericCreateUseCase[entities.EmployeeEntity]],
        data: DTOData[entities.EmployeeEntity],
    ) -> entities.EmployeeEntity:
        return await use_case.create(data)
