import pytest

def test_tag_normalization(client):
    res = client.post("/notes/", json={
        "title": "Tag Test Note",
        "content": "Testing tag cleaner",
        "tags": ["  #Web-Dev  ", "data_science!", "AI", "ai", "web--dev"]
    })
    assert res.status_code == 201
    tags = res.json()["tags"]
    # Should normalize and deduplicate: 'web-dev', 'datascience', 'ai'
    assert "web-dev" in tags
    assert "data-science" in tags
    assert "ai" in tags
    assert len(tags) == 3

def test_tag_limit_exceeded(client):
    too_many_tags = [f"tag-{i}" for i in range(16)]
    res = client.post("/notes/", json={
        "title": "Too Many Tags",
        "content": "Content",
        "tags": too_many_tags
    })
    assert res.status_code == 422
    assert "15 tags" in res.json()["message"]

def test_tag_listing_and_suggestions(client):
    client.post("/notes/", json={"title": "N1", "content": "Algorithms in python", "tags": ["python", "algorithms"]})
    client.post("/notes/", json={"title": "N2", "content": "Algorithms in java", "tags": ["java", "algorithms"]})

    # List tags
    res_list = client.get("/tags/")
    assert res_list.status_code == 200
    tags_list = res_list.json()
    assert any(t["name"] == "algorithms" and t["count"] == 2 for t in tags_list)

    # Suggest tags with prefix 'py'
    res_sugg = client.get("/tags/suggest?q=py")
    assert res_sugg.status_code == 200
    names = [s["name"] for s in res_sugg.json()["suggestions"]]
    assert "python" in names

    # Suggest with co-occurrence: given 'java', 'algorithms' should be boosted
    res_co = client.get("/tags/suggest?selected=java")
    assert res_co.status_code == 200
    co_names = [s["name"] for s in res_co.json()["suggestions"]]
    assert "algorithms" in co_names
