import uuid
from typing import override

from sqlalchemy.ext.asyncio import AsyncSession

from apps.company_structure.application import ports, schemas
from apps.company_structure.domain import aggregates
from apps.company_structure.domain import exceptions as domain_exceptions
from apps.company_structure.infrastructure import gateways, models


def _convert_orm_department_to_schema(
    orm_department: models.Department,
) -> schemas.DepartmentSchema:
    return schemas.DepartmentSchema.model_validate(orm_department.__dict__)


class DepartmentRepository(  # noqa: WPS215  # reason: explicit define implemented interfaces
    ports.GenericFetchPort[uuid.UUID, schemas.DepartmentSchema],
    ports.GenericSavePort[schemas.DepartmentSchema],
    ports.GenericDeletePort[uuid.UUID],
):
    def __init__(
        self,
        db_session: AsyncSession,
        department_gateway: gateways.DepartmentGateway,
    ) -> None:
        self._db_session = db_session
        self._department_gateway = department_gateway

    @override
    async def fetch_one(self, department_id: uuid.UUID) -> schemas.DepartmentSchema:
        orm_department = await self._department_gateway.get(department_id)
        return _convert_orm_department_to_schema(orm_department)

    @override
    async def save(self, department_data: schemas.DepartmentSchema) -> None:
        orm_object = await self._convert_to_orm(department_data)
        await self._department_gateway.upsert(orm_object)
        await self._db_session.commit()

    @override
    async def delete(self, department_id: uuid.UUID) -> None:
        await self._department_gateway.delete(department_id)
        await self._db_session.commit()

    async def _convert_to_orm(
        self,
        department_data: schemas.DepartmentSchema,
    ) -> models.Department:
        existent_orm_object = await self._department_gateway.get_one_or_none(id=department_data.id)
        if existent_orm_object is None:
            slug = await self._department_gateway.get_available_slug(department_data.title)
        else:
            slug = existent_orm_object.slug

        return models.Department(
            id=department_data.id,
            slug=slug,
            title=department_data.title,
            parent_id=department_data.parent_id,
        )


class GottenWrongDepartmentSubclassError(TypeError):
    def __init__(self, gotten_type: type, expected_type: type) -> None:
        super().__init__(
            f"Gotten wrong department subclass: {gotten_type} instead of {expected_type}. "
            f"Use special DepartmentRepository methods to get {expected_type}."
        )


def _convert_tree_to_orm_departments(
    department_tree: aggregates.DepartmentTreeAggregate,
) -> list[models.Department]:
    def _flatten_department_node(  # noqa: WPS430  # allowed nested function
        current_node: aggregates.DepartmentTreeNode, parent_id: uuid.UUID | None
    ) -> list[models.Department]:
        """Recursively processes department nodes depth-first while tracking parents."""
        current_department = models.Department(
            id=current_node.id, title=current_node.title, parent_id=parent_id
        )

        flattened_departments = [current_department]
        for child_node in current_node.children:
            flattened_departments.extend(
                _flatten_department_node(child_node, parent_id=current_node.id)
            )

        return flattened_departments

    return _flatten_department_node(department_tree.root, parent_id=None)


def _build_department_trees(
    orm_departments: list[models.Department],
) -> list[aggregates.DepartmentTreeAggregate]:
    node_dict = {}
    for orm_department in orm_departments:
        node_dict[orm_department.id] = aggregates.DepartmentTreeNode(
            id=orm_department.id,
            title=orm_department.title,
            children=[],
        )

    for orm_department in orm_departments:
        if orm_department.parent_id is not None:
            node_dict[orm_department.parent_id].children.append(node_dict[orm_department.id])

    root_nodes = [node_dict[dept.id] for dept in orm_departments if dept.parent_id is None]
    return [aggregates.DepartmentTreeAggregate(root=root_node) for root_node in root_nodes]


class DepartmentTreeRepository(  # noqa: WPS215  # reason: explicit define implemented interfaces
    ports.GenericFetchPort[uuid.UUID, aggregates.DepartmentTreeAggregate],
):
    def __init__(self, department_gateway: gateways.DepartmentGateway) -> None:
        self._department_gateway = department_gateway

    @override
    async def fetch_one(self, department_id: uuid.UUID) -> aggregates.DepartmentTreeAggregate:
        tree_list = await self.fetch_all()
        for tree in tree_list:
            if department_id in tree:
                return tree
        raise domain_exceptions.DepartmentTreeNodeNotFoundError

    @override
    async def fetch_all(self) -> list[aggregates.DepartmentTreeAggregate]:
        orm_departments = await self._department_gateway.list()
        return _build_department_trees(orm_departments)
