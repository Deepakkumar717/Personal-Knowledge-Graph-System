import pytest

def test_tag_parsing_and_normalization(client):
    # Test POST /assist/tags normalization rules
    res = client.post("/assist/tags", json={
        "title": "Diet Plan",
        "content": "Tips on healthy eating.",
        "tags": ["  #Machine Learning! ", "fast food", "fast food", "very-long-tag-name-that-exceeds-thirty-characters-limit"]
    })
    assert res.status_code == 200
    data = res.json()
    normalized = data["normalized"]

    # "  #Machine Learning! " -> "machine-learning"
    assert "machine-learning" in normalized
    # "fast food" -> "fast-food" (space inside tag converted to hyphen)
    assert "fast-food" in normalized
    # deduplicated
    assert normalized.count("fast-food") == 1
    # max 30 chars
    long_tag = [t for t in normalized if "very-long" in t][0]
    assert len(long_tag) <= 30


def test_phrase_merge_suggestion_and_typos(client):
    # Step: "food, fast" -> suggests merge to "fast-food" (known phrase from phrases.txt)
    res = client.post("/assist/tags", json={
        "title": "Quick Snacks",
        "content": "Burgers and fries.",
        "tags": ["food", "fast", "fod"]
    })
    assert res.status_code == 200
    data = res.json()

    # Merge suggestion for adjacent tags food + fast -> fast-food
    merges = data["merges"]
    assert any(m["to"] == "fast-food" for m in merges)

    # Typo suggestion for 'fod' -> 'food'
    corrections = data["corrections"]
    assert any(c["from"] == "fod" and c["to"] == "food" for c in corrections)


def test_content_proofreading(client):
    # Create note "Python" so "Python" is in known titles
    client.post("/notes/", json={"title": "Python", "content": "Language"})

    # Proofread text
    sample_text = "IS used to reverse a string in python. It is the the best language."
    res = client.post("/assist/proofread", json={"text": sample_text})
    assert res.status_code == 200
    issues = res.json()

    # 1. Capitalize sentence start: "IS" -> "Is"
    is_issues = [i for i in issues if i["original"] == "IS"]
    assert len(is_issues) == 1
    assert is_issues[0]["suggestion"] == "Is"

    # 2. Repeated words: "the the" -> "the"
    dup_issues = [i for i in issues if "the the" in i["original"]]
    assert len(dup_issues) == 1
    assert dup_issues[0]["suggestion"] == "the"

    # 3. Known note title "Python" should NOT be flagged as typo
    py_typos = [i for i in issues if i["original"].lower() == "python"]
    assert len(py_typos) == 0

    # 4. Code and wikilinks should be exempted
    code_text = "Here is `some_code_snippet` and [[FastAPI]] and ```fenced block```"
    res_code = client.post("/assist/proofread", json={"text": code_text})
    assert res_code.status_code == 200
    assert len(res_code.json()) == 0


def test_palindrome_python_scenario(client):
    """
    Scenario:
    - Create "Python" (tags: python).
    - Create "Palindrome" (content: "Is used to reverse a string in python", tags: python, string).
    - Expect a suggestion to link Palindrome -> Python with reason: mentions 'python'.
    - Accept it; Palindrome -> Python created.
    - Python shows backlink from Palindrome.
    """
    client.delete("/system/reset")

    # 1. Create Python
    res_py = client.post("/notes/", json={
        "title": "Python",
        "tags": ["python"],
        "content": "A high level programming language."
    })
    assert res_py.status_code == 201
    py_id = res_py.json()["id"]

    # 2. Create Palindrome
    res_pal = client.post("/notes/", json={
        "title": "Palindrome",
        "tags": ["python", "string"],
        "content": "Is used to reverse a string in python."
    })
    assert res_pal.status_code == 201
    pal_id = res_pal.json()["id"]

    # 3. Get link suggestions for Palindrome
    res_sugg = client.get(f"/assist/link-suggestions?note_id={pal_id}")
    assert res_sugg.status_code == 200
    suggestions = res_sugg.json()
    assert len(suggestions) > 0

    py_sugg = [s for s in suggestions if s["note_id"] == py_id][0]
    assert "mentions 'Python'" in py_sugg["reasons"] or any("mentions" in r for r in py_sugg["reasons"])
    assert any("shared tags" in r for r in py_sugg["reasons"])

    # 4. Accept suggestion by calling standard PATCH /notes/{id}/link
    res_link = client.patch(f"/notes/{pal_id}/link", json={"target_id": py_id})
    assert res_link.status_code == 200

    # 5. Verify Python has backlink from Palindrome
    py_detail = client.get(f"/notes/{py_id}").json()
    assert any(b["id"] == pal_id for b in py_detail["backlinks"])

    # 6. Verify link suggestions no longer suggest Python (already linked)
    res_sugg_after = client.get(f"/assist/link-suggestions?note_id={pal_id}").json()
    assert not any(s["note_id"] == py_id for s in res_sugg_after)


