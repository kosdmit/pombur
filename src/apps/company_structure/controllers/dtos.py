from typing import Literal

from litestar.dto import DataclassDTO, DTOConfig
from litestar.plugins.pydantic import PydanticDTO

from apps.company_structure.application import schemas
from apps.company_structure.domain import entities

_RENAME_STRATEGY: Literal["camel"] = "camel"


class ReadDepartmentDTO(PydanticDTO[schemas.DepartmentSchema]):
    config = DTOConfig(rename_strategy=_RENAME_STRATEGY)


class WriteDepartmentDTO(PydanticDTO[schemas.DepartmentSchema]):
    config = DTOConfig(exclude={"id"}, rename_strategy=_RENAME_STRATEGY)


class PatchDepartmentDTO(PydanticDTO[schemas.DepartmentSchema]):
    config = DTOConfig(exclude={"id"}, partial=True, rename_strategy=_RENAME_STRATEGY)


class ReadEmployeeDTO(DataclassDTO[entities.EmployeeEntity]):
    config = DTOConfig(max_nested_depth=1, rename_strategy=_RENAME_STRATEGY)


class WriteEmployeeDTO(DataclassDTO[entities.EmployeeEntity]):
    config = DTOConfig(exclude={"id"}, max_nested_depth=0, rename_strategy=_RENAME_STRATEGY)
