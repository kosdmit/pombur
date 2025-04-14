import uuid
from typing import override

from litestar.repository import filters
from sqlalchemy.ext.asyncio import AsyncSession

from apps.company_structure.application import ports
from apps.company_structure.domain import entities
from apps.company_structure.infrastructure import gateways, models


class GottenWrongDepartmentSubclassError(TypeError):
    def __init__(self, gotten_type: type, expected_type: type) -> None:
        super().__init__(
            f"Gotten wrong department subclass: {gotten_type} instead of {expected_type}. "
            f"Use special DepartmentRepository methods to get {expected_type}."
        )


def _convert_orm_department_to_entity(
    orm_department: models.Department,
) -> entities.DepartmentEntity | entities.RootDepartmentEntity:
    if orm_department.parent_id is None:
        return entities.RootDepartmentEntity(
            id=orm_department.id,
            title=orm_department.title,
            parent_id=None,
        )

    return entities.DepartmentEntity(
        id=orm_department.id,
        title=orm_department.title,
        parent_id=orm_department.parent_id,
    )


def _convert_entity_to_orm_department(
    entity: entities.DepartmentEntity | entities.RootDepartmentEntity,
) -> models.Department:
    return models.Department(
        id=entity.id,
        title=entity.title,
        parent_id=entity.parent_id,
    )


class DepartmentRepository(  # noqa: WPS215  # reason: explicit define implemented interfaces
    ports.DepartmentsFetchPort,
    ports.GenericSavePort[entities.DepartmentEntity],
    ports.GenericDeletePort[entities.DepartmentEntity],
):
    def __init__(
        self,
        db_session: AsyncSession,
        department_gateway: gateways.DepartmentGateway,
    ) -> None:
        self._db_session = db_session
        self._department_gateway = department_gateway

    @override
    async def fetch_all(self) -> list[entities.DepartmentEntity | entities.RootDepartmentEntity]:
        orm_departments = await self._department_gateway.list()
        return [
            _convert_orm_department_to_entity(orm_department) for orm_department in orm_departments
        ]

    @override
    async def fetch_one(self, department_id: uuid.UUID) -> entities.DepartmentEntity:
        orm_department = await self._department_gateway.get_one(id=department_id)
        department_entity = _convert_orm_department_to_entity(orm_department)
        if isinstance(department_entity, entities.RootDepartmentEntity):
            raise GottenWrongDepartmentSubclassError(
                gotten_type=type(department_entity),
                expected_type=entities.DepartmentEntity,
            )
        return department_entity

    async def fetch_root(self) -> entities.RootDepartmentEntity:
        orm_root_department = await self._department_gateway.fetch_root_department()
        root_department_entity = _convert_orm_department_to_entity(orm_root_department)
        if not isinstance(root_department_entity, entities.RootDepartmentEntity):
            raise GottenWrongDepartmentSubclassError(
                gotten_type=type(root_department_entity),
                expected_type=entities.RootDepartmentEntity,
            )
        return root_department_entity

    @override
    async def save(self, department: entities.DepartmentEntity) -> None:
        await self._department_gateway.upsert(_convert_entity_to_orm_department(department))
        await self._db_session.commit()

    @override
    async def delete(self, department_id: uuid.UUID) -> None:
        await self._department_gateway.delete(department_id)
        await self._db_session.commit()


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
