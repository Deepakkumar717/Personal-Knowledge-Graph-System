import pytest

def test_full_user_scenario(client):
    """
    Executes the exact 20-step manual user scenario through the API,
    verifying end-to-end functionality from a clean empty database.
    """
    # Pre-clean database
    client.request("DELETE", "/system/reset", json={"confirm": "DELETE ALL"})

    # Step 1: Create "Python" | tags: "Programming, Python" | content: "Python is a language used for [[Data Structures]] and [[FastAPI]]."
    res1 = client.post("/notes/", json={
        "title": "Python",
        "tags": ["Programming", "Python"],
        "content": "Python is a language used for [[Data Structures]] and [[FastAPI]]."
    })
    assert res1.status_code == 201
    py_data = res1.json()
    py_id = py_data["id"]
    assert "data structures" in py_data["unresolved_links"]
    assert "fastapi" in py_data["unresolved_links"]
    assert len(py_data["outgoing_links"]) == 0
    g1 = client.get("/graph/").json()
    assert len(g1["edges"]) == 0

    # Step 2: Create "Data Structures" | tags: "programming, #DSA" | content: "Arrays, stacks and queues. Used in [[Algorithms]]."
    res2 = client.post("/notes/", json={
        "title": "Data Structures",
        "tags": ["programming", "#DSA"],
        "content": "Arrays, stacks and queues. Used in [[Algorithms]]."
    })
    assert res2.status_code == 201
    ds_data = res2.json()
    ds_id = ds_data["id"]
    # Python -> Data Structures resolves automatically
    py_detail = client.get(f"/notes/{py_id}").json()
    assert any(l["target_id"] == ds_id for l in py_detail["outgoing_links"])
    assert "data structures" not in py_detail["unresolved_links"]
    # Data Structures shows backlink from Python
    assert any(b["id"] == py_id for b in ds_data["backlinks"])
    assert "algorithms" in ds_data["unresolved_links"]

    # Step 3: Create "Algorithms" | tags: "dsa" | content: "Sorting and searching. See [[Data Structures]]."
    res3 = client.post("/notes/", json={
        "title": "Algorithms",
        "tags": ["dsa"],
        "content": "Sorting and searching. See [[Data Structures]]."
    })
    assert res3.status_code == 201
    algo_id = res3.json()["id"]
    # Data Structures <-> Algorithms is one two-way (indigo) edge in the graph
    g3 = client.get("/graph/").json()
    ds_algo_edges = [
        e for e in g3["edges"]
        if {e["source"], e["target"]} == {str(ds_id), str(algo_id)}
    ]
    assert len(ds_algo_edges) == 1
    assert ds_algo_edges[0]["mutual"] is True
    assert ds_algo_edges[0]["direction"] == "mutual"

    # Step 4: Create "FastAPI" | tags: "python, web" | content: "A web framework built with [[Python]]."
    res4 = client.post("/notes/", json={
        "title": "FastAPI",
        "tags": ["python", "web"],
        "content": "A web framework built with [[Python]]."
    })
    assert res4.status_code == 201
    fa_id = res4.json()["id"]
    # Python <-> FastAPI two-way edge; Python's unresolved list is now empty
    g4 = client.get("/graph/").json()
    py_fa_edges = [
        e for e in g4["edges"]
        if {e["source"], e["target"]} == {str(py_id), str(fa_id)}
    ]
    assert len(py_fa_edges) == 1
    assert py_fa_edges[0]["mutual"] is True
    py_detail_4 = client.get(f"/notes/{py_id}").json()
    assert len(py_detail_4["unresolved_links"]) == 0

    # Step 5: Create "Cooking Pasta" and "Gardening" (Orphans)
    res_pasta = client.post("/notes/", json={
        "title": "Cooking Pasta",
        "tags": ["cooking"],
        "content": "Boil water, add salt."
    })
    res_garden = client.post("/notes/", json={
        "title": "Gardening",
        "tags": ["hobby"],
        "content": "Water plants in the morning."
    })
    pasta_id = res_pasta.json()["id"]
    garden_id = res_garden.json()["id"]

    # Verify both appear as orphans
    stats5 = client.get("/graph/stats").json()
    assert "Cooking Pasta" in stats5["orphans"]
    assert "Gardening" in stats5["orphans"]

    # Step 6: Focus "Python" in graph / neighborhood
    neigh_py = client.get(f"/graph/neighbors/{py_id}?depth=1").json()
    # Outgoing = Data Structures; Mutual = FastAPI
    assert str(ds_id) in neigh_py["outgoing_ids"]
    assert str(fa_id) in neigh_py["mutual_ids"]
    assert str(pasta_id) not in [n["id"] for n in neigh_py["nodes"]]
    # Detail panel for Python lists Outgoing (2: Data Structures, FastAPI) and Backlinks (1: FastAPI)
    py_detail_6 = client.get(f"/notes/{py_id}").json()
    assert len(py_detail_6["outgoing_links"]) == 2
    assert len(py_detail_6["backlinks"]) == 1

    # Step 7: Focus "Data Structures"
    neigh_ds = client.get(f"/graph/neighbors/{ds_id}?depth=1").json()
    assert str(algo_id) in neigh_ds["mutual_ids"]
    assert str(py_id) in neigh_ds["backlink_ids"]

    # Step 8: Manually link Algorithms -> FastAPI
    res_link = client.patch(f"/notes/{algo_id}/link", json={"target_id": fa_id})
    assert res_link.status_code == 200
    assert res_link.json()["origin"] == "manual"
    fa_backlinks = client.get(f"/notes/{fa_id}/backlinks").json()
    assert any(b["id"] == algo_id for b in fa_backlinks)

    # Step 9: Link Python -> Python (Self-link)
    res_self = client.patch(f"/notes/{py_id}/link", json={"target_id": py_id})
    assert res_self.status_code == 400
    assert res_self.json()["error"] == "BAD_REQUEST"

    # Step 10: Link Algorithms -> FastAPI again (Duplicate manual link)
    res_dup_link = client.patch(f"/notes/{algo_id}/link", json={"target_id": fa_id})
    assert res_dup_link.status_code == 409
    assert res_dup_link.json()["error"] == "CONFLICT"

    # Step 11: Create note titled "python" (case-insensitive duplicate)
    res_dup_title = client.post("/notes/", json={"title": "python", "content": "Lowercase dup"})
    assert res_dup_title.status_code == 409
    assert res_dup_title.json()["error"] == "CONFLICT"

    # Step 12: Tags normalization & suggestions
    res_tag_test = client.post("/notes/", json={
        "title": "Tag Normalization Test",
        "tags": ["  #Machine Learning! "],
        "content": "Testing tag cleaner"
    })
    assert res_tag_test.status_code == 201
    assert "machine-learning" in res_tag_test.json()["tags"]
    # Tag suggestion with "pro" should suggest "programming"
    res_tag_sugg = client.get("/tags/suggest?q=pro").json()
    sugg_names = [s["name"] for s in res_tag_sugg["suggestions"]]
    assert "programming" in sugg_names

    # Step 13: Search "pyhton" (typo) fuzzy fallback and tag searches
    res_fuzzy = client.get("/search/?q=pyhton").json()
    assert any(r["title"] == "Python" for r in res_fuzzy["results"])
    # Autocomplete with "py"
    res_ac = client.get("/search/suggest?q=py").json()
    assert any(r["title"] == "Python" for r in res_ac["results"])
    # Search "#dsa" returns Data Structures and Algorithms
    res_tag_search = client.get("/search/", params={"q": "#dsa"}).json()
    titles_dsa = [r["title"] for r in res_tag_search["results"]]
    assert "Data Structures" in titles_dsa
    assert "Algorithms" in titles_dsa
    # GET /notes/?tag=dsa returns the same two
    res_notes_dsa = client.get("/notes/?tag=dsa").json()
    dsa_note_titles = [n["title"] for n in res_notes_dsa]
    assert "Data Structures" in dsa_note_titles
    assert "Algorithms" in dsa_note_titles

    # Step 14: Create "Study Plan" without brackets -> unlinked mentions
    res_study = client.post("/notes/", json={
        "title": "Study Plan",
        "tags": ["productivity"],
        "content": "Learn Python and Algorithms this week."
    })
    assert res_study.status_code == 201
    study_id = res_study.json()["id"]

    # Python mentions should list Study Plan
    py_mentions = client.get(f"/notes/{py_id}/mentions").json()
    assert any(m["note_id"] == study_id for m in py_mentions)

    # Algorithms mentions should list Study Plan
    algo_mentions = client.get(f"/notes/{algo_id}/mentions").json()
    assert any(m["note_id"] == study_id for m in algo_mentions)

    # Convert mention by updating content to use wikilinks
    client.put(f"/notes/{study_id}", json={
        "title": "Study Plan",
        "tags": ["productivity"],
        "content": "Learn [[Python]] and [[Algorithms]] this week."
    })
    study_detail = client.get(f"/notes/{study_id}").json()
    assert any(l["target_id"] == py_id for l in study_detail["outgoing_links"])
    assert any(l["target_id"] == algo_id for l in study_detail["outgoing_links"])
    # GET /notes/?tag=productivity returns Study Plan
    prod_notes = client.get("/notes/?tag=productivity").json()
    assert any(n["title"] == "Study Plan" for n in prod_notes)

    # Step 15: Edit "Python" and remove [[FastAPI]] from the text
    client.put(f"/notes/{py_id}", json={
        "title": "Python",
        "tags": ["Programming", "Python"],
        "content": "Python is a language used for [[Data Structures]]."
    })
    py_after_edit = client.get(f"/notes/{py_id}").json()
    # Auto link Python -> FastAPI is gone
    assert not any(l["target_id"] == fa_id for l in py_after_edit["outgoing_links"])
    # But FastAPI -> Python remains!
    fa_after_edit = client.get(f"/notes/{fa_id}").json()
    assert any(l["target_id"] == py_id for l in fa_after_edit["outgoing_links"])
    # And manual link Algorithms -> FastAPI is untouched
    algo_after = client.get(f"/notes/{algo_id}").json()
    assert any(l["target_id"] == fa_id and l["origin"] == "manual" for l in algo_after["outgoing_links"])

    # Step 16: Rename "FastAPI" to "FastAPI Framework"
    client.put(f"/notes/{fa_id}", json={
        "title": "FastAPI Framework",
        "tags": ["python", "web"],
        "content": "A web framework built with [[Python]]."
    })
    fa_renamed = client.get(f"/notes/{fa_id}").json()
    assert fa_renamed["title"] == "FastAPI Framework"

    # Step 17: Delete "Data Structures"
    client.delete(f"/notes/{ds_id}")
    # References to it in Python should return to unresolved
    py_after_del = client.get(f"/notes/{py_id}").json()
    assert "data structures" in py_after_del["unresolved_links"]
    # Reference in Algorithms should return to unresolved
    algo_after_del = client.get(f"/notes/{algo_id}").json()
    assert "data structures" in algo_after_del["unresolved_links"]

    # Step 18: Edit Mode: Link Cooking Pasta -> Gardening, then delete edge
    res_pasta_link = client.patch(f"/notes/{pasta_id}/link", json={"target_id": garden_id})
    assert res_pasta_link.status_code == 200
    res_unlink = client.delete(f"/notes/{pasta_id}/link/{garden_id}")
    assert res_unlink.status_code == 200

    # Step 19: Check /graph/ and /graph/stats
    g_final = client.get("/graph/").json()
    stats_final = client.get("/graph/stats").json()
    assert len(g_final["nodes"]) == stats_final["total_notes"]
    assert stats_final["orphan_count"] >= 2

    # Step 20: Reset database
    res_reset = client.request("DELETE", "/system/reset", json={"confirm": "DELETE ALL"})
    assert res_reset.status_code == 200
    assert len(client.get("/notes/").json()) == 0
    assert len(client.get("/graph/").json()["nodes"]) == 0
