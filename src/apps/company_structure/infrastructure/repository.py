from apps.company_structure.application import ports
from apps.company_structure.domain import entities
from apps.company_structure.infrastructure import gateways, models


class DepartmentRepository(ports.FetchAllDepartmentsPort, ports.SaveDepartmentPort):
    def __init__(self, department_gateway: gateways.DepartmentGateway) -> None:
        self._department_gateway = department_gateway

    async def fetch_all(self) -> list[entities.DepartmentEntity]:
        orm_departments = await self._department_gateway.fetch_all()
        return [
            self._orm_department_to_entity(orm_department)
            for orm_department in orm_departments
        ]

    async def save(self, department: entities.DepartmentEntity) -> None:
        await self._department_gateway.save(obj=self._entity_to_orm_department(department))

    @staticmethod
    def _orm_department_to_entity(orm_department: models.Department) -> entities.DepartmentEntity:
        return entities.DepartmentEntity(
            id=orm_department.id,
            title=orm_department.title,
            parent_id=orm_department.parent_id,
        )

    @staticmethod
    def _entity_to_orm_department(entity: entities.DepartmentEntity) -> models.Department:
        return models.Department(
            id=entity.id,
            title=entity.title,
            parent_id=entity.parent_id,
        )

