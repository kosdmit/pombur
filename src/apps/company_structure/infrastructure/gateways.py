from abc import ABC
from collections.abc import Sequence
from typing import final, TypeVar

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from apps.company_structure.infrastructure import models


OrmModel = TypeVar("OrmModel", bound=models.Base)


class GenericGateway[OrmModel](ABC):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def fetch_all(self) -> Sequence[OrmModel]:
        raise NotImplementedError

    async def save(self, obj: OrmModel) -> None:
        raise NotImplementedError


@final
class DepartmentGateway(GenericGateway[models.Department]):
    async def fetch_all(self) -> Sequence[models.Department]:
        result = await self._session.execute(
            sa.select(models.Department).order_by(models.Department.title)
        )
        return result.scalars().all()
