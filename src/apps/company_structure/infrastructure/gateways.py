from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import TypeVar, final

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from apps.company_structure.infrastructure import models

OrmModel = TypeVar("OrmModel", bound=models.Base)


class GenericGateway[OrmModel](ABC):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @abstractmethod
    async def fetch_all(self) -> Sequence[OrmModel]:
        """Fetch all records from the database.

        Returns:
            Sequence[OrmModel]: A sequence of ORM models.
        """
        raise NotImplementedError

    @abstractmethod
    async def save(self, orm_obj: OrmModel) -> None:
        """Save the object to the database.

        Args:
            orm_obj (OrmModel): The ORM model to save.
        """
        raise NotImplementedError


@final
class DepartmentGateway(GenericGateway[models.Department]):
    async def fetch_all(self) -> Sequence[models.Department]:
        query_result = await self._session.execute(
            sa.select(models.Department).order_by(models.Department.title),
        )
        return query_result.scalars().all()

    async def save(self, orm_obj: models.Department) -> None:
        await self._session.merge(orm_obj)
