from dishka import FromDishka
from dishka.integrations.litestar import inject
from litestar import Controller, get

from apps.company_structure.application.use_cases import GetDepartmentsListUseCase
from apps.company_structure.controllers import schemas


class DepartmentHTTPController(Controller):
    path = "/departments"

    @get()
    @inject
    async def list(
        self,
        use_case: FromDishka[GetDepartmentsListUseCase],
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
