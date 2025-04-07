import uuid

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


class DepartmentRepository(
    ports.FetchAllDepartmentsPort,
    ports.FetchOneDepartmentPort,
    ports.SaveDepartmentPort,
):
    def __init__(
        self,
        db_session: AsyncSession,
        department_gateway: gateways.DepartmentGateway,
    ) -> None:
        self._db_session = db_session
        self._department_gateway = department_gateway

    async def fetch_all(self) -> list[entities.DepartmentEntity | entities.RootDepartmentEntity]:
        orm_departments = await self._department_gateway.fetch_all()
        return [
            self._orm_department_to_entity(orm_department) for orm_department in orm_departments
        ]

    async def fetch_one(self, department_id: uuid.UUID) -> entities.DepartmentEntity:
        orm_department = await self._department_gateway.fetch_one(obj_id=department_id)
        department_entity = self._orm_department_to_entity(orm_department)
        if isinstance(department_entity, entities.RootDepartmentEntity):
            raise GottenWrongDepartmentSubclassError(
                gotten_type=type(department_entity),
                expected_type=entities.DepartmentEntity,
            )
        return department_entity

    async def fetch_root(self) -> entities.RootDepartmentEntity:
        orm_root_department = await self._department_gateway.fetch_root_department()
        root_department_entity = self._orm_department_to_entity(orm_root_department)
        if not isinstance(root_department_entity, entities.RootDepartmentEntity):
            raise GottenWrongDepartmentSubclassError(
                gotten_type=type(root_department_entity),
                expected_type=entities.RootDepartmentEntity,
            )
        return root_department_entity

    async def save(self, department: entities.DepartmentEntity) -> None:
        await self._department_gateway.save(orm_obj=self._entity_to_orm_department(department))
        await self._db_session.commit()

    @staticmethod
    def _orm_department_to_entity(
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

    @staticmethod
    def _entity_to_orm_department(
        entity: entities.DepartmentEntity | entities.RootDepartmentEntity,
    ) -> models.Department:
        return models.Department(
            id=entity.id,
            title=entity.title,
            parent_id=entity.parent_id,
        )
