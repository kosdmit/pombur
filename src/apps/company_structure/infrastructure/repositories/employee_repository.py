from typing import override

from litestar.repository import filters
from sqlalchemy.ext.asyncio import AsyncSession

from apps.company_structure.application import ports
from apps.company_structure.domain import entities
from apps.company_structure.infrastructure import gateways, models


class EmployeeRepository(
    ports.GenericFetchPort[str, entities.EmployeeEntity],
    ports.GenericSavePort[entities.EmployeeEntity],
):
    def __init__(
        self,
        employee_gateway: gateways.EmployeeGateway,
        db_session: AsyncSession,
    ) -> None:
        self._employee_gateway = employee_gateway
        self._db_session = db_session

    @override
    async def fetch_one(self, slug: str) -> entities.EmployeeEntity:
        orm_employee = await self._employee_gateway.get_one(slug=slug)
        return _convert_orm_employee_to_entity(orm_employee)

    @override
    async def fetch_all(self) -> list[entities.EmployeeEntity]:
        orm_objects = await self._employee_gateway.list()
        return [_convert_orm_employee_to_entity(orm_object) for orm_object in orm_objects]

    @override
    async def fetch_page(
        self,
        limit_offset: filters.LimitOffset,
    ) -> tuple[list[entities.EmployeeEntity], int]:
        orm_objects, total = await self._employee_gateway.list_and_count(limit_offset)
        return [_convert_orm_employee_to_entity(orm_object) for orm_object in orm_objects], total

    @override
    async def save(self, employee: entities.EmployeeEntity) -> None:
        await self._employee_gateway.upsert(await self._convert_entity_to_orm_employee(employee))
        await self._db_session.commit()

    async def _convert_entity_to_orm_employee(
        self,
        entity: entities.EmployeeEntity,
    ) -> models.Employee:
        existent_orm_object = await self._employee_gateway.get_one_or_none(id=entity.id)
        if existent_orm_object is None:
            slug = await self._employee_gateway.get_available_slug(entity.name)
        else:
            slug = existent_orm_object.slug

        return models.Employee(
            id=entity.id,
            slug=slug,
            name=entity.name,
            manager=entity.manager,
            department_id=entity.department_id,
        )


def _convert_orm_employee_to_entity(
    orm_employee: models.Employee,
) -> entities.EmployeeEntity:
    return entities.EmployeeEntity(
        id=orm_employee.id,
        name=orm_employee.name,
        manager=(
            _convert_orm_employee_to_entity(orm_employee.manager) if orm_employee.manager else None
        ),
        department_id=orm_employee.department_id,
    )
