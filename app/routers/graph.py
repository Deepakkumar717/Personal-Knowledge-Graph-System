from typing import Optional
from fastapi import APIRouter, Depends, Query, Path
from app.schemas.graph import GraphResponse, GraphStats, ShortestPathResponse, GraphInsightsResponse
from app.services.graph_service import GraphService
from app.core.dependencies import get_graph_service

router = APIRouter(prefix="/graph", tags=["graph"])

@router.get(
    "/insights",
    response_model=GraphInsightsResponse,
    summary="Get knowledge graph insights and analytics",
    operation_id="get_insights",
)
def get_insights(
    graph_service: GraphService = Depends(get_graph_service),
):
    """Retrieve comprehensive graph analytics: top tags, groups, activity over 30 days, hubs, orphans, and link types."""
    return graph_service.get_insights()

@router.get(
    "/",
    response_model=GraphResponse,
    summary="Get full graph",
    operation_id="get_graph",
)
def get_graph(
    tag: Optional[str] = Query(None, description="Optional tag filter for graph nodes"),
    graph_service: GraphService = Depends(get_graph_service),
):
    """Retrieve graph nodes, directed edges, and adjacency list for visualization."""
    return graph_service.get_full_graph(tag_filter=tag)

@router.get(
    "/neighbors/{note_id}",
    response_model=GraphResponse,
    summary="Get BFS neighborhood of a note",
    operation_id="get_graph_neighbors",
)
def get_graph_neighbors(
    note_id: int = Path(..., ge=1, description="Center note ID"),
    depth: int = Query(1, ge=1, le=4, description="BFS exploration depth (1-4)"),
    graph_service: GraphService = Depends(get_graph_service),
):
    """Retrieve neighborhood subgraph around a note using BFS up to depth."""
    return graph_service.get_neighborhood(note_id=note_id, depth=depth)

@router.get(
    "/path",
    response_model=ShortestPathResponse,
    summary="Find shortest path between two notes",
    operation_id="get_shortest_path",
)
def get_shortest_path(
    source: int = Query(..., ge=1, description="Source note ID"),
    target: int = Query(..., ge=1, description="Target note ID"),
    graph_service: GraphService = Depends(get_graph_service),
):
    """Find the shortest directed path between two notes using BFS."""
    return graph_service.find_shortest_path(source_id=source, target_id=target)

@router.get(
    "/stats",
    response_model=GraphStats,
    summary="Get knowledge graph statistics",
    operation_id="get_graph_stats",
)
def get_graph_stats(
    graph_service: GraphService = Depends(get_graph_service),
):
    """Get network statistics: total notes, links, tags, orphans, hub nodes, tag distribution."""
    return graph_service.get_stats()
