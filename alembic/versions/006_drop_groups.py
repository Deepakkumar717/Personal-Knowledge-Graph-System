"""006_drop_groups

Revision ID: 006_drop_groups
Revises: 005_add_groups_and_note_groups
Create Date: 2026-10-11 16:48:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "006_drop_groups"
down_revision: Union[str, None] = "005_add_groups_and_note_groups"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop group-related tables cleanly
    op.execute("DROP TABLE IF EXISTS note_groups")
    op.execute("DROP TABLE IF EXISTS dismissed_group_suggestions")
    op.execute("DROP TABLE IF EXISTS groups")


def downgrade() -> None:
    pass
