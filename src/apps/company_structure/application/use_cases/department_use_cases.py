import uuid
from abc import abstractmethod

from apps.company_structure.application import schemas


class GetDepartmentTreeAsListUseCase:
    @abstractmethod
    async def get_one_as_list(self, root_id: uuid.UUID) -> list[schemas.DepartmentSchema]:
        raise NotImplementedError
