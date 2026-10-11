import pytest

def test_fts_and_fuzzy_search(client):
    client.post("/notes/", json={
        "title": "Python Programming Language",
        "content": "Python is a high-level interpreted programming language.",
        "tags": ["programming", "python"]
    })
    client.post("/notes/", json={
        "title": "Rust Systems Programming",
        "content": "Rust is a fast and memory-efficient systems language.",
        "tags": ["systems", "rust"]
    })

    # Exact FTS query
    res_fts = client.get("/search/?q=programming")
    assert res_fts.status_code == 200
    assert res_fts.json()["total"] >= 1
    titles = [r["title"] for r in res_fts.json()["results"]]
    assert "Python Programming Language" in titles

    # #tag syntax in query
    res_tag_q = client.get("/search/", params={"q": "#python"})
    assert res_tag_q.status_code == 200
    assert any("Python" in r["title"] for r in res_tag_q.json()["results"])

    # Fuzzy typo query: "pyhton" should find "Python Programming Language"
    res_fuzzy = client.get("/search/?q=pyhton")
    assert res_fuzzy.status_code == 200
    assert res_fuzzy.json()["total"] >= 1
    assert any("Python" in r["title"] for r in res_fuzzy.json()["results"])

def test_autocomplete(client):
    client.post("/notes/", json={"title": "Data Structures", "content": "Arrays and Trees", "tags": ["cs", "data"]})

    # Prefix match
    res_ac = client.get("/search/suggest?q=dat")
    assert res_ac.status_code == 200
    results = res_ac.json()["results"]
    assert len(results) > 0
    # Should contain note 'Data Structures' and tag '#data'
    types = [r["type"] for r in results]
    assert "note" in types

def test_wikilink_title_suggest(client):
    client.post("/notes/", json={"title": "Algorithms & Optimization", "content": ""})

    res = client.get("/titles/suggest?q=algo")
    assert res.status_code == 200
    titles = [r["title"] for r in res.json()["results"]]
    assert "Algorithms & Optimization" in titles

def test_unlinked_mentions(client):
    # Note 1: Target note
    res1 = client.post("/notes/", json={"title": "Quantum Physics", "content": "Study of atoms"})
    id1 = res1.json()["id"]

    # Note 2: mentions "Quantum Physics" without [[ ]]
    client.post("/notes/", json={"title": "Modern Science", "content": "Modern science includes Quantum Physics in its curriculum."})

    # Note 3: contains [[Quantum Physics]] (already linked -> should not be an unlinked mention)
    client.post("/notes/", json={"title": "Linked Note", "content": "See [[Quantum Physics]]."})

    res_mentions = client.get(f"/notes/{id1}/mentions")
    assert res_mentions.status_code == 200
    mentions = res_mentions.json()
    mention_titles = [m["note_title"] for m in mentions]
    assert "Modern Science" in mention_titles
    assert "Linked Note" not in mention_titles

def test_tfidf_related_notes(client):
    client.post("/notes/", json={"title": "Linear Algebra", "content": "Matrices, vectors, eigenvalues, and transformations.", "tags": ["math"]})
    client.post("/notes/", json={"title": "Matrix Calculus", "content": "Derivative of matrices and vectors in calculus.", "tags": ["math"]})
    client.post("/notes/", json={"title": "Cooking Recipes", "content": "Pasta with tomato sauce and basil.", "tags": ["food"]})

    res_notes = client.get("/notes/")
    notes = res_notes.json()
    la_id = [n["id"] for n in notes if n["title"] == "Linear Algebra"][0]

    res_rel = client.get(f"/notes/{la_id}/related")
    assert res_rel.status_code == 200
    related = res_rel.json()
    assert len(related) > 0
    assert related[0]["title"] == "Matrix Calculus"
