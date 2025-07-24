import pytest
from fastapi.testclient import TestClient
from app.api import app

TOKEN = "secret-token"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

client = TestClient(app)

def test_pow():
    resp = client.post("/pow", json={"base": 2, "exponent": 8}, headers=HEADERS)
    assert resp.status_code == 200
    assert resp.json()["result"] == 256

def test_fibonacci():
    resp = client.post("/fibonacci", json={"n": 10}, headers=HEADERS)
    assert resp.status_code == 200
    assert resp.json()["result"] == 55

def test_factorial():
    resp = client.post("/factorial", json={"n": 5}, headers=HEADERS)
    assert resp.status_code == 200
    assert resp.json()["result"] == 120

def test_gcd():
    resp = client.post("/gcd", json={"a": 54, "b": 24}, headers=HEADERS)
    assert resp.status_code == 200
    assert resp.json()["result"] == 6

def test_is_prime():
    resp = client.post("/is_prime", json={"n": 17}, headers=HEADERS)
    assert resp.status_code == 200
    assert resp.json()["result"] is True
    resp2 = client.post("/is_prime", json={"n": 18}, headers=HEADERS)
    assert resp2.status_code == 200
    assert resp2.json()["result"] is False

def test_history_auth():
    resp = client.get("/history", headers=HEADERS)
    assert resp.status_code == 200

def test_auth_required():
    resp = client.post("/pow", json={"base": 2, "exponent": 2})
    assert resp.status_code == 403 or resp.status_code == 401 