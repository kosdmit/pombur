"""alter table department

Revision ID: 9fe3e41b620c
Revises: 2e5d9b672e80
Create Date: 2025-04-07 17:56:05.138888

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "9fe3e41b620c"
down_revision: Union[str, None] = "2e5d9b672e80"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "department",
        "created_at",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=False,
    )
    op.alter_column(
        "department",
        "updated_at",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "department", "updated_at", existing_type=postgresql.TIMESTAMP(timezone=True), nullable=True
    )
    op.alter_column(
        "department", "created_at", existing_type=postgresql.TIMESTAMP(timezone=True), nullable=True
    )
    # ### end Alembic commands ###
