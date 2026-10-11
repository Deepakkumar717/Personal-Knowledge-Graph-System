from typing import Dict, Any, List
from datetime import datetime
from sqlalchemy.orm import Session
from app.repositories.note_repo import NoteRepository
from app.repositories.tag_repo import TagRepository
from app.repositories.link_repo import LinkRepository
from app.repositories.fts_repo import FTSRepository
from app.services.note_service import NoteService
from app.schemas.note import NoteCreate

class IOService:
    def __init__(self, db: Session):
        self.db = db
        self.note_repo = NoteRepository(db)
        self.tag_repo = TagRepository(db)
        self.link_repo = LinkRepository(db)
        self.fts_repo = FTSRepository(db)
        self.note_service = NoteService(db)

    def export_data(self) -> Dict[str, Any]:
        """Export full knowledge graph data to JSON format."""
        all_notes = self.note_repo.get_all_notes_full()
        all_links = self.link_repo.get_all_links()
        all_tags = self.tag_repo.get_all_tags_with_counts()

        notes_data = []
        for n in all_notes:
            notes_data.append({
                "id": n.id,
                "title": n.title,
                "content": n.content,
                "tags": [t.name for t in n.tags],
                "pinned": bool(n.pinned),
                "created_at": n.created_at.isoformat() if n.created_at else None,
                "updated_at": n.updated_at.isoformat() if n.updated_at else None,
            })

        links_data = []
        for l in all_links:
            links_data.append({
                "source_id": l.source_id,
                "target_id": l.target_id,
                "origin": l.origin,
            })

        tags_data = [{"id": t.id, "name": t.name, "count": count} for t, count in all_tags]

        return {
            "version": "1.0",
            "exported_at": datetime.utcnow().isoformat(),
            "notes": notes_data,
            "tags": tags_data,
            "links": links_data,
        }

    def import_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Import notes, tags, and links from JSON.
        Validates content, skips duplicate note titles, creates notes and manual links,
        and returns a detailed summary.
        """
        imported_notes_count = 0
        skipped_notes_count = 0
        imported_links_count = 0
        skipped_links_count = 0
        errors = []

        notes_payload = data.get("notes", [])
        id_mapping: Dict[int, int] = {}  # old_id -> new_id

        for note_item in notes_payload:
            title = (note_item.get("title") or "").strip()
            content = note_item.get("content") or ""
            tags = note_item.get("tags") or []
            old_id = note_item.get("id")

            if not title:
                errors.append("Skipped note with empty title.")
                skipped_notes_count += 1
                continue

            existing = self.note_repo.get_by_title_lower(title)
            if existing:
                skipped_notes_count += 1
                if old_id:
                    id_mapping[old_id] = existing.id
                continue

            try:
                new_note = self.note_service.create_note(
                    NoteCreate(title=title, content=content, tags=tags)
                )
                imported_notes_count += 1
                if old_id:
                    id_mapping[old_id] = new_note.id
            except Exception as e:
                errors.append(f"Error importing note '{title}': {str(e)}")
                skipped_notes_count += 1

        # Import manual links
        links_payload = data.get("links", [])
        for link_item in links_payload:
            old_src = link_item.get("source_id")
            old_tgt = link_item.get("target_id")
            origin = link_item.get("origin", "manual")

            new_src = id_mapping.get(old_src)
            new_tgt = id_mapping.get(old_tgt)

            if not new_src or not new_tgt or new_src == new_tgt:
                skipped_links_count += 1
                continue

            # Only import manual links explicitly (auto links are already resolved by wikilink sync)
            if origin == "manual":
                existing = self.link_repo.get_link(new_src, new_tgt)
                if not existing:
                    self.link_repo.add_link(new_src, new_tgt, origin="manual")
                    imported_links_count += 1
                else:
                    skipped_links_count += 1

        self.db.commit()

        return {
            "status": "success",
            "imported_notes": imported_notes_count,
            "skipped_notes": skipped_notes_count,
            "imported_links": imported_links_count,
            "skipped_links": skipped_links_count,
            "errors": errors,
        }

    def reset_database(self, confirm: str = "DELETE ALL") -> Dict[str, Any]:
        """Clear all notes, tags, links, pending links, and FTS index after taking a safety backup."""
        from sqlalchemy import text
        from app.nlp.tfidf import tfidf_engine
        from app.services.backup_service import backup_service
        from app.repositories.activity_repo import ActivityRepository
        from app.core.exceptions import ValidationException

        if confirm != "DELETE ALL":
            raise ValidationException("Reset confirmation required. Payload must contain confirm: 'DELETE ALL'.")

        # Always take an automatic backup before clearing
        backup_service.create_backup(reason="pre_reset")

        self.db.execute(text("DELETE FROM trash;"))
        self.db.execute(text("DELETE FROM dismissed_suggestions;"))
        self.db.execute(text("DELETE FROM pending_links;"))
        self.db.execute(text("DELETE FROM links;"))
        self.db.execute(text("DELETE FROM note_tags;"))
        self.db.execute(text("DELETE FROM tags;"))
        self.db.execute(text("DELETE FROM notes;"))
        self.db.execute(text("DELETE FROM notes_fts;"))
        self.db.commit()

        # Log reset action
        activity_repo = ActivityRepository(self.db)
        activity_repo.log(
            action="reset",
            entity="system",
            title="Database Reset",
            detail="All notes and tags cleared after safety backup.",
        )
        self.db.commit()

        tfidf_engine.invalidate()
        return {"status": "success", "message": "Database successfully reset to empty state after safety backup."}
