import pytest

def test_create_and_get_note(client):
    res = client.post("/notes/", json={
        "title": "Machine Learning",
        "content": "A branch of artificial intelligence.",
        "tags": ["AI", "Data Science"]
    })
    assert res.status_code == 201
    data = res.json()
    assert data["id"] is not None
    assert data["title"] == "Machine Learning"
    assert "ai" in data["tags"]
    assert "data-science" in data["tags"]

    note_id = data["id"]
    get_res = client.get(f"/notes/{note_id}")
    assert get_res.status_code == 200
    assert get_res.json()["title"] == "Machine Learning"

def test_duplicate_title_conflict(client):
    res1 = client.post("/notes/", json={"title": "Unique Title", "content": "First"})
    assert res1.status_code == 201

    # Exact duplicate
    res2 = client.post("/notes/", json={"title": "Unique Title", "content": "Second"})
    assert res2.status_code == 409
    assert res2.json()["error"] == "CONFLICT"

    # Case-insensitive duplicate
    res3 = client.post("/notes/", json={"title": "unique title", "content": "Third"})
    assert res3.status_code == 409
    assert res3.json()["error"] == "CONFLICT"

def test_validation_errors(client):
    # Empty title
    res_empty = client.post("/notes/", json={"title": "   ", "content": "Empty"})
    assert res_empty.status_code == 422
    assert res_empty.json()["error"] == "VALIDATION_ERROR"

    # Oversized title
    res_long = client.post("/notes/", json={"title": "A" * 201, "content": "Long"})
    assert res_long.status_code == 422

    # Oversized content
    res_huge = client.post("/notes/", json={"title": "Valid", "content": "C" * 50001})
    assert res_huge.status_code == 422

def test_update_and_patch_note(client):
    create_res = client.post("/notes/", json={"title": "Initial Title", "content": "Initial Content"})
    note_id = create_res.json()["id"]

    # PUT update
    put_res = client.put(f"/notes/{note_id}", json={
        "title": "Updated Title",
        "content": "Updated Content",
        "tags": ["updated-tag"]
    })
    assert put_res.status_code == 200
    assert put_res.json()["title"] == "Updated Title"
    assert put_res.json()["tags"] == ["updated-tag"]

    # PATCH update (e.g. pinned)
    patch_res = client.patch(f"/notes/{note_id}", json={"pinned": True})
    assert patch_res.status_code == 200
    assert patch_res.json()["pinned"] is True

def test_delete_note(client):
    create_res = client.post("/notes/", json={"title": "To Delete", "content": "Bye"})
    note_id = create_res.json()["id"]

    del_res = client.delete(f"/notes/{note_id}")
    assert del_res.status_code == 200
    assert del_res.json()["id"] == note_id

    # Verify 404
    get_res = client.get(f"/notes/{note_id}")
    assert get_res.status_code == 404
