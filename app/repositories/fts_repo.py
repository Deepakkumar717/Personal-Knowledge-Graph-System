import re
from typing import List, Dict, Any, Optional, Tuple
from sqlalchemy import text
from sqlalchemy.orm import Session

# FTS query cleaner
FTS_SPECIAL_CHARS = re.compile(r'["\*\^:\(\)\{\}\[\]\~\+\-\/]')

class FTSRepository:
    def __init__(self, db: Session):
        self.db = db

    def sync_note_fts(self, note_id: int, title: str, content: str, tag_names: List[str]) -> None:
        """Upsert a note into the FTS5 virtual table."""
        tags_str = " ".join(tag_names)
        # SQLite FTS5 delete old if exists then insert
        self.db.execute(
            text("DELETE FROM notes_fts WHERE rowid = :note_id;"),
            {"note_id": note_id},
        )
        self.db.execute(
            text(
                "INSERT INTO notes_fts(rowid, title, content, tags) "
                "VALUES (:note_id, :title, :content, :tags);"
            ),
            {"note_id": note_id, "title": title, "content": content or "", "tags": tags_str},
        )

    def delete_note_fts(self, note_id: int) -> None:
        """Remove a note from the FTS5 virtual table."""
        self.db.execute(
            text("DELETE FROM notes_fts WHERE rowid = :note_id;"),
            {"note_id": note_id},
        )

    def search_fts(
        self,
        query: str,
        tag_filter: Optional[str] = None,
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        """
        Execute FTS5 search with bm25 ranking and snippet generation.
        Supports multi-word prefix search and column weights: title=10.0, content=1.0, tags=5.0.
        """
        if not query and not tag_filter:
            return []

        fts_clauses = []

        # Parse query words and escape special characters
        if query:
            raw_words = query.strip().split()
            word_clauses = []
            for w in raw_words:
                if w.startswith("#"):
                    # Tag specified in query
                    tag_name = FTS_SPECIAL_CHARS.sub("", w[1:]).strip()
                    if tag_name:
                        word_clauses.append(f'tags: {tag_name}*')
                else:
                    clean_w = FTS_SPECIAL_CHARS.sub("", w).strip()
                    if clean_w:
                        word_clauses.append(f'{clean_w}*')
            if word_clauses:
                fts_clauses.append(" AND ".join(word_clauses))

        if tag_filter:
            clean_tag = FTS_SPECIAL_CHARS.sub("", tag_filter).strip()
            if clean_tag:
                fts_clauses.append(f'tags: {clean_tag}*')

        if not fts_clauses:
            return []

        match_expression = " AND ".join(f"({c})" for c in fts_clauses)

        sql = text("""
            SELECT 
                notes_fts.rowid AS id,
                notes_fts.title AS title,
                snippet(notes_fts, 1, '<mark>', '</mark>', '...', 20) AS snippet,
                notes_fts.tags AS tags_str,
                bm25(notes_fts, 10.0, 1.0, 5.0) AS rank
            FROM notes_fts
            WHERE notes_fts MATCH :match_expr
            ORDER BY rank ASC
            LIMIT :limit;
        """)

        try:
            result = self.db.execute(sql, {"match_expr": match_expression, "limit": limit})
            rows = result.fetchall()
            items = []
            for r in rows:
                items.append({
                    "id": r.id,
                    "title": r.title,
                    "snippet": r.snippet if r.snippet else "",
                    "tags": [t for t in (r.tags_str or "").split() if t],
                    "score": round(abs(float(r.rank)), 4),
                    "match_type": "fts",
                })
            return items
        except Exception:
            # If FTS syntax error on malformed inputs, return empty for fallback
            return []
