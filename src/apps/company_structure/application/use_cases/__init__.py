from apps.company_structure.application.use_cases.department_use_cases import (
    GetDepartmentTreeAsListUseCase,
)
from apps.company_structure.application.use_cases.generic_use_cases import (
    GenericCreateUseCase,
    GenericDeleteUseCase,
    GenericGetListUseCase,
    GenericGetPaginatedListUseCase,
    GenericGetUseCase,
    GenericUpdateUseCase,
)

__all__ = [
    # Generic
    "GenericCreateUseCase",
    "GenericDeleteUseCase",
    "GenericGetListUseCase",
    "GenericGetPaginatedListUseCase",
    "GenericGetUseCase",
    "GenericUpdateUseCase",
    # Department
    "GetDepartmentTreeAsListUseCase",
]
