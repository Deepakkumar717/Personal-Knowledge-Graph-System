import re
from typing import List, Optional, Tuple, Dict, Any
from sqlalchemy.orm import Session
from app.repositories.fts_repo import FTSRepository
from app.repositories.note_repo import NoteRepository
from app.repositories.tag_repo import TagRepository
from app.schemas.search import (
    SearchResultItem,
    SearchResponse,
    AutocompleteItem,
    AutocompleteResponse,
    TitleSuggestItem,
    TitleSuggestResponse,
)
from app.nlp.fuzzy import find_fuzzy_matches, fuzzy_score

class SearchService:
    def __init__(self, db: Session):
        self.db = db
        self.fts_repo = FTSRepository(db)
        self.note_repo = NoteRepository(db)
        self.tag_repo = TagRepository(db)

    def search(
        self,
        query: str = "",
        tag: Optional[str] = None,
        limit: int = 50,
    ) -> SearchResponse:
        """
        Ranked full-text search with snippet highlights and fuzzy fallback.
        Supports:
        - #tag query syntax
        - prefix matching
        - bm25 ranking (title > tags > content)
        - fuzzy typo fallback if FTS returns 0 or few results
        """
        clean_q = query.strip()
        fts_results = self.fts_repo.search_fts(clean_q, tag_filter=tag, limit=limit)

        items: List[SearchResultItem] = [
            SearchResultItem(
                id=r["id"],
                title=r["title"],
                snippet=r["snippet"],
                tags=r["tags"],
                score=r["score"],
                match_type="fts",
            )
            for r in fts_results
        ]

        # If FTS returned fewer than 3 results and query has non-tag terms, run fuzzy fallback
        non_tag_query = " ".join([w for w in clean_q.split() if not w.startswith("#")]).strip()
        if len(items) < 3 and non_tag_query:
            existing_ids = {item.id for item in items}
            all_notes = self.note_repo.get_all_notes_full()

            candidates = [
                (n, f"{n.title} {' '.join([t.name for t in n.tags])}")
                for n in all_notes if n.id not in existing_ids
            ]
            fuzzy_matches = find_fuzzy_matches(non_tag_query, candidates, threshold=0.55, limit=limit - len(items))

            for note, score in fuzzy_matches:
                # Generate simple snippet from content
                c_str = note.content or ""
                snippet = c_str[:120] + ("..." if len(c_str) > 120 else "")
                items.append(
                    SearchResultItem(
                        id=note.id,
                        title=note.title,
                        snippet=snippet,
                        tags=[t.name for t in note.tags],
                        score=round(score, 4),
                        match_type="fuzzy",
                    )
                )

        return SearchResponse(query=query, total=len(items), results=items)

    def autocomplete(self, query: str, limit: int = 10) -> AutocompleteResponse:
        """
        Autocomplete ranking:
        1. Title prefix match
        2. Tag prefix match
        3. Title substring match
        4. Fuzzy title/tag match
        Returns items with type ('note' or 'tag') and score.
        """
        q = query.strip().lower()
        if not q:
            return AutocompleteResponse(query=query, results=[])

        all_notes = self.note_repo.get_all_note_titles()  # (id, title)
        all_tags = self.tag_repo.get_all_tags_with_counts()  # (Tag, count)

        scored_results: List[AutocompleteItem] = []
        seen_keys = set()

        # 1. Title prefix
        for n_id, title in all_notes:
            t_lower = title.lower()
            if t_lower.startswith(q):
                score = 100.0 + (10.0 * len(q) / len(t_lower))
                key = ("note", n_id)
                if key not in seen_keys:
                    seen_keys.add(key)
                    scored_results.append(AutocompleteItem(type="note", id=n_id, title=title, score=score))

        # 2. Tag prefix
        for tag, count in all_tags:
            t_lower = tag.name.lower()
            if t_lower.startswith(q):
                score = 80.0 + (5.0 * len(q) / len(t_lower)) + min(5.0, count * 0.5)
                key = ("tag", tag.name)
                if key not in seen_keys:
                    seen_keys.add(key)
                    scored_results.append(AutocompleteItem(type="tag", id=None, title=f"#{tag.name}", score=score))

        # 3. Title substring
        for n_id, title in all_notes:
            t_lower = title.lower()
            if q in t_lower and not t_lower.startswith(q):
                score = 60.0 + (5.0 * len(q) / len(t_lower))
                key = ("note", n_id)
                if key not in seen_keys:
                    seen_keys.add(key)
                    scored_results.append(AutocompleteItem(type="note", id=n_id, title=title, score=score))

        # 4. Fuzzy fallback if fewer results
        if len(scored_results) < limit:
            note_candidates = [(("note", n_id, title), title) for n_id, title in all_notes if ("note", n_id) not in seen_keys]
            tag_candidates = [(("tag", None, f"#{t.name}"), t.name) for t, _ in all_tags if ("tag", t.name) not in seen_keys]

            fuzzy_note_matches = find_fuzzy_matches(q, note_candidates, threshold=0.55, limit=limit)
            for (typ, n_id, title), f_score in fuzzy_note_matches:
                scored_results.append(AutocompleteItem(type=typ, id=n_id, title=title, score=f_score * 40.0))

            fuzzy_tag_matches = find_fuzzy_matches(q, tag_candidates, threshold=0.55, limit=limit)
            for (typ, n_id, title), f_score in fuzzy_tag_matches:
                scored_results.append(AutocompleteItem(type=typ, id=n_id, title=title, score=f_score * 35.0))

        scored_results.sort(key=lambda x: x.score, reverse=True)
        return AutocompleteResponse(query=query, results=scored_results[:limit])

    def suggest_titles_for_wikilink(self, query: str = "", limit: int = 10) -> TitleSuggestResponse:
        """
        Suggest existing note titles for [[ autocomplete popup while typing in the editor.
        """
        q = query.strip().lower()
        all_notes = self.note_repo.get_all_note_titles()

        if not q:
            # Return most recent / default first 10
            items = [TitleSuggestItem(id=n_id, title=title) for n_id, title in all_notes[:limit]]
            return TitleSuggestResponse(query=query, results=items)

        matches = []
        for n_id, title in all_notes:
            t_lower = title.lower()
            if t_lower.startswith(q):
                matches.append((TitleSuggestItem(id=n_id, title=title), 100.0 - len(t_lower)))
            elif q in t_lower:
                matches.append((TitleSuggestItem(id=n_id, title=title), 50.0 - len(t_lower)))
            else:
                score = fuzzy_score(q, t_lower)
                if score > 0.5:
                    matches.append((TitleSuggestItem(id=n_id, title=title), score * 30.0))

        matches.sort(key=lambda x: x[1], reverse=True)
        return TitleSuggestResponse(query=query, results=[m[0] for m in matches[:limit]])
