from uuid import UUID

import sqlalchemy as sa
from litestar.plugins.sqlalchemy import base
from sqlalchemy.orm import Mapped, mapped_column

_DEFAULT_VARCHAR_LENGTH = 255


class Base(base.UUIDAuditBase):
    """Base class for SQL Alchemy models."""

    __abstract__ = True


class Department(Base):
    __table_args__ = (sa.Index("ix_department_parent_id", "parent_id"),)

    title: Mapped[str] = mapped_column(sa.String(_DEFAULT_VARCHAR_LENGTH))
    parent_id: Mapped[UUID | None] = mapped_column(sa.ForeignKey("department.id"), nullable=True)
    head_id: Mapped[UUID | None] = mapped_column(sa.ForeignKey("employee.id"), nullable=True)


class Employee(Base):
    name: Mapped[str] = mapped_column(sa.String(_DEFAULT_VARCHAR_LENGTH))
    manager_id: Mapped[UUID | None] = mapped_column(sa.ForeignKey("employee.id"), nullable=True)
    department_id: Mapped[UUID] = mapped_column(sa.ForeignKey("department.id"))
