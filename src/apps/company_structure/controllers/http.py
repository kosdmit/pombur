import uuid
from typing import Annotated

from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import Controller, delete, get, post, put
from litestar.params import Body

from apps.company_structure.application import dto, use_cases
from apps.company_structure.controllers import schemas
from apps.company_structure.domain import entities


class DepartmentHTTPController(Controller):
    path = "/departments"

    @get()
    @inject
    async def list(
        self,
        use_case: FromDishka[use_cases.GetDepartmentsListUseCase],
    ) -> list[schemas.DepartmentSchema]:
        department_entities = await use_case.list()

        return [
            schemas.DepartmentSchema(
                id=entity.id,
                title=entity.title,
                parent_id=entity.parent_id,
            )
            for entity in department_entities
        ]

    @get(path="/{department_id:uuid}")
    @inject
    async def get(
        self,
        use_case: FromDishka[use_cases.GetDepartmentUseCase],
        department_id: uuid.UUID,
    ) -> schemas.DepartmentSchema:
        department_entity = await use_case.get(department_id)
        return schemas.DepartmentSchema(
            id=department_entity.id,
            title=department_entity.title,
            parent_id=department_entity.parent_id,
        )

    @post()
    @inject
    async def create(
        self,
        use_case: FromDishka[use_cases.CreateDepartmentUseCase],
        data: Annotated[dto.NewDepartmentDTO, Body()],
    ) -> schemas.DepartmentSchema:
        department_entity = await use_case.create(data)
        return schemas.DepartmentSchema(
            id=department_entity.id,
            title=department_entity.title,
            parent_id=department_entity.parent_id,
        )

    @put("/{department_id:uuid}")
    @inject
    async def update(
        self,
        use_case: FromDishka[use_cases.UpdateDepartmentUseCase],
        department_id: uuid.UUID,
        data: Annotated[dto.UpdateDepartmentDTO, Body()],
    ) -> schemas.DepartmentSchema:
        department_entity = await use_case.update(department_id, data)
        return schemas.DepartmentSchema(
            id=department_entity.id,
            title=department_entity.title,
            parent_id=department_entity.parent_id,
        )

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

    @get()
    @inject
    async def list(
        self,
        use_case: FromDishka[use_cases.GenericGetListUseCase[entities.EmployeeEntity]],
    ) -> list[schemas.EmployeeSchema]:
        employee_entities = await use_case.list()
        return [
            schemas.EmployeeSchema(
                id=entity.id,
                name=entity.name,
                manager_id=entity.manager_id,
                department_id=entity.department_id,
            )
            for entity in employee_entities
        ]

    @post()
    @inject
    async def create(
        self,
        use_case: FromDishka[
            use_cases.GenericCreateUseCase[dto.NewEmployeeDTO, entities.EmployeeEntity]
        ],
        data: dto.NewEmployeeDTO,
    ) -> schemas.EmployeeSchema:
        employee_entity = await use_case.create(data)
        return schemas.EmployeeSchema(
            id=employee_entity.id,
            name=employee_entity.name,
            manager_id=employee_entity.manager_id,
            department_id=employee_entity.department_id,
        )
