"""alter table employee

Revision ID: de1925bd6609
Revises: 8cf56b672ac4
Create Date: 2025-04-08 20:51:10.055622

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "de1925bd6609"
down_revision: Union[str, None] = "8cf56b672ac4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("employee", "manager_id", existing_type=sa.UUID(), nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("employee", "manager_id", existing_type=sa.UUID(), nullable=False)
    # ### end Alembic commands ###
