import uuid
from typing import Annotated

from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import Controller, get, post, put
from litestar.params import Body

from apps.company_structure.application import dto, use_cases
from apps.company_structure.controllers import schemas


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
        data: Annotated[dto.NewDepartmentDTO, Body()],  # noqa: WPS110  # reason: litestar syntax
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
        data: Annotated[dto.UpdateDepartmentDTO, Body()],  # noqa: WPS110  # reason: litestar syntax
    ) -> schemas.DepartmentSchema:
        department_entity = await use_case.update(department_id, data)
        return schemas.DepartmentSchema(
            id=department_entity.id,
            title=department_entity.title,
            parent_id=department_entity.parent_id,
        )
