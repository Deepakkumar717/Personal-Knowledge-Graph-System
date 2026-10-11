"""002_add_fts_origins_pending

Revision ID: 002_add_fts_origins_pending
Revises: 001_initial_schema
Create Date: 2026-10-10 00:01:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "002_add_fts_origins_pending"
down_revision: Union[str, None] = "001_initial_schema"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. links.origin TEXT NOT NULL DEFAULT 'manual'
    with op.batch_alter_table("links") as batch_op:
        batch_op.add_column(
            sa.Column("origin", sa.Text(), nullable=False, server_default="manual")
        )

    # 2. notes.updated_at TIMESTAMP, notes.pinned INTEGER DEFAULT 0
    with op.batch_alter_table("notes") as batch_op:
        batch_op.add_column(
            sa.Column("updated_at", sa.TIMESTAMP(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=True)
        )
        batch_op.add_column(
            sa.Column("pinned", sa.Integer(), nullable=False, server_default="0")
        )

    # 3. unique index on lower(title) for case-insensitive title uniqueness
    op.execute("CREATE UNIQUE INDEX IF NOT EXISTS ix_notes_title_lower ON notes (lower(title));")

    # 4. FTS5 virtual table notes_fts(title, content, tags)
    op.execute(
        "CREATE VIRTUAL TABLE IF NOT EXISTS notes_fts USING fts5("
        "title, content, tags, tokenize = 'unicode61'"
        ");"
    )

    # 5. table pending_links(source_id, target_title_lower, PRIMARY KEY (source_id, target_title_lower))
    op.create_table(
        "pending_links",
        sa.Column("source_id", sa.Integer(), nullable=False),
        sa.Column("target_title_lower", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(["source_id"], ["notes.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("source_id", "target_title_lower"),
    )


def downgrade() -> None:
    op.drop_table("pending_links")
    op.execute("DROP TABLE IF EXISTS notes_fts;")
    op.execute("DROP INDEX IF EXISTS ix_notes_title_lower;")

    with op.batch_alter_table("notes") as batch_op:
        batch_op.drop_column("pinned")
        batch_op.drop_column("updated_at")

    with op.batch_alter_table("links") as batch_op:
        batch_op.drop_column("origin")
