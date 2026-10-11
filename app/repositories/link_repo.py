from typing import List, Optional, Set, Tuple
from sqlalchemy import text, and_
from sqlalchemy.orm import Session
from app.models.link import Link
from app.models.pending_link import PendingLink
from app.models.note import Note

class LinkRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_link(self, source_id: int, target_id: int) -> Optional[Link]:
        """Find a directed link from source to target."""
        return (
            self.db.query(Link)
            .filter(Link.source_id == source_id, Link.target_id == target_id)
            .first()
        )

    def add_link(self, source_id: int, target_id: int, origin: str = "manual") -> Link:
        """Add or update a directed link."""
        link = self.get_link(source_id, target_id)
        if link:
            # If it exists as auto and now manually linked, upgrade to manual
            if origin == "manual" and link.origin != "manual":
                link.origin = "manual"
                self.db.flush()
            return link

        link = Link(source_id=source_id, target_id=target_id, origin=origin)
        self.db.add(link)
        self.db.flush()
        return link

    def delete_link(self, source_id: int, target_id: int) -> bool:
        """Delete a directed link."""
        link = self.get_link(source_id, target_id)
        if link:
            self.db.delete(link)
            self.db.flush()
            return True
        return False

    def get_outgoing_links(self, source_id: int) -> List[Tuple[Link, Note]]:
        """Get all outgoing links for a note with target note details."""
        return (
            self.db.query(Link, Note)
            .join(Note, Link.target_id == Note.id)
            .filter(Link.source_id == source_id)
            .all()
        )

    def get_incoming_links(self, target_id: int) -> List[Tuple[Link, Note]]:
        """Get all incoming backlinks for a note with source note details."""
        return (
            self.db.query(Link, Note)
            .join(Note, Link.source_id == Note.id)
            .filter(Link.target_id == target_id)
            .all()
        )

    def get_all_links(self) -> List[Link]:
        """Get all links in the graph."""
        return self.db.query(Link).all()

    # --- Pending Links Operations ---

    def get_pending_links(self, source_id: int) -> List[str]:
        """Get all pending unresolved target title lower strings for a note."""
        rows = (
            self.db.query(PendingLink.target_title_lower)
            .filter(PendingLink.source_id == source_id)
            .all()
        )
        return [r[0] for r in rows]

    def set_pending_links(self, source_id: int, target_titles_lower: Set[str]) -> None:
        """Replace all pending links for a note."""
        self.db.query(PendingLink).filter(PendingLink.source_id == source_id).delete()
        for t_lower in target_titles_lower:
            pl = PendingLink(source_id=source_id, target_title_lower=t_lower)
            self.db.add(pl)
        self.db.flush()

    def find_pending_links_for_title(self, title_lower: str) -> List[PendingLink]:
        """Find all notes that have a pending unresolved link to title_lower."""
        return (
            self.db.query(PendingLink)
            .filter(PendingLink.target_title_lower == title_lower)
            .all()
        )

    def delete_pending_links_for_title(self, title_lower: str) -> None:
        """Delete pending links that match title_lower."""
        self.db.query(PendingLink).filter(PendingLink.target_title_lower == title_lower).delete()
        self.db.flush()

    def sync_auto_links(
        self,
        source_id: int,
        resolved_target_ids: Set[int],
        unresolved_titles_lower: Set[str],
    ) -> None:
        """
        Synchronize auto links and pending links for source_id:
        - Add new auto links for newly resolved targets.
        - Remove existing 'auto' links that are no longer in resolved_target_ids (never touch manual links!).
        - Update pending_links table.
        """
        # 1. Existing links from this note
        existing_links = self.db.query(Link).filter(Link.source_id == source_id).all()
        existing_by_target = {l.target_id: l for l in existing_links}

        # 2. Add or keep resolved links
        for target_id in resolved_target_ids:
            if target_id == source_id:
                continue
            if target_id in existing_by_target:
                # Link already exists; if manual, preserve manual
                pass
            else:
                new_auto_link = Link(source_id=source_id, target_id=target_id, origin="auto")
                self.db.add(new_auto_link)

        # 3. Remove auto links whose target is no longer referenced in resolved_target_ids
        for target_id, link in existing_by_target.items():
            if link.origin == "auto" and target_id not in resolved_target_ids:
                self.db.delete(link)

        # 4. Sync pending links
        self.set_pending_links(source_id, unresolved_titles_lower)
        self.db.flush()
