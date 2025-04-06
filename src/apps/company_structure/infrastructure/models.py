from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Department(Base):
    __tablename__ = "department"

    id: Mapped[UUID] = mapped_column(sa.Uuid, primary_key=True)
    title: Mapped[str] = mapped_column(sa.String(255))
    parent_id: Mapped[UUID] = mapped_column(sa.ForeignKey("department.id"))
