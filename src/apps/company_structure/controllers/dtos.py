from typing import Literal

from litestar.dto import DataclassDTO, DTOConfig

from apps.company_structure.domain import entities

_RENAME_STRATEGY: Literal["camel"] = "camel"


class ReadDepartmentDTO(DataclassDTO[entities.DepartmentEntity]):
    config = DTOConfig(rename_strategy=_RENAME_STRATEGY)


class ReadRootDepartmentDTO(DataclassDTO[entities.RootDepartmentEntity]):
    config = DTOConfig(rename_strategy=_RENAME_STRATEGY)


class WriteDepartmentDTO(DataclassDTO[entities.DepartmentEntity]):
    config = DTOConfig(exclude={"id"}, rename_strategy=_RENAME_STRATEGY)


class PatchDepartmentDTO(DataclassDTO[entities.DepartmentEntity]):
    config = DTOConfig(exclude={"id"}, partial=True, rename_strategy=_RENAME_STRATEGY)


class ReadEmployeeDTO(DataclassDTO[entities.EmployeeEntity]):
    config = DTOConfig(max_nested_depth=1, rename_strategy=_RENAME_STRATEGY)


class WriteEmployeeDTO(DataclassDTO[entities.EmployeeEntity]):
    config = DTOConfig(exclude={"id"}, max_nested_depth=0, rename_strategy=_RENAME_STRATEGY)
