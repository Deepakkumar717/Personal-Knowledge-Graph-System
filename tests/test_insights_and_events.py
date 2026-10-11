import pytest
import asyncio
import json
from datetime import datetime, timezone
from app.services.event_service import event_service

def test_openapi_insights_specification(client):
    """Verify GET /graph/insights has operation_id 'get_insights' and tag 'graph'."""
    res = client.get("/openapi.json")
    assert res.status_code == 200
    data = res.json()
    assert "/graph/insights" in data["paths"]
    insights_op = data["paths"]["/graph/insights"]["get"]
    assert insights_op["operationId"] == "get_insights"
    assert "graph" in insights_op["tags"]

def test_insights_empty_database(client):
    """Verify GET /graph/insights on an empty database."""
    res = client.get("/graph/insights")
    assert res.status_code == 200
    data = res.json()
    
    assert data["notes_by_tag"] == []
    assert data["notes_by_group"] == []
    assert len(data["notes_per_day"]) == 30
    # Every day in the last 30 days should have count 0
    for item in data["notes_per_day"]:
        assert item["count"] == 0
        assert len(item["date"]) == 10  # YYYY-MM-DD
    assert data["top_connected"] == []
    assert data["connected_vs_orphans"] == {"connected": 0, "orphans": 0}
    assert data["link_types"] == {"auto": 0, "manual": 0, "mutual": 0}

def test_insights_populated_database(client):
    """Verify GET /graph/insights on a populated database with links, tags, and orphans."""
    # 1. Create Note 1 with wikilink to Note 2
    r1 = client.post("/notes/", json={
        "title": "Note Alpha",
        "content": "Refers to [[Note Beta]] for details.",
        "tags": ["FastAPI", "Python"]
    })
    assert r1.status_code == 201
    n1_id = r1.json()["id"]

    # 2. Create Note 2
    r2 = client.post("/notes/", json={
        "title": "Note Beta",
        "content": "Target of Note Alpha.",
        "tags": ["Python", "Backend"]
    })
    assert r2.status_code == 201
    n2_id = r2.json()["id"]

    # At this point, Alpha -> Beta is an auto link
    # 3. Create Note Gamma
    r3 = client.post("/notes/", json={
        "title": "Note Gamma",
        "content": "UI component.",
        "tags": ["Frontend"]
    })
    assert r3.status_code == 201
    n3_id = r3.json()["id"]

    # 4. Create Note Delta (orphan)
    r4 = client.post("/notes/", json={
        "title": "Note Delta",
        "content": "Isolated note.",
        "tags": ["DevOps"]
    })
    assert r4.status_code == 201
    n4_id = r4.json()["id"]

    # 5. Make Beta -> Alpha a manual link (making Alpha <-> Beta mutual)
    link_res1 = client.patch(f"/notes/{n2_id}/link", json={"target_id": n1_id})
    assert link_res1.status_code == 200

    # 6. Make Beta -> Gamma a manual one-way link
    link_res2 = client.patch(f"/notes/{n2_id}/link", json={"target_id": n3_id})
    assert link_res2.status_code == 200

    # 7. Create Note Epsilon with auto-link to Gamma (unidirectional auto link)
    r5 = client.post("/notes/", json={
        "title": "Note Epsilon",
        "content": "Links to [[Note Gamma]].",
        "tags": ["Python"]
    })
    assert r5.status_code == 201

    # Request Insights
    res = client.get("/graph/insights")
    assert res.status_code == 200
    data = res.json()

    # Verify notes_by_tag: python should have count 3 (Alpha, Beta, Epsilon)
    tag_counts = {item["tag"]: item["count"] for item in data["notes_by_tag"]}
    assert tag_counts["python"] == 3
    assert tag_counts["fastapi"] == 1
    assert tag_counts["backend"] == 1
    assert tag_counts["frontend"] == 1
    assert tag_counts["devops"] == 1
    assert len(data["notes_by_tag"]) <= 10

    # Verify notes_by_group is empty list
    assert data["notes_by_group"] == []

    # Verify notes_per_day: last day (today UTC) should have 5 created notes
    assert len(data["notes_per_day"]) == 30
    today_utc_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    assert data["notes_per_day"][-1]["date"] == today_utc_str
    assert data["notes_per_day"][-1]["count"] == 5

    # Verify top_connected:
    # Note Beta degree = (incoming from Alpha) + (outgoing to Alpha) + (outgoing to Gamma) = 3
    # Note Alpha degree = (outgoing to Beta) + (incoming from Beta) = 2
    # Note Gamma degree = (incoming from Beta) + (incoming from Epsilon) = 2
    # Note Epsilon degree = 1
    # Note Delta degree = 0
    top_connected = data["top_connected"]
    assert len(top_connected) == 5
    assert top_connected[0]["title"] == "Note Beta"
    assert top_connected[0]["degree"] == 3

    # Verify connected_vs_orphans:
    # Connected: Alpha, Beta, Gamma, Epsilon (4 notes)
    # Orphans: Delta (1 note)
    assert data["connected_vs_orphans"] == {"connected": 4, "orphans": 1}

    # Verify link_types:
    # Mutual: Alpha <-> Beta (1 mutual pair)
    # Manual: Beta -> Gamma (1 manual directed link)
    # Auto: Epsilon -> Gamma (1 auto directed link)
    assert data["link_types"] == {"auto": 1, "manual": 1, "mutual": 1}

