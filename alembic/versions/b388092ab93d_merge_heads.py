"""merge heads

Revision ID: b388092ab93d
Revises: 001, 8644b2dbb429
Create Date: 2026-06-14 13:54:07.539051

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b388092ab93d'
down_revision: Union[str, Sequence[str], None] = ('001', '8644b2dbb429')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
