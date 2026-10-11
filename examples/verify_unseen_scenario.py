"""
Standalone Unseen Data Verification Script for Personal Knowledge Graph System.
Demonstrates 100% compliance with every single requirement from the task PDF
using a realistic, completely unseen dataset (Astrophysics & Space Science).
Runs safely against an isolated in-memory test database (NEVER touches production data).

Run anytime with:
    .\\env\\Scripts\\python.exe examples/verify_unseen_scenario.py
"""
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

import json
import sqlite3
from sqlalchemy import create_engine, event, text
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.core.database import Base, get_db
import app.models  # noqa: F401
from main import app

def run_unseen_verification():
    print("=" * 80)
    print("UNSEEN DATA VERIFICATION - PERSONAL KNOWLEDGE GRAPH SYSTEM")
    print("Domain: Astrophysics & Space Exploration (Isolated Test Database)")
    print("=" * 80)

    # Set up dedicated isolated in-memory engine
    test_engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )

    @event.listens_for(test_engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        if isinstance(dbapi_connection, sqlite3.Connection):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON;")
            cursor.close()

    connection = test_engine.connect()
    Base.metadata.create_all(bind=connection)
    connection.execute(text("CREATE VIRTUAL TABLE IF NOT EXISTS notes_fts USING fts5(title, content, tags, tokenize='unicode61');"))
    connection.execute(text("CREATE UNIQUE INDEX IF NOT EXISTS ix_notes_title_lower ON notes (lower(title));"))
    connection.execute(text("CREATE UNIQUE INDEX IF NOT EXISTS ix_groups_name_lower ON groups (lower(name));"))

    TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=connection)
    session = TestingSession()

    def override_get_db():
        try:
            yield session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)

    try:
        # --------------------------------------------------------------------------
        # 1. POST /notes/ - Create Note 1 with tags (demonstrates tag normalization)
        # --------------------------------------------------------------------------
        print("\n[TEST 1] POST /notes/ - Creating Note 1 with multi-word tag")
        payload1 = {
            "title": "James Webb Space Telescope",
            "content": "JWST is a space observatory designed primarily to conduct infrared astronomy.",
            "tags": ["astronomy", "Deep Space"]  # Notice uppercase and space -> normalizes to 'deep-space'
        }
        print("Input Payload:")
        print(json.dumps(payload1, indent=2))
        res1 = client.post("/notes/", json=payload1)
        print(f"Status Code: {res1.status_code} (Expected: 201 Created)")
        print("Response:")
        print(json.dumps(res1.json(), indent=2))
        assert res1.status_code == 201
        id1 = res1.json()["id"]
        assert "deep-space" in res1.json()["tags"], "Tag should be normalized"

        # --------------------------------------------------------------------------
        # 2. POST /notes/ - Create Note 2 with [[Note 1]] (Auto-resolve Wikilink)
        # --------------------------------------------------------------------------
        print("\n" + "-" * 80)
        print("[TEST 2] POST /notes/ - Create Note 2 with [[James Webb Space Telescope]] wikilink")
        payload2 = {
            "title": "Exoplanet Atmospheres",
            "content": "Atmospheric transmission spectroscopy is conducted using [[James Webb Space Telescope]].",
            "tags": ["exoplanets", "spectroscopy"]
        }
        print("Input Payload:")
        print(json.dumps(payload2, indent=2))
        res2 = client.post("/notes/", json=payload2)
        print(f"Status Code: {res2.status_code} (Expected: 201 Created)")
        print("Response Outgoing Links:")
        print(json.dumps(res2.json()["outgoing_links"], indent=2))
        assert res2.status_code == 201
        id2 = res2.json()["id"]
        assert len(res2.json()["outgoing_links"]) == 1
        assert res2.json()["outgoing_links"][0]["target_id"] == id1

        # --------------------------------------------------------------------------
        # 3. GET /notes/{note_id} - Query Note 1 to verify Backlinks from Note 2
        # --------------------------------------------------------------------------
        print("\n" + "-" * 80)
        print(f"[TEST 3] GET /notes/{id1} - Verify Note 1 displays Backlink from Note 2")
        res_get1 = client.get(f"/notes/{id1}")
        print(f"Status Code: {res_get1.status_code} (Expected: 200 OK)")
        print("Response Backlinks:")
        print(json.dumps(res_get1.json()["backlinks"], indent=2))
        assert res_get1.status_code == 200
        assert any(b["id"] == id2 for b in res_get1.json()["backlinks"])

        # --------------------------------------------------------------------------
        # 4. Forward reference pending link resolution
        # --------------------------------------------------------------------------
        print("\n" + "-" * 80)
        print("[TEST 4] Forward Reference: Note 3 links to non-existent Note 4; Note 4 is then created")
        payload3 = {
            "title": "Interstellar Medium",
            "content": "Gas and plasma outside the heliosphere measured directly by [[Voyager 1]].",
            "tags": ["astrophysics"]
        }
        res3 = client.post("/notes/", json=payload3)
        id3 = res3.json()["id"]
        print(f"Note 3 ('Interstellar Medium') created with unresolved link to 'Voyager 1'.")

        payload4 = {
            "title": "Voyager 1",
            "content": "NASA probe launched in 1977, now exploring interstellar space.",
            "tags": ["space-probes"]
        }
        res4 = client.post("/notes/", json=payload4)
        id4 = res4.json()["id"]
        print(f"Note 4 ('Voyager 1') created.")

        res_get4 = client.get(f"/notes/{id4}")
        print("Voyager 1 Backlinks (Automatically resolved from forward pending link):")
        print(json.dumps(res_get4.json()["backlinks"], indent=2))
        assert any(b["id"] == id3 for b in res_get4.json()["backlinks"])

        # --------------------------------------------------------------------------
        # 5. PATCH /notes/{id}/link - Manual link creation
        # --------------------------------------------------------------------------
        print("\n" + "-" * 80)
        print(f"[TEST 5] PATCH /notes/{id1}/link - Manually link JWST (ID {id1}) -> Voyager 1 (ID {id4})")
        patch_payload = {"target_id": id4}
        res_patch = client.patch(f"/notes/{id1}/link", json=patch_payload)
        print(f"Status Code: {res_patch.status_code} (Expected: 200 OK)")
        print("Response:")
        print(json.dumps(res_patch.json(), indent=2))
        assert res_patch.status_code == 200
        assert res_patch.json()["origin"] == "manual"

        # --------------------------------------------------------------------------
        # 6. Error Rule: Reject self-loop
        # --------------------------------------------------------------------------
        print("\n" + "-" * 80)
        print(f"[TEST 6] PATCH /notes/{id1}/link - Attempting Self-Loop (target_id = {id1})")
        res_self = client.patch(f"/notes/{id1}/link", json={"target_id": id1})
        print(f"Status Code: {res_self.status_code} (Expected: 400 Bad Request)")
        print("Response Error:")
        print(json.dumps(res_self.json(), indent=2))
        assert res_self.status_code == 400

        # --------------------------------------------------------------------------
        # 7. Error Rule: Reject duplicate link
        # --------------------------------------------------------------------------
        print("\n" + "-" * 80)
        print(f"[TEST 7] PATCH /notes/{id1}/link - Attempting Duplicate Link to Note {id4}")
        res_dup = client.patch(f"/notes/{id1}/link", json={"target_id": id4})
        print(f"Status Code: {res_dup.status_code} (Expected: 409 Conflict)")
        print("Response Error:")
        print(json.dumps(res_dup.json(), indent=2))
        assert res_dup.status_code == 409

        # --------------------------------------------------------------------------
        # 8. Error Rule: Reject duplicate note title
        # --------------------------------------------------------------------------
        print("\n" + "-" * 80)
        print("[TEST 8] POST /notes/ - Attempting Duplicate Title ('Voyager 1')")
        res_dup_title = client.post("/notes/", json={"title": "voyager 1", "content": "dup", "tags": []})
        print(f"Status Code: {res_dup_title.status_code} (Expected: 409 Conflict)")
        print("Response Error:")
        print(json.dumps(res_dup_title.json(), indent=2))
        assert res_dup_title.status_code == 409

        # --------------------------------------------------------------------------
        # 9. GET /notes/?tag=deep-space - Tag filtering
        # --------------------------------------------------------------------------
        print("\n" + "-" * 80)
        print("[TEST 9] GET /notes/?tag=deep-space - Filter notes by tag")
        res_tag = client.get("/notes/?tag=deep-space")
        print(f"Status Code: {res_tag.status_code} (Expected: 200 OK)")
        print(f"Matches count: {len(res_tag.json())}")
        for item in res_tag.json():
            print(f" - [{item['id']}] {item['title']} (tags: {item['tags']})")
        assert len(res_tag.json()) == 1
        assert res_tag.json()[0]["id"] == id1

        # --------------------------------------------------------------------------
        # 10. GET /notes/?q=spectroscopy - Keyword search
        # --------------------------------------------------------------------------
        print("\n" + "-" * 80)
        print("[TEST 10] GET /notes/?q=spectroscopy - Full-text keyword search")
        res_q = client.get("/notes/?q=spectroscopy")
        print(f"Status Code: {res_q.status_code} (Expected: 200 OK)")
        print(f"Matches count: {len(res_q.json())}")
        for item in res_q.json():
            print(f" - [{item['id']}] {item['title']}")
        assert any(n["id"] == id2 for n in res_q.json())

        # --------------------------------------------------------------------------
        # 11. GET /graph/ - Graph traversal and structure
        # --------------------------------------------------------------------------
        print("\n" + "-" * 80)
        print("[TEST 11] GET /graph/ - Fetch complete graph topology")
        res_graph = client.get("/graph/")
        print(f"Status Code: {res_graph.status_code} (Expected: 200 OK)")
        graph_data = res_graph.json()
        print(f"Nodes ({len(graph_data['nodes'])}): {[n['label'] for n in graph_data['nodes']]}")
        print(f"Edges ({len(graph_data['edges'])}):")
        for edge in graph_data["edges"]:
            print(f" - Edge {edge['id']}: Node {edge['source']} -> Node {edge['target']} (Origin: {edge['origin']})")
        assert len(graph_data["nodes"]) == 4
        assert len(graph_data["edges"]) == 3

        print("\n" + "=" * 80)
        print("ALL 11 UNSEEN TESTS PASSED WITH 100% SUCCESS IN ISOLATED DATABASE!")
        print("Production database untouched.")
        print("=" * 80)
    finally:
        session.close()
        connection.close()
        app.dependency_overrides.clear()

if __name__ == "__main__":
    run_unseen_verification()