@pytest.mark.asyncio
async def test_event_emission_and_heartbeat():
    """Verify that event_service emits all expected events and 15s heartbeat format."""
    queue = event_service.subscribe()
    try:
        # Test emitting note_created
        await event_service.broadcast("note_created", {"id": 10, "title": "New Note"})
        msg = await asyncio.wait_for(queue.get(), timeout=1.0)
        parsed = json.loads(msg)
        assert parsed["event"] == "note_created"
        assert parsed["data"]["id"] == 10

        # Test emitting note_updated
        await event_service.broadcast("note_updated", {"id": 10, "title": "Updated Title"})
        msg = await asyncio.wait_for(queue.get(), timeout=1.0)
        parsed = json.loads(msg)
        assert parsed["event"] == "note_updated"
        assert parsed["data"]["title"] == "Updated Title"

        # Test emitting note_deleted
        await event_service.broadcast("note_deleted", {"id": 10, "title": "Updated Title"})
        msg = await asyncio.wait_for(queue.get(), timeout=1.0)
        parsed = json.loads(msg)
        assert parsed["event"] == "note_deleted"

        # Test emitting link_created
        await event_service.broadcast("link_created", {"source_id": 10, "target_id": 20})
        msg = await asyncio.wait_for(queue.get(), timeout=1.0)
        parsed = json.loads(msg)
        assert parsed["event"] == "link_created"

        # Test emitting link_deleted
        await event_service.broadcast("link_deleted", {"source_id": 10, "target_id": 20})
        msg = await asyncio.wait_for(queue.get(), timeout=1.0)
        parsed = json.loads(msg)
        assert parsed["event"] == "link_deleted"

        # Test emitting group_changed
        await event_service.broadcast("group_changed", {"note_id": 10, "group": "Research"})
        msg = await asyncio.wait_for(queue.get(), timeout=1.0)
        parsed = json.loads(msg)
        assert parsed["event"] == "group_changed"

    finally:
        event_service.unsubscribe(queue)

@pytest.mark.asyncio
async def test_heartbeat_timeout_yield():
    """Verify that event_generator yields heartbeat after interval timeout."""
    gen = event_service.event_generator(interval=0.05)
    item = await gen.__anext__()
    assert "heartbeat" in item
    assert ": heartbeat" in item
    assert "data: " in item
    await gen.aclose()
