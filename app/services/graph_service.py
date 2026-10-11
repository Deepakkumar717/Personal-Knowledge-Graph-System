from collections import deque, defaultdict, Counter
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Set, Optional, Tuple
from sqlalchemy.orm import Session
from app.repositories.note_repo import NoteRepository
from app.repositories.link_repo import LinkRepository
from app.repositories.tag_repo import TagRepository
from app.schemas.graph import (
    GraphNode,
    GraphEdge,
    GraphResponse,
    GraphStats,
    ShortestPathResponse,
    HubStat,
    TagDistributionStat,
    GraphInsightsResponse,
    NotesByTagItem,
    NotesByGroupItem,
    NotesPerDayItem,
    TopConnectedItem,
    ConnectedVsOrphans,
    LinkTypes,
)
from app.core.exceptions import NotFoundException, ValidationException

class GraphService:
    def __init__(self, db: Session):
        self.db = db
        self.note_repo = NoteRepository(db)
        self.link_repo = LinkRepository(db)
        self.tag_repo = TagRepository(db)

    def _build_merged_edges(
        self, all_links: List[any], valid_node_ids: Set[int]
    ) -> Tuple[List[GraphEdge], Dict[str, List[str]]]:
        """
        Merge two-way links (A->B and B->A) into a single edge with mutual=True and direction="mutual".
        Returns (edges_list, adjacency_list).
        """
        adjacency_list: Dict[str, List[str]] = {str(nid): [] for nid in valid_node_ids}
        link_pairs: Dict[Tuple[int, int], str] = {}  # (source, target) -> origin

        for link in all_links:
            if link.source_id in valid_node_ids and link.target_id in valid_node_ids:
                link_pairs[(link.source_id, link.target_id)] = link.origin
                adjacency_list[str(link.source_id)].append(str(link.target_id))

        edges: List[GraphEdge] = []
        processed_pairs: Set[Tuple[int, int]] = set()

        for (u, v), origin_uv in link_pairs.items():
            pair_key = (min(u, v), max(u, v))
            if pair_key in processed_pairs:
                continue
            processed_pairs.add(pair_key)

            has_reverse = (v, u) in link_pairs
            if has_reverse:
                # Two-way mutual edge
                origin_vu = link_pairs[(v, u)]
                merged_origin = "manual" if (origin_uv == "manual" or origin_vu == "manual") else "auto"
                edges.append(
                    GraphEdge(
                        id=f"e_{pair_key[0]}_{pair_key[1]}_mutual",
                        source=str(pair_key[0]),
                        target=str(pair_key[1]),
                        origin=merged_origin,
                        mutual=True,
                        direction="mutual",
                    )
                )
            else:
                # One-way directed edge
                edges.append(
                    GraphEdge(
                        id=f"e_{u}_{v}",
                        source=str(u),
                        target=str(v),
                        origin=origin_uv,
                        mutual=False,
                        direction="directed",
                    )
                )

        return edges, adjacency_list

    def get_full_graph(self, tag_filter: Optional[str] = None) -> GraphResponse:
        """
        Build full graph structure with nodes, merged edges, and adjacency list.
        Optionally filters nodes (and incident edges) by tag.
        """
        all_notes = self.note_repo.get_all_notes_full()
        all_links = self.link_repo.get_all_links()

        # If tag filter is provided
        filtered_note_ids: Optional[Set[int]] = None
        if tag_filter:
            tf_lower = tag_filter.strip().lower()
            filtered_note_ids = {
                n.id for n in all_notes
                if any(t.name.lower() == tf_lower for t in n.tags)
            }

        # Calculate degrees / connection counts
        connection_counts: Dict[int, int] = defaultdict(int)
        for link in all_links:
            connection_counts[link.source_id] += 1
            connection_counts[link.target_id] += 1

        nodes: List[GraphNode] = []
        valid_node_ids: Set[int] = set()

        for n in all_notes:
            if filtered_note_ids is not None and n.id not in filtered_note_ids:
                continue

            valid_node_ids.add(n.id)
            nodes.append(
                GraphNode(
                    id=str(n.id),
                    label=n.title,
                    tags=[t.name for t in n.tags],
                    connection_count=connection_counts[n.id],
                    pinned=bool(n.pinned),
                )
            )

        edges, adjacency_list = self._build_merged_edges(all_links, valid_node_ids)

        return GraphResponse(
            nodes=nodes,
            edges=edges,
            adjacency_list=adjacency_list,
            outgoing_ids=[],
            backlink_ids=[],
            mutual_ids=[],
        )

    def get_neighborhood(self, note_id: int, depth: int = 1) -> GraphResponse:
        """
        BFS traversal to discover subgraph around note_id up to specified depth (1..4).
        Computes focus neighborhood lists: outgoing_ids, backlink_ids, mutual_ids.
        """
        if depth < 1 or depth > 4:
            raise ValidationException("depth must be between 1 and 4.")

        center_note = self.note_repo.get_by_id(note_id)
        if not center_note:
            raise NotFoundException(f"Note with id {note_id} not found.")

        all_notes = self.note_repo.get_all_notes_full()
        all_links = self.link_repo.get_all_links()
        note_map = {n.id: n for n in all_notes}

        # Build undirected graph adjacency for BFS traversal
        neighbors_map: Dict[int, Set[int]] = defaultdict(set)
        direct_out: Set[Tuple[int, int]] = set()

        for link in all_links:
            neighbors_map[link.source_id].add(link.target_id)
            neighbors_map[link.target_id].add(link.source_id)
            direct_out.add((link.source_id, link.target_id))

        # BFS
        visited: Set[int] = {note_id}
        queue: deque = deque([(note_id, 0)])

        while queue:
            curr_id, curr_depth = queue.popleft()
            if curr_depth < depth:
                for neighbor in neighbors_map[curr_id]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append((neighbor, curr_depth + 1))

        # Connection counts
        connection_counts: Dict[int, int] = defaultdict(int)
        for link in all_links:
            connection_counts[link.source_id] += 1
            connection_counts[link.target_id] += 1

        nodes = []
        for nid in visited:
            note = note_map.get(nid)
            if note:
                nodes.append(
                    GraphNode(
                        id=str(note.id),
                        label=note.title,
                        tags=[t.name for t in note.tags],
                        connection_count=connection_counts[note.id],
                        pinned=bool(note.pinned),
                    )
                )

        edges, adj = self._build_merged_edges(all_links, visited)

        # Classify immediate 1-hop neighbours of note_id
        outgoing_ids: List[str] = []
        backlink_ids: List[str] = []
        mutual_ids: List[str] = []

        for other_id in visited:
            if other_id == note_id:
                continue
            has_out = (note_id, other_id) in direct_out
            has_in = (other_id, note_id) in direct_out

            if has_out and has_in:
                mutual_ids.append(str(other_id))
            elif has_out:
                outgoing_ids.append(str(other_id))
            elif has_in:
                backlink_ids.append(str(other_id))

        return GraphResponse(
            nodes=nodes,
            edges=edges,
            adjacency_list=adj,
            outgoing_ids=outgoing_ids,
            backlink_ids=backlink_ids,
            mutual_ids=mutual_ids,
        )

    def find_shortest_path(self, source_id: int, target_id: int) -> ShortestPathResponse:
        """
        Cycle-safe BFS to find the shortest directed path from source to target.
        """
        if source_id == target_id:
            source_note = self.note_repo.get_by_id(source_id)
            if not source_note:
                raise NotFoundException(f"Source note with id {source_id} not found.")
            return ShortestPathResponse(
                source_id=source_id,
                target_id=target_id,
                found=True,
                path=[source_id],
                path_titles=[source_note.title],
                length=0,
            )

        source_note = self.note_repo.get_by_id(source_id)
        if not source_note:
            raise NotFoundException(f"Source note with id {source_id} not found.")

        target_note = self.note_repo.get_by_id(target_id)
        if not target_note:
            raise NotFoundException(f"Target note with id {target_id} not found.")

        all_links = self.link_repo.get_all_links()
        out_adj: Dict[int, List[int]] = defaultdict(list)
        for link in all_links:
            out_adj[link.source_id].append(link.target_id)

        # BFS for shortest path
        queue = deque([[source_id]])
        visited = {source_id}

        found_path: Optional[List[int]] = None

        while queue:
            curr_path = queue.popleft()
            node = curr_path[-1]

            if node == target_id:
                found_path = curr_path
                break

            for next_node in out_adj[node]:
                if next_node not in visited:
                    visited.add(next_node)
                    queue.append(curr_path + [next_node])

        if not found_path:
            return ShortestPathResponse(
                source_id=source_id,
                target_id=target_id,
                found=False,
                path=[],
                path_titles=[],
                length=0,
            )

        all_notes = self.note_repo.get_all_notes_full()
        note_title_map = {n.id: n.title for n in all_notes}
        path_titles = [note_title_map.get(nid, f"Note {nid}") for nid in found_path]

        return ShortestPathResponse(
            source_id=source_id,
            target_id=target_id,
            found=True,
            path=found_path,
            path_titles=path_titles,
            length=len(found_path) - 1,
        )

    def get_stats(self) -> GraphStats:
        """Compute network statistics: counts, orphans, hubs, tag distribution."""
        all_notes = self.note_repo.get_all_notes_full()
        all_links = self.link_repo.get_all_links()
        all_tags = self.tag_repo.get_all_tags_with_counts()

        total_notes = len(all_notes)
        total_links = len(all_links)
        total_tags = len(all_tags)

        # Compute degree per note
        degrees: Dict[int, int] = defaultdict(int)
        for link in all_links:
            degrees[link.source_id] += 1
            degrees[link.target_id] += 1

        orphans = []
        for n in all_notes:
            if degrees[n.id] == 0:
                orphans.append(n.title)

        # Hubs sorted by degree desc
        hubs_list = sorted(
            [HubStat(id=n.id, title=n.title, link_count=degrees[n.id]) for n in all_notes],
            key=lambda h: h.link_count,
            reverse=True,
        )[:5]

        # Tag distribution
        tag_dist = [
            TagDistributionStat(tag=tag.name, count=cnt)
            for tag, cnt in all_tags
        ]

        return GraphStats(
            total_notes=total_notes,
            total_links=total_links,
            total_tags=total_tags,
            orphan_count=len(orphans),
            orphans=orphans,
            hubs=hubs_list,
            tag_distribution=tag_dist,
        )

    def get_insights(self) -> GraphInsightsResponse:
        """
        Compute comprehensive knowledge graph insights and analytics.
        Returns top tags, notes per day (last 30 days in UTC), top connected notes,
        connected vs orphans, and link type breakdown.
        """
        all_notes = self.note_repo.get_all_notes_full()
        all_links = self.link_repo.get_all_links()
        all_tags = self.tag_repo.get_all_tags_with_counts()

        # 1. notes_by_tag (top 10 tags by note count)
        sorted_tags = sorted(all_tags, key=lambda tc: (-tc[1], tc[0].name.lower()))[:10]
        notes_by_tag = [
            NotesByTagItem(tag=tag.name, count=cnt)
            for tag, cnt in sorted_tags
        ]

        # 2. notes_by_group (empty list as groups are not in the core 4-table schema)
        notes_by_group: List[NotesByGroupItem] = []

        # 3. notes_per_day (last 30 days in UTC)
        now_utc = datetime.now(timezone.utc)
        today_utc = now_utc.date()
        days_30 = [today_utc - timedelta(days=i) for i in range(29, -1, -1)]

        date_counts = Counter()
        for n in all_notes:
            if n.created_at:
                d = n.created_at.date()
                date_counts[d] += 1

        notes_per_day = [
            NotesPerDayItem(date=d.strftime("%Y-%m-%d"), count=date_counts[d])
            for d in days_30
        ]

        # 4. Compute degrees for top_connected and connected_vs_orphans
        degrees: Dict[int, int] = defaultdict(int)
        for link in all_links:
            degrees[link.source_id] += 1
            degrees[link.target_id] += 1

        # top 5 connected notes
        sorted_notes = sorted(all_notes, key=lambda n: (-degrees[n.id], n.title.lower()))[:5]
        top_connected = [
            TopConnectedItem(id=n.id, title=n.title, degree=degrees[n.id])
            for n in sorted_notes
        ]

        # 5. connected_vs_orphans
        connected_count = sum(1 for n in all_notes if degrees[n.id] > 0)
        orphans_count = sum(1 for n in all_notes if degrees[n.id] == 0)
        connected_vs_orphans = ConnectedVsOrphans(
            connected=connected_count,
            orphans=orphans_count,
        )

        # 6. link_types {auto, manual, mutual}
        link_pairs = {(l.source_id, l.target_id): l.origin for l in all_links}
        mutual_pairs: Set[Tuple[int, int]] = set()
        for (u, v) in link_pairs:
            if (v, u) in link_pairs:
                mutual_pairs.add((min(u, v), max(u, v)))
        mutual_count = len(mutual_pairs)

        auto_count = 0
        manual_count = 0
        for (u, v), orig in link_pairs.items():
            if (v, u) in link_pairs:
                continue
            if orig == "auto":
                auto_count += 1
            else:
                manual_count += 1

        link_types = LinkTypes(
            auto=auto_count,
            manual=manual_count,
            mutual=mutual_count,
        )

        return GraphInsightsResponse(
            notes_by_tag=notes_by_tag,
            notes_by_group=notes_by_group,
            notes_per_day=notes_per_day,
            top_connected=top_connected,
            connected_vs_orphans=connected_vs_orphans,
            link_types=link_types,
        )