def test_maggi_and_unrelated_notes_scenario(client):
    """
    Scenario:
    - Note "Maggi" with tags "food, fast" suggests merging to "fast-food".
    - "Maggi" must NOT be suggested a link to unrelated notes like "Python".
    """
    # Create Python if not exists
    py_res = client.post("/notes/", json={"title": "Python", "tags": ["python"], "content": "Language"})
    py_id = py_res.json().get("id")

    # Create Maggi
    maggi_res = client.post("/notes/", json={
        "title": "Maggi",
        "tags": ["food", "fast"],
        "content": "Instant noodles prepared in 2 minutes."
    })
    maggi_id = maggi_res.json()["id"]

    # Check tag assistance on Maggi tags
    tag_assist = client.post("/assist/tags", json={
        "title": "Maggi",
        "content": "Instant noodles prepared in 2 minutes.",
        "tags": ["food", "fast"]
    }).json()
    assert any(m["to"] == "fast-food" for m in tag_assist["merges"])

    # Check link suggestions for Maggi
    link_suggs = client.get(f"/assist/link-suggestions?note_id={maggi_id}").json()
    # Maggi should NOT suggest Python (completely unrelated: no text mention, no shared tags, no similarity)
    assert not any(s["title"] == "Python" for s in link_suggs)


def test_dismissed_suggestions_persist(client):
    """
    Test that dismissed suggestions never reappear.
    """
    client.delete("/system/reset")

    # Note A & Note B share tags and topic
    res_a = client.post("/notes/", json={"title": "Healthy Diet", "tags": ["health", "nutrition"], "content": "Eat vegetables."})
    res_b = client.post("/notes/", json={"title": "Nutrition Facts", "tags": ["health", "nutrition"], "content": "Nutrient values."})
    id_a = res_a.json()["id"]
    id_b = res_b.json()["id"]

    # Initially suggests B for A
    suggs = client.get(f"/assist/link-suggestions?note_id={id_a}").json()
    assert any(s["note_id"] == id_b for s in suggs)

    # Dismiss suggestion
    res_dis = client.post("/assist/link-suggestions/dismiss", json={"note_id": id_a, "other_id": id_b})
    assert res_dis.status_code == 200

    # Verify B no longer appears for A
    suggs_after = client.get(f"/assist/link-suggestions?note_id={id_a}").json()
    assert not any(s["note_id"] == id_b for s in suggs_after)


def test_non_programming_domains(client):
    """
    Test domain-agnostic tag and link suggestions for travel and food.
    """
    client.delete("/system/reset")

    res_italy = client.post("/notes/", json={
        "title": "Trip to Italy",
        "tags": ["travel", "europe"],
        "content": "Visited Rome and Florence during summer."
    })
    id_italy = res_italy.json()["id"]

    res_florence = client.post("/notes/", json={
        "title": "Florence Guide",
        "tags": ["travel", "italy"],
        "content": "Best museums and art in Florence."
    })
    id_florence = res_florence.json()["id"]

    # Trip to Italy mentions 'Florence' -> should suggest Florence Guide
    suggs = client.get(f"/assist/link-suggestions?note_id={id_italy}").json()
    assert any(s["note_id"] == id_florence for s in suggs)


def test_assist_status_and_fallback(client):
    """
    Test GET /assist/status reports rule-based by default.
    """
    res = client.get("/assist/status")
    assert res.status_code == 200
    data = res.json()
    assert data["enabled"] is False
    assert data["provider"] == "rule-based"
    assert data["model"] is None
