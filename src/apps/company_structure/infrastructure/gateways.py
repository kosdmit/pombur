import uuid
from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import TypeVar, final, override

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
    async def fetch_one(self, obj_id: uuid.UUID) -> OrmModel:
        """Fetch one record from the database.

        Args:
            obj_id (uuid.UUID): A primary key of the object to fetch.

        Returns:
            OrmModel: The ORM model of the fetched object.
        """
        raise NotImplementedError

    @abstractmethod
    async def save(self, orm_obj: OrmModel) -> None:
        """Save the object to the database.

        Args:
            orm_obj (OrmModel): The ORM model to save.
        """
        raise NotImplementedError

    @abstractmethod
    async def delete(self, obj_id: uuid.UUID) -> None:
        """Delete the object from the database.

        Args:
            obj_id (uuid.UUID): A primary key of the object to delete.
        """
        raise NotImplementedError


class RootDepartmentDoesNotExistError(Exception):
    def __init__(self) -> None:
        super().__init__(
            "Root department does not exist in the database. "
            "It must be created then db initialized."
        )


class GottenMoreThanOneRootDepartmentError(Exception):
    def __init__(self) -> None:
        super().__init__("More than one root department fetched from the database.")


@final
class DepartmentGateway(GenericGateway[models.Department]):
    @override
    async def fetch_all(self) -> Sequence[models.Department]:
        query_result = await self._session.execute(
            sa.select(models.Department).order_by(models.Department.title),
        )
        return query_result.scalars().all()

    @override
    async def fetch_one(self, obj_id: uuid.UUID) -> models.Department:
        query_result = await self._session.execute(
            sa.select(models.Department).where(models.Department.id == obj_id),
        )
        return query_result.scalars().one()

    @override
    async def save(self, orm_obj: models.Department) -> None:
        await self._session.merge(orm_obj)

    async def fetch_root_department(self) -> models.Department:
        query_result = await self._session.execute(
            sa.select(models.Department).where(models.Department.parent_id == None),  # noqa: E711  # reason: alchemy syntax
        )

        if len(query_result.scalars().all()) > 1:
            raise GottenMoreThanOneRootDepartmentError
        if len(query_result.scalars().all()) == 0:
            raise RootDepartmentDoesNotExistError

        return query_result.scalars().one()

    @override
    async def delete(self, obj_id: uuid.UUID) -> None:
        await self._session.execute(
            sa.delete(models.Department).where(models.Department.id == obj_id),
        )
