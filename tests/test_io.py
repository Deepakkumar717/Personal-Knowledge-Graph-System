import pytest

def test_export_and_import_roundtrip(client):
    # Create test note and manual link
    r1 = client.post("/notes/", json={"title": "Export Note 1", "content": "Content 1", "tags": ["backup"]})
    r2 = client.post("/notes/", json={"title": "Export Note 2", "content": "Content 2", "tags": ["backup"]})
    id1, id2 = r1.json()["id"], r2.json()["id"]

    client.patch(f"/notes/{id1}/link", json={"target_id": id2})

    # Export
    res_exp = client.get("/export")
    assert res_exp.status_code == 200
    export_payload = res_exp.json()
    assert len(export_payload["notes"]) >= 2
    assert len(export_payload["links"]) >= 1

    # Import the same data again -> duplicate notes should be safely skipped
    res_imp = client.post("/import", json=export_payload)
    assert res_imp.status_code == 200
    imp_summary = res_imp.json()
    assert imp_summary["status"] == "success"
    assert imp_summary["skipped_notes"] >= 2

def test_reset_database(client):
    # Create notes and tags
    client.post("/notes/", json={"title": "Note to Reset", "content": "Will be wiped", "tags": ["temp"]})
    res_notes = client.get("/notes/")
    assert len(res_notes.json()) >= 1

    # Calling DELETE /system/reset without confirmation must be rejected with 400
    res_bad = client.request("DELETE", "/system/reset", json={"confirm": "no"})
    assert res_bad.status_code == 400

    # Call DELETE /system/reset with required typed confirmation
    res_reset = client.request("DELETE", "/system/reset", json={"confirm": "DELETE ALL"})
    assert res_reset.status_code == 200
    assert res_reset.json()["status"] == "success"

    # Verify everything is empty
    assert len(client.get("/notes/").json()) == 0
    assert len(client.get("/tags/").json()) == 0
    g = client.get("/graph/").json()
    assert len(g["nodes"]) == 0
    assert len(g["edges"]) == 0
