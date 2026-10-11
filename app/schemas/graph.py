from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

class GraphNode(BaseModel):
    id: str  # Note ID as string for Cytoscape compatibility
    label: str  # Note title
    tags: List[str] = []
    connection_count: int = 0
    pinned: bool = False

class GraphEdge(BaseModel):
    id: str  # e.g., "e_1_2"
    source: str
    target: str
    origin: str  # "auto" or "manual"
    mutual: bool = False
    direction: str = "directed"  # "directed" or "mutual"

class GraphResponse(BaseModel):
    nodes: List[GraphNode]
    edges: List[GraphEdge]
    adjacency_list: Dict[str, List[str]]
    outgoing_ids: List[str] = []
    backlink_ids: List[str] = []
    mutual_ids: List[str] = []

class HubStat(BaseModel):
    id: int
    title: str
    link_count: int

class TagDistributionStat(BaseModel):
    tag: str
    count: int

class GraphStats(BaseModel):
    total_notes: int
    total_links: int
    total_tags: int
    orphan_count: int
    orphans: List[str]
    hubs: List[HubStat]
    tag_distribution: List[TagDistributionStat]

class ShortestPathResponse(BaseModel):
    source_id: int
    target_id: int
    found: bool
    path: List[int] = []
    path_titles: List[str] = []
    length: int = 0

class NotesByTagItem(BaseModel):
    tag: str
    count: int

class NotesByGroupItem(BaseModel):
    group: str
    count: int

class NotesPerDayItem(BaseModel):
    date: str  # YYYY-MM-DD in UTC
    count: int

class TopConnectedItem(BaseModel):
    id: int
    title: str
    degree: int

class ConnectedVsOrphans(BaseModel):
    connected: int
    orphans: int

class LinkTypes(BaseModel):
    auto: int
    manual: int
    mutual: int

class GraphInsightsResponse(BaseModel):
    notes_by_tag: List[NotesByTagItem]
    notes_by_group: List[NotesByGroupItem]
    notes_per_day: List[NotesPerDayItem]
    top_connected: List[TopConnectedItem]
    connected_vs_orphans: ConnectedVsOrphans
    link_types: LinkTypes

