import uuid
from collections.abc import Iterator
from dataclasses import dataclass

from apps.company_structure.domain import exceptions as domain_exceptions


@dataclass
class DepartmentTreeNode:
    id: uuid.UUID
    title: str
    children: list["DepartmentTreeNode"]


@dataclass
class DepartmentTreeAggregate:
    root: DepartmentTreeNode

    def __iter__(self) -> Iterator[DepartmentTreeNode]:
        stack = [self.root]
        while stack:
            node = stack.pop()
            yield node
            stack.extend(node.children)

    def __contains__(self, node_id: uuid.UUID, /) -> bool:
        return any(node.id == node_id for node in self)

    def __len__(self) -> int:
        return len(list(self))

    def __getitem__(self, node_id: uuid.UUID) -> DepartmentTreeNode:
        for node in self:
            if node.id == node_id:
                return node
        raise domain_exceptions.DepartmentTreeNodeNotFoundError

    def remove_if_has_no_children(self, node_id: uuid.UUID) -> None:
        node = self[node_id]
        if node.children:
            raise domain_exceptions.ForbiddenDeleteDepartmentWithChildrenError
        self._remove_department(node_id)

    def remove_with_children(self, node_id: uuid.UUID) -> None:
        self._remove_department(node_id)

    def add_child(self, parent_id: uuid.UUID, child: DepartmentTreeNode) -> None:
        parent = self[parent_id]
        parent.children.append(child)

    def _find_parent(self, node_id: uuid.UUID, /) -> DepartmentTreeNode:
        for node in self:
            for child in node.children:
                if child.id == node_id:
                    return node
        raise domain_exceptions.DepartmentTreeNodeNotFoundError

    def _remove_department(self, node_id: uuid.UUID) -> None:
        node = self[node_id]
        if node is self.root:
            raise domain_exceptions.ForbiddenDeleteRootDepartmentError
        parent = self._find_parent(node_id)
        parent.children.remove(node)
