import uuid

from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import Controller, delete, get, post, put
from litestar.dto import DTOData

from apps.company_structure.application import use_cases
from apps.company_structure.controllers import dto
from apps.company_structure.domain import entities


class DepartmentHTTPController(Controller):
    path = "/departments"

    @get(return_dto=dto.ReadDepartmentDTO)
    @inject
    async def list(
        self,
        use_case: FromDishka[use_cases.GetDepartmentsListUseCase],
    ) -> list[entities.DepartmentEntity | entities.RootDepartmentEntity]:
        return await use_case.list()

    @get(path="/{department_id:uuid}", return_dto=dto.ReadDepartmentDTO)
    @inject
    async def get(
        self,
        use_case: FromDishka[use_cases.GenericGetUseCase[entities.DepartmentEntity]],
        department_id: uuid.UUID,
    ) -> entities.DepartmentEntity:
        return await use_case.get(department_id)

    @post(dto=dto.WriteDepartmentDTO, return_dto=dto.ReadDepartmentDTO)
    @inject
    async def create(
        self,
        use_case: FromDishka[use_cases.GenericCreateUseCase[entities.DepartmentEntity]],
        data: DTOData[entities.DepartmentEntity],
    ) -> entities.DepartmentEntity:
        return await use_case.create(data)

    @put("/{department_id:uuid}", dto=dto.WriteDepartmentDTO, return_dto=dto.ReadDepartmentDTO)
    @inject
    async def update(
        self,
        use_case: FromDishka[use_cases.UpdateDepartmentUseCase],
        department_id: uuid.UUID,
        data: DTOData[entities.DepartmentEntity],
    ) -> entities.DepartmentEntity:
        return await use_case.update(department_id, data)

    @delete("/{department_id:uuid}")
    @inject
    async def delete(
        self,
        use_case: FromDishka[use_cases.DeleteDepartmentUseCase],
        department_id: uuid.UUID,
    ) -> None:
        await use_case.delete(department_id)


class EmployeeHTTPController(Controller):
    path = "/employees"

    @get(return_dto=dto.ReadDepartmentDTO)
    @inject
    async def list(
        self,
        use_case: FromDishka[use_cases.GenericGetListUseCase[entities.EmployeeEntity]],
    ) -> list[entities.EmployeeEntity]:
        return await use_case.list()

    @post(dto=dto.WriteEmployeeDTO, return_dto=dto.ReadEmployeeDTO)
    @inject
    async def create(
        self,
        use_case: FromDishka[use_cases.GenericCreateUseCase[entities.EmployeeEntity]],
        data: DTOData[entities.EmployeeEntity],
    ) -> entities.EmployeeEntity:
        return await use_case.create(data)
