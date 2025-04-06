from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

_DEFAULT_VARCHAR_LENGTH = 255


class Base(DeclarativeBase):
    """Base class for SQL Alchemy models."""


class Department(Base):
    __tablename__ = "department"

    id: Mapped[UUID] = mapped_column(sa.Uuid, primary_key=True)
    title: Mapped[str] = mapped_column(sa.String(_DEFAULT_VARCHAR_LENGTH))
    parent_id: Mapped[UUID] = mapped_column(sa.ForeignKey("department.id"))
