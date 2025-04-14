from typing import Any, override

import sqlalchemy as sa
from litestar.plugins.sqlalchemy import repository as litestar_repository

from apps.company_structure.infrastructure import models


class RootDepartmentDoesNotExistError(Exception):
    def __init__(self) -> None:
        super().__init__(
            "Root department does not exist in the database. "
            "It must be created then db initialized."
        )


class GottenMoreThanOneRootDepartmentError(Exception):
    def __init__(self) -> None:
        super().__init__("More than one root department fetched from the database.")


class DepartmentGateway(litestar_repository.SQLAlchemyAsyncRepository[models.Department]):
    model_type = models.Department

    @override
    async def list(self, *args: Any, **kwargs: Any) -> list[models.Department]:
        return await super().list(
            sa.and_(models.Department.parent_id != None),  # noqa: E711  # reason: alchemy syntax
            *args,
            **kwargs,
        )

    async def fetch_root_department(self) -> models.Department:
        query_result = await self.session.execute(
            sa.select(models.Department).where(models.Department.parent_id == None),  # noqa: E711  # reason: alchemy syntax
        )
        departments = query_result.scalars().all()

        if len(departments) > 1:
            raise GottenMoreThanOneRootDepartmentError
        if not departments:
            raise RootDepartmentDoesNotExistError

        return departments[0]


class EmployeeGateway(litestar_repository.SQLAlchemyAsyncSlugRepository[models.Employee]):
    model_type = models.Employee
