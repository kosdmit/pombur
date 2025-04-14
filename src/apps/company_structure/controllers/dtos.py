from litestar.dto import DataclassDTO, DTOConfig

from apps.company_structure.domain import entities


class ReadDepartmentDTO(DataclassDTO[entities.DepartmentEntity]):
    """DTO for department entity.

    Converts entities.DepartmentEntity to serialization ready data.
    """


class WriteDepartmentDTO(DataclassDTO[entities.DepartmentEntity]):
    config = DTOConfig(exclude={"id"})


class PatchDepartmentDTO(DataclassDTO[entities.DepartmentEntity]):
    config = DTOConfig(exclude={"id"}, partial=True)


class ReadEmployeeDTO(DataclassDTO[entities.EmployeeEntity]):
    """DTO for employee entity.

    Converts entities.EmployeeEntity to serialization ready data.
    """

    config = DTOConfig(max_nested_depth=1)


class WriteEmployeeDTO(DataclassDTO[entities.EmployeeEntity]):
    config = DTOConfig(exclude={"id"}, max_nested_depth=0)
