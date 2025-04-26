from litestar.dto import DataclassDTO, DTOConfig
from litestar.plugins.pydantic import PydanticDTO

from apps.company_structure.application import schemas
from apps.company_structure.domain import entities


class WriteDepartmentDTO(PydanticDTO[schemas.DepartmentSchema]):
    config = DTOConfig(exclude={"id"})


class PatchDepartmentDTO(PydanticDTO[schemas.DepartmentSchema]):
    config = DTOConfig(exclude={"id"}, partial=True)


class ReadEmployeeDTO(DataclassDTO[entities.EmployeeEntity]):
    config = DTOConfig(max_nested_depth=1)


class WriteEmployeeDTO(DataclassDTO[entities.EmployeeEntity]):
    config = DTOConfig(exclude={"id"}, max_nested_depth=0)
