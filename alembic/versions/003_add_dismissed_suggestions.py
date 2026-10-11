"""003_add_dismissed_suggestions

Revision ID: 003_add_dismissed_suggestions
Revises: 002_add_fts_origins_pending
Create Date: 2026-10-11 13:30:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "003_add_dismissed_suggestions"
down_revision: Union[str, None] = "002_add_fts_origins_pending"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "dismissed_suggestions",
        sa.Column("note_id", sa.Integer(), sa.ForeignKey("notes.id", ondelete="CASCADE"), primary_key=True, nullable=False),
        sa.Column("other_id", sa.Integer(), sa.ForeignKey("notes.id", ondelete="CASCADE"), primary_key=True, nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("dismissed_suggestions")
