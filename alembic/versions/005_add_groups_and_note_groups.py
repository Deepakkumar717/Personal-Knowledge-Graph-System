"""005_add_groups_and_note_groups

Revision ID: 005_add_groups_and_note_groups
Revises: 004_add_trash_and_activity_log
Create Date: 2026-10-11 15:16:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "005_add_groups_and_note_groups"
down_revision: Union[str, None] = "004_add_trash_and_activity_log"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "groups",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("color", sa.Text(), nullable=False),
        sa.Column("kind", sa.Text(), server_default="manual", nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.TIMESTAMP(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.CheckConstraint("kind IN ('auto', 'manual')", name="ck_groups_kind"),
    )
    op.create_index(
        "ix_groups_name_lower",
        "groups",
        [sa.text("lower(name)")],
        unique=True,
    )

    op.create_table(
        "note_groups",
        sa.Column("note_id", sa.Integer(), sa.ForeignKey("notes.id", ondelete="CASCADE"), primary_key=True, nullable=False),
        sa.Column("group_id", sa.Integer(), sa.ForeignKey("groups.id", ondelete="CASCADE"), nullable=False),
        sa.Column("source", sa.Text(), server_default="manual", nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.CheckConstraint("source IN ('auto', 'manual')", name="ck_note_groups_source"),
    )

    op.create_table(
        "dismissed_group_suggestions",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("note_id", sa.Integer(), sa.ForeignKey("notes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("group_id", sa.Integer(), sa.ForeignKey("groups.id", ondelete="CASCADE"), nullable=False),
        sa.Column("dismissed_at", sa.TIMESTAMP(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.UniqueConstraint("note_id", "group_id", name="uq_dismissed_group_suggestion"),
    )


def downgrade() -> None:
    op.drop_table("dismissed_group_suggestions")
    op.drop_table("note_groups")
    op.drop_index("ix_groups_name_lower", table_name="groups")
    op.drop_table("groups")
