import uuid
from collections.abc import Sequence
from enum import Enum

from advanced_alchemy.service import OffsetPagination
from dishka.integrations.litestar import FromDishka, inject
from litestar import Controller, delete, get, patch, post, put
from litestar.dto import AbstractDTO, DTOData
from litestar.repository import filters
from litestar.types.empty import EmptyType

from apps.company_structure.application import schemas, use_cases
from apps.company_structure.controllers import dtos
from apps.company_structure.domain import aggregates, entities


class Tags(Enum):
    departments = "Departments"
    employees = "Employees"


class DepartmentHTTPController(Controller):
    path = "/departments"
    id_path_param = "/{department_id:uuid}"
    dto: type[AbstractDTO[schemas.DepartmentSchema]] | None | EmptyType = dtos.WriteDepartmentDTO
    tags: Sequence[str] | None = [Tags.departments.value]

    @get("/trees", dto=None, return_dto=None)
    @inject
    async def get_trees(
        self,
        use_case: FromDishka[use_cases.GenericGetListUseCase[aggregates.DepartmentTreeAggregate]],
    ) -> list[aggregates.DepartmentTreeAggregate]:
        return await use_case.get_list()

    @get("trees/{root_id:uuid}", dto=None, return_dto=None)
    @inject
    async def get_tree(
        self,
        use_case: FromDishka[
            use_cases.GenericGetUseCase[uuid.UUID, aggregates.DepartmentTreeAggregate]
        ],
        root_id: uuid.UUID,
    ) -> aggregates.DepartmentTreeAggregate:
        return await use_case.get(root_id)

    @get("/trees/{root_id:uuid}/as_list")
    @inject
    async def get_tree_as_list(
        self,
        use_case: FromDishka[use_cases.GetDepartmentTreeAsListUseCase],
        root_id: uuid.UUID,
    ) -> list[schemas.DepartmentSchema]:
        return await use_case.get_one_as_list(root_id)

    @get(path=id_path_param)
    @inject
    async def get(
        self,
        use_case: FromDishka[use_cases.GenericGetUseCase[uuid.UUID, schemas.DepartmentSchema]],
        department_id: uuid.UUID,
    ) -> schemas.DepartmentSchema:
        return await use_case.get(department_id)

    @post(name="company_structure.create_department")
    @inject
    async def create(
        self,
        use_case: FromDishka[use_cases.GenericCreateUseCase[schemas.DepartmentSchema]],
        data: DTOData[schemas.DepartmentSchema],
    ) -> schemas.DepartmentSchema:
        return await use_case.create(data)

    @put(path=id_path_param)
    @inject
    async def update(
        self,
        use_case: FromDishka[use_cases.GenericUpdateUseCase[uuid.UUID, schemas.DepartmentSchema]],
        department_id: uuid.UUID,
        data: DTOData[schemas.DepartmentSchema],
    ) -> schemas.DepartmentSchema:
        return await use_case.update(department_id, data)

    @patch(path=id_path_param, dto=dtos.PatchDepartmentDTO)
    @inject
    async def partial_update(
        self,
        use_case: FromDishka[use_cases.GenericUpdateUseCase[uuid.UUID, schemas.DepartmentSchema]],
        department_id: uuid.UUID,
        data: DTOData[schemas.DepartmentSchema],
    ) -> schemas.DepartmentSchema:
        return await use_case.update(department_id, data)

    @delete(path=id_path_param)
    @inject
    async def delete(
        self,
        use_case: FromDishka[use_cases.GenericDeleteUseCase[uuid.UUID]],
        department_id: uuid.UUID,
    ) -> None:
        await use_case.delete(department_id)


class EmployeeHTTPController(Controller):
    path = "/employees"
    slug_path_param = "/{slug:str}"

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

    @get(path=slug_path_param)
    @inject
    async def get(
        self,
        use_case: FromDishka[use_cases.GenericGetUseCase[str, entities.EmployeeEntity]],
        slug: str,
    ) -> entities.EmployeeEntity:
        return await use_case.get(slug)

    @post()
    @inject
    async def create(
        self,
        use_case: FromDishka[use_cases.GenericCreateUseCase[entities.EmployeeEntity]],
        data: DTOData[entities.EmployeeEntity],
    ) -> entities.EmployeeEntity:
        return await use_case.create(data)
