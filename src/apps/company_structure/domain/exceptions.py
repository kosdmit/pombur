from abc import ABC


class ForbiddenDeleteDepartmentError(Exception, ABC):
    """Base class for exceptions raised when department can't be deleted.

    Useful to catch inherited exceptions.
    """


class ForbiddenDeleteRootDepartmentError(ForbiddenDeleteDepartmentError):
    def __init__(self) -> None:
        super().__init__("Cannot delete root node")


class ForbiddenDeleteDepartmentWithChildrenError(ForbiddenDeleteDepartmentError):
    def __init__(self) -> None:
        super().__init__("Cannot delete department with children")


class DepartmentTreeNodeNotFoundError(Exception):
    def __init__(self) -> None:
        super().__init__("Department tree node not found")
