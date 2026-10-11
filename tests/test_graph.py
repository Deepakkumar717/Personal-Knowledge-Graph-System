import pytest

def test_graph_endpoints_and_traversal(client):
    # Setup graph: N1 -> N2 -> N3 -> N1 (Cycle!), plus N4 (Orphan)
    r1 = client.post("/notes/", json={"title": "N1", "content": "Links to [[N2]]", "tags": ["loop"]})
    r2 = client.post("/notes/", json={"title": "N2", "content": "Links to [[N3]]", "tags": ["loop"]})
    r3 = client.post("/notes/", json={"title": "N3", "content": "Links to [[N1]]", "tags": ["loop"]})
    r4 = client.post("/notes/", json={"title": "Orphan", "content": "Isolated note", "tags": ["isolated"]})

    id1, id2, id3, id4 = r1.json()["id"], r2.json()["id"], r3.json()["id"], r4.json()["id"]

    # 1. Full graph
    res_graph = client.get("/graph/")
    assert res_graph.status_code == 200
    g_data = res_graph.json()
    assert len(g_data["nodes"]) == 4
    assert len(g_data["edges"]) == 3

    # 2. Tag filter on graph
    res_tag_graph = client.get("/graph/?tag=loop")
    assert res_tag_graph.status_code == 200
    assert len(res_tag_graph.json()["nodes"]) == 3

    # 3. BFS neighborhood depth=1
    res_neigh_1 = client.get(f"/graph/neighbors/{id1}?depth=1")
    assert res_neigh_1.status_code == 200
    neigh_nodes = [n["id"] for n in res_neigh_1.json()["nodes"]]
    assert str(id1) in neigh_nodes
    assert str(id2) in neigh_nodes
    assert str(id4) not in neigh_nodes

    # 4. Shortest path N1 -> N3 (should be N1 -> N2 -> N3 of length 2)
    res_path = client.get(f"/graph/path?source={id1}&target={id3}")
    assert res_path.status_code == 200
    p_data = res_path.json()
    assert p_data["found"] is True
    assert p_data["length"] == 2
    assert p_data["path"] == [id1, id2, id3]

    # 5. Shortest path to Orphan (unreachable)
    res_unreach = client.get(f"/graph/path?source={id1}&target={id4}")
    assert res_unreach.status_code == 200
    assert res_unreach.json()["found"] is False

    # 6. Graph stats
    res_stats = client.get("/graph/stats")
    assert res_stats.status_code == 200
    stats = res_stats.json()
    assert stats["total_notes"] == 4
    assert stats["total_links"] == 3
    assert stats["orphan_count"] == 1
    assert "Orphan" in stats["orphans"]

def test_merged_two_way_edges_and_neighbourhood_classification(client):
    # Create notes A, B, C:
    # A <-> B (two-way mutual)
    # A -> C (one-way outgoing from A, backlink for C)
    r_a = client.post("/notes/", json={"title": "Note A", "content": "Links to [[Note B]] and [[Note C]]"})
    r_b = client.post("/notes/", json={"title": "Note B", "content": "Links to [[Note A]]"})
    r_c = client.post("/notes/", json={"title": "Note C", "content": "Leaf note"})

    a_id, b_id, c_id = str(r_a.json()["id"]), str(r_b.json()["id"]), str(r_c.json()["id"])

    # Verify GET /graph/ merges A <-> B into 1 edge with mutual=True and direction="mutual"
    res_graph = client.get("/graph/")
    assert res_graph.status_code == 200
    edges = res_graph.json()["edges"]

    # Total unique pairs should be 2: (A, B) and (A, C)
    assert len(edges) == 2

    # Check the mutual edge between A and B
    mutual_edges = [e for e in edges if e["mutual"] is True]
    assert len(mutual_edges) == 1
    ab_edge = mutual_edges[0]
    assert ab_edge["direction"] == "mutual"
    assert {ab_edge["source"], ab_edge["target"]} == {a_id, b_id}

    # Check the directed edge from A to C
    directed_edges = [e for e in edges if e["mutual"] is False]
    assert len(directed_edges) == 1
    ac_edge = directed_edges[0]
    assert ac_edge["direction"] == "directed"
    assert ac_edge["source"] == a_id
    assert ac_edge["target"] == c_id

    # Check GET /graph/neighbors/{a_id} returns classified focus neighbourhood
    res_neigh_a = client.get(f"/graph/neighbors/{a_id}?depth=1")
    assert res_neigh_a.status_code == 200
    data_a = res_neigh_a.json()
    assert b_id in data_a["mutual_ids"]
    assert c_id in data_a["outgoing_ids"]
    assert len(data_a["backlink_ids"]) == 0

    # Check GET /graph/neighbors/{c_id} shows A in backlink_ids
    res_neigh_c = client.get(f"/graph/neighbors/{c_id}?depth=1")
    assert res_neigh_c.status_code == 200
    data_c = res_neigh_c.json()
    assert a_id in data_c["backlink_ids"]
    assert len(data_c["outgoing_ids"]) == 0
    assert len(data_c["mutual_ids"]) == 0
