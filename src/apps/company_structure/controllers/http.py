import uuid

from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import Controller, delete, get, patch, post, put
from litestar.dto import AbstractDTO, DTOData
from litestar.types.empty import EmptyType

from apps.company_structure.application import use_cases
from apps.company_structure.controllers import dtos
from apps.company_structure.domain import entities


class DepartmentHTTPController(Controller):
    path = "/departments"
    id_path_param = "/{department_id:uuid}"

    dto: type[AbstractDTO[entities.DepartmentEntity]] | None | EmptyType = dtos.WriteDepartmentDTO
    return_dto: type[AbstractDTO[entities.DepartmentEntity]] | None | EmptyType = (
        dtos.ReadDepartmentDTO
    )

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

    @get()
    @inject
    async def list(
        self,
        use_case: FromDishka[use_cases.GenericGetListUseCase[entities.EmployeeEntity]],
    ) -> list[entities.EmployeeEntity]:
        return await use_case.list()

    @post()
    @inject
    async def create(
        self,
        use_case: FromDishka[use_cases.GenericCreateUseCase[entities.EmployeeEntity]],
        data: DTOData[entities.EmployeeEntity],
    ) -> entities.EmployeeEntity:
        return await use_case.create(data)
