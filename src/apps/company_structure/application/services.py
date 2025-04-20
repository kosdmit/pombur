import builtins
import uuid
from typing import override

from litestar.dto import DTOData
from litestar.repository import filters

from apps.company_structure.application import ports, schemas, use_cases
from apps.company_structure.domain import aggregates, entities


class DepartmentTreeNotFoundError(Exception):
    def __init__(self, root_department_id: uuid.UUID) -> None:
        super().__init__(f"Department tree with root id {root_department_id} not found")


def _convert_department_tree_to_list(
    department_tree: aggregates.DepartmentTreeAggregate,
) -> list[schemas.DepartmentSchema]:
    def _flatten_department_node(  # noqa: WPS430  # allowed nested function
        current_node: aggregates.DepartmentTreeNode, parent_id: uuid.UUID | None
    ) -> list[schemas.DepartmentSchema]:
        """Recursively processes department nodes depth-first while tracking parents."""
        current_department = schemas.DepartmentSchema(
            id=current_node.id, title=current_node.title, parent_id=parent_id
        )

        flattened_departments = [current_department]
        for child_node in current_node.children:
            flattened_departments.extend(
                _flatten_department_node(child_node, parent_id=current_node.id)
            )

        return flattened_departments

    return _flatten_department_node(department_tree.root, parent_id=None)


def _convert_department_data_to_tree_node(
    department_data: schemas.DepartmentSchema,
) -> aggregates.DepartmentTreeNode:
    return aggregates.DepartmentTreeNode(
        id=department_data.id,
        title=department_data.title,
        children=[],
    )


class DepartmentTreeService(  # noqa: WPS215  # reason: explicit define implemented interfaces
    use_cases.GenericGetUseCase[uuid.UUID, aggregates.DepartmentTreeAggregate],
    use_cases.GenericGetListUseCase[aggregates.DepartmentTreeAggregate],
):
    def __init__(
        self,
        fetch_port: ports.GenericFetchPort[uuid.UUID, aggregates.DepartmentTreeAggregate],
    ) -> None:
        self._fetch_port = fetch_port

    @override
    async def get_list(self) -> list[aggregates.DepartmentTreeAggregate]:
        return await self._fetch_port.fetch_all()

    @override
    async def get(self, root_department_id: uuid.UUID) -> aggregates.DepartmentTreeAggregate:
        tree_list = await self._fetch_port.fetch_all()
        for tree in tree_list:
            if root_department_id == tree.root.id:
                return tree
        raise DepartmentTreeNotFoundError(root_department_id)


class DepartmentService(  # noqa: WPS215  # reason: explicit define implemented interfaces
    use_cases.GenericGetListUseCase[schemas.DepartmentListSchema],
    use_cases.GenericGetUseCase[uuid.UUID, schemas.DepartmentSchema],
    use_cases.GenericCreateUseCase[schemas.DepartmentSchema],
    use_cases.GenericUpdateUseCase[uuid.UUID, schemas.DepartmentSchema],
    use_cases.GenericDeleteUseCase[uuid.UUID],
):
    def __init__(
        self,
        fetch_port: ports.GenericFetchPort[uuid.UUID, schemas.DepartmentSchema],
        fetch_aggregate_port: ports.GenericFetchPort[uuid.UUID, aggregates.DepartmentTreeAggregate],
        save_port: ports.GenericSavePort[schemas.DepartmentSchema],
        delete_port: ports.GenericDeletePort[uuid.UUID],
    ) -> None:
        self._fetch_port = fetch_port
        self._fetch_aggregate_port = fetch_aggregate_port
        self._save_port = save_port
        self._delete_port = delete_port

    @override
    async def get_list(self) -> list[schemas.DepartmentListSchema]:
        tree_list = await self._fetch_aggregate_port.fetch_all()
        return [
            schemas.DepartmentListSchema.model_validate(_convert_department_tree_to_list(tree))
            for tree in tree_list
        ]

    @override
    async def create(
        self,
        input_data: DTOData[schemas.DepartmentSchema],
    ) -> schemas.DepartmentSchema:
        department_data = input_data.create_instance(id=uuid.uuid4())
        if department_data.parent_id is not None:
            department_tree = await self._fetch_aggregate_port.fetch_one(department_data.parent_id)
            department_tree.add_child(
                parent_id=department_data.parent_id,
                child=_convert_department_data_to_tree_node(department_data),
            )
        await self._save_port.save(department_data)
        return department_data

    @override
    async def update(
        self,
        department_id: uuid.UUID,
        department_data: DTOData[schemas.DepartmentSchema],
    ) -> schemas.DepartmentSchema:
        department_entity_to_update = await self._fetch_port.fetch_one(department_id)
        updated_department_entity = department_data.update_instance(department_entity_to_update)
        await self._save_port.save(updated_department_entity)
        return updated_department_entity

    @override
    async def delete(self, department_id: uuid.UUID) -> None:
        department_tree = await self._fetch_aggregate_port.fetch_one(department_id)
        department_tree.remove_if_has_no_children(department_id)
        await self._delete_port.delete(department_id)


class EmployeeService(  # noqa: WPS215  # reason: explicit define implemented interfaces
    use_cases.GenericGetUseCase[str, entities.EmployeeEntity],
    use_cases.GenericGetListUseCase[entities.EmployeeEntity],
    use_cases.GenericCreateUseCase[entities.EmployeeEntity],
    use_cases.GenericGetPaginatedListUseCase[entities.EmployeeEntity],
):
    def __init__(
        self,
        fetch_port: ports.GenericFetchPort[str, entities.EmployeeEntity],
        save_port: ports.GenericSavePort[entities.EmployeeEntity],
    ) -> None:
        self._fetch_port = fetch_port
        self._save_port = save_port

    @override
    async def get(self, slug: str) -> entities.EmployeeEntity:
        return await self._fetch_port.fetch_one(slug)

    @override
    async def get_list(self) -> list[entities.EmployeeEntity]:
        return await self._fetch_port.fetch_all()

    @override
    async def paginated_list(
        self,
        limit_offset: filters.LimitOffset,
    ) -> tuple[builtins.list[entities.EmployeeEntity], int]:
        return await self._fetch_port.fetch_page(limit_offset)

    @override
    async def create(
        self, entity_data: DTOData[entities.EmployeeEntity]
    ) -> entities.EmployeeEntity:
        employee_entity = entity_data.create_instance(id=uuid.uuid4())
        await self._save_port.save(employee_entity)
        return employee_entity
