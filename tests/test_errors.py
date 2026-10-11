import pytest
from app.core.exceptions import AppException

def test_error_response_format(client):
    # 404 Not Found
    res_404 = client.get("/notes/99999")
    assert res_404.status_code == 404
    data_404 = res_404.json()
    assert "error" in data_404
    assert "message" in data_404
    assert "details" in data_404
    assert data_404["error"] == "NOT_FOUND"

    # 422 Validation Error format
    res_422 = client.post("/notes/", json={"title": ""})
    assert res_422.status_code == 422
    data_422 = res_422.json()
    assert data_422["error"] == "VALIDATION_ERROR"
    assert "details" in data_422

def test_health_endpoint(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"
