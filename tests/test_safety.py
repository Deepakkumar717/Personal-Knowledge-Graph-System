import pytest
from pathlib import Path
from app.core.config import settings
from tests.conftest import assert_not_production_db

def test_guard_raises_on_production_db():
    """Verify the guard raises immediately if any test tries to connect to production DATABASE_PATH."""
    prod_url = f"sqlite:///{settings.DATABASE_PATH}"
    with pytest.raises(RuntimeError, match="CRITICAL TEST GUARD"):
        assert_not_production_db(prod_url)

def test_timestamp_utc_iso_serialization(client):
    """Verify timestamps serialize with explicit UTC offset (e.g. 2026-10-11T...Z)."""
    res = client.post("/notes/", json={
        "title": "Timestamp Test Note",
        "content": "Checking UTC offset",
        "tags": ["utc"]
    })
    assert res.status_code == 201
    data = res.json()
    created_at = data["created_at"]
    assert created_at is not None
    assert created_at.endswith("Z"), f"Expected UTC Z offset, got {created_at}"

    # Also verify list item serialization
    list_res = client.get("/notes/?q=Timestamp")
    assert list_res.status_code == 200
    item = list_res.json()[0]
    assert item["created_at"].endswith("Z")

def test_trash_snapshot_and_restore(client):
    """Verify deleting a note creates a snapshot in trash and restoring brings back tags and links."""
    # 1. Create target note
    r_target = client.post("/notes/", json={"title": "Beach Shack", "content": "Seafood", "tags": ["beach"]})
    target_id = r_target.json()["id"]

    # 2. Create note with link to target
    r_main = client.post("/notes/", json={
        "title": "Baga Travelogue",
        "content": "Visited [[Beach Shack]] on the coast.",
        "tags": ["travel", "goa"],
    })
    main_id = r_main.json()["id"]

    # Verify link
    main_detail = client.get(f"/notes/{main_id}").json()
    assert len(main_detail["outgoing_links"]) == 1

    # 3. Delete main note
    r_del = client.delete(f"/notes/{main_id}")
    assert r_del.status_code == 200

    # Verify note is gone from live notes
    assert client.get(f"/notes/{main_id}").status_code == 404

    # 4. Check trash
    r_trash = client.get("/trash/")
    assert r_trash.status_code == 200
    trash_items = r_trash.json()
    assert any(t["original_note_id"] == main_id for t in trash_items)
    item = next(t for t in trash_items if t["original_note_id"] == main_id)

    # 5. Restore from trash
    r_restore = client.post(f"/trash/{item['id']}/restore")
    assert r_restore.status_code == 200
    restored = r_restore.json()
    assert restored["title"] == "Baga Travelogue"
    assert "travel" in restored["tags"]
    assert any(l["target_id"] == target_id for l in restored["outgoing_links"])

    # 6. Restoring with taken title returns 409
    client.delete(f"/notes/{restored['id']}")
    client.post("/notes/", json={"title": "Baga Travelogue", "content": "conflict", "tags": []})
    trash_items_again = client.get("/trash/").json()
    item_again = next(t for t in trash_items_again if t["title"] == "Baga Travelogue")
    r_conflict = client.post(f"/trash/{item_again['id']}/restore")
    assert r_conflict.status_code == 409

def test_trash_purge_preserves_live_notes(client):
    """Verify trash emptying / purge permanently deletes only trash records, never live notes."""
    r_live = client.post("/notes/", json={"title": "Live Note Kept", "content": "safe", "tags": []})
    live_id = r_live.json()["id"]

    r_temp = client.post("/notes/", json={"title": "Temp Note Deleted", "content": "trash", "tags": []})
    temp_id = r_temp.json()["id"]
    client.delete(f"/notes/{temp_id}")

    # Empty trash
    client.delete("/trash/")
    assert len(client.get("/trash/").json()) == 0

    # Live note remains safe
    assert client.get(f"/notes/{live_id}").status_code == 200

def test_activity_log_captures_actions(client):
    """Verify activity_log records mutations."""
    client.post("/notes/", json={"title": "Activity Note", "content": "activity", "tags": []})
    res_act = client.get("/system/activity")
    assert res_act.status_code == 200
    logs = res_act.json()
    assert len(logs) > 0
    actions = [l["action"] for l in logs]
    assert "create" in actions
