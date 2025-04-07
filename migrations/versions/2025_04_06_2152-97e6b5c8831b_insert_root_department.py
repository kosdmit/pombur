"""insert root department

Revision ID: 97e6b5c8831b
Revises: 0a6a2f02b8ba
Create Date: 2025-04-06 21:52:27.092334

"""

import uuid
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "97e6b5c8831b"
down_revision: Union[str, None] = "0a6a2f02b8ba"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# Fixed UUID for the root department (for idempotency)
ROOT_DEPARTMENT_ID = uuid.UUID("00000000-0000-0000-0000-000000000000")
ROOT_TITLE = "root"


def upgrade() -> None:
    """Upgrade schema."""
    conn = op.get_bind()
    exists = conn.scalar(
        sa.text("SELECT 1 FROM department WHERE id = :id"), {"id": ROOT_DEPARTMENT_ID}
    )
    if not exists:
        op.execute(
            sa.text(
                """
                INSERT INTO department (id, title, parent_id)
                VALUES (:id, :title, NULL)
                """
            ).bindparams(id=ROOT_DEPARTMENT_ID, title=ROOT_TITLE)
        )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(sa.text("DELETE FROM department WHERE id = :id").bindparams(id=ROOT_DEPARTMENT_ID))
