"""Smoke tests for the stateless API."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_healthz():
    res = client.get("/healthz")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}


def test_readyz():
    res = client.get("/readyz")
    assert res.status_code == 200
    assert res.json() == {"status": "ready"}


def test_info_reports_hostname():
    res = client.get("/api/info")
    assert res.status_code == 200
    body = res.json()
    assert "message" in body
    assert body["hostname"]  # non-empty
