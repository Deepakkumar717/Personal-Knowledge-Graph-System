import pytest

def test_wikilink_parsing_and_auto_linking(client):
    # Create target note B
    res_b = client.post("/notes/", json={"title": "Note B", "content": "I am Note B"})
    assert res_b.status_code == 201
    b_id = res_b.json()["id"]

    # Create Note A with wikilink to B, alias to B, code blocks to ignore, self link to ignore
    content_a = """
    Check out [[Note B]] and [[Note B|alias to B]].
    Also self link [[Note A]].
    Do not link inside `[[Note C]]` or fenced code:
    ```
    [[Note D]]
    ```
    And unresolved [[Future Topic]].
    """
    res_a = client.post("/notes/", json={"title": "Note A", "content": content_a})
    assert res_a.status_code == 201
    a_id = res_a.json()["id"]
    data_a = res_a.json()

    # Outgoing links from A should contain only Note B
    outgoing = data_a["outgoing_links"]
    assert len(outgoing) == 1
    assert outgoing[0]["target_id"] == b_id
    assert outgoing[0]["origin"] == "auto"

    # Pending links should contain 'future topic'
    assert "future topic" in data_a["unresolved_links"]
    assert "note c" not in data_a["unresolved_links"]
    assert "note d" not in data_a["unresolved_links"]

    # Backlinks of Note B should show Note A
    res_b_details = client.get(f"/notes/{b_id}")
    backlinks = res_b_details.json()["backlinks"]
    assert len(backlinks) == 1
    assert backlinks[0]["id"] == a_id

def test_pending_link_resolution_on_create(client):
    # Create Note X with unresolved link to 'Future Note'
    res_x = client.post("/notes/", json={"title": "Note X", "content": "References [[Future Note]]"})
    x_id = res_x.json()["id"]
    assert "future note" in res_x.json()["unresolved_links"]

    # Now create 'Future Note'
    res_f = client.post("/notes/", json={"title": "Future Note", "content": "Here I am!"})
    f_id = res_f.json()["id"]

    # Note X should now have outgoing link to Future Note, and unresolved_links cleared
    res_x_updated = client.get(f"/notes/{x_id}")
    outgoing = res_x_updated.json()["outgoing_links"]
    assert any(l["target_id"] == f_id for l in outgoing)
    assert "future note" not in res_x_updated.json()["unresolved_links"]

def test_rename_rewrites_wikilinks_in_other_notes(client):
    # Note Target and Note Source
    res_t = client.post("/notes/", json={"title": "Old Target", "content": "Target content"})
    t_id = res_t.json()["id"]

    res_s = client.post("/notes/", json={"title": "Source Note", "content": "Links to [[Old Target]] and [[Old Target|My Alias]]"})
    s_id = res_s.json()["id"]

    # Rename Target to New Target
    res_rename = client.put(f"/notes/{t_id}", json={"title": "New Target", "content": "Target content"})
    assert res_rename.status_code == 200

    # Verify Source Note content was rewritten
    res_s_detail = client.get(f"/notes/{s_id}")
    content = res_s_detail.json()["content"]
    assert "[[New Target]]" in content
    assert "[[New Target|My Alias]]" in content
    assert "[[Old Target]]" not in content

def test_manual_linking_rules(client):
    res1 = client.post("/notes/", json={"title": "Alpha", "content": "Alpha content"})
    res2 = client.post("/notes/", json={"title": "Beta", "content": "Beta content"})
    id1, id2 = res1.json()["id"], res2.json()["id"]

    # Self link -> 400
    res_self = client.patch(f"/notes/{id1}/link", json={"target_id": id1})
    assert res_self.status_code == 400
    assert res_self.json()["error"] == "BAD_REQUEST"

    # Missing target -> 404
    res_missing = client.patch(f"/notes/{id1}/link", json={"target_id": 99999})
    assert res_missing.status_code == 404

    # Valid manual link
    res_link = client.patch(f"/notes/{id1}/link", json={"target_id": id2})
    assert res_link.status_code == 200
    assert res_link.json()["origin"] == "manual"

    # Duplicate manual link -> 409
    res_dup = client.patch(f"/notes/{id1}/link", json={"target_id": id2})
    assert res_dup.status_code == 409

def test_delete_note_moves_to_pending(client):
    res_a = client.post("/notes/", json={"title": "Host", "content": "Points to [[Guest]]"})
    res_b = client.post("/notes/", json={"title": "Guest", "content": "Guest here"})
    a_id, b_id = res_a.json()["id"], res_b.json()["id"]

    # Delete Guest
    del_res = client.delete(f"/notes/{b_id}")
    assert del_res.status_code == 200

    # Host should now have 'guest' in unresolved_links
    res_a_detail = client.get(f"/notes/{a_id}")
    assert "guest" in res_a_detail.json()["unresolved_links"]
    assert len(res_a_detail.json()["outgoing_links"]) == 0
