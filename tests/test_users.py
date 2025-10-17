# tests/test_users.py
import pytest


def user_payload(uid=1, name="Paul", email="pl@atu.ie", age=25, sid="S1234567"):
    return {"user_id": uid, "name": name, "email": email, "age": age, "student_id": sid}

def test_create_user_ok(client):

    r = client.post("/api/users", json=user_payload())
    assert r.status_code == 201
    data = r.json()
    assert data["user_id"] == 1
    assert data["name"] == "Paul"

def test_duplicate_user_id_conflict(client):
    client.post("/api/users", json=user_payload(uid=2))
    r = client.post("/api/users", json=user_payload(uid=2))
    assert r.status_code == 409 # duplicate id -> conflict
    assert "exists" in r.json()["detail"].lower()

@pytest.mark.parametrize("bad_sid", ["BAD123", "s1234567", "S123", "S12345678"])
def test_bad_student_id_422(client, bad_sid):
    r = client.post("/api/users", json=user_payload(uid=3, sid=bad_sid))
    assert r.status_code == 422 # pydantic validation error

def test_get_user_404(client):
    r = client.get("/api/users/999")
    assert r.status_code == 404


def test_delete_then_404(client):
    client.post("/api/users", json=user_payload(uid=3))
    r1 = client.delete("/api/users/3")
    assert r1.status_code == 204

def test_update_user_ok(client):
     client.post("/api/users", json=user_payload(uid=5, name="Sean", email="sean@atu.ie"))
     updated = user_payload(uid=10, name="Sean", email="sean@atu.ie", age=20)
     r = client.put("/api/users/5", json=updated)
     assert r.status_code == 200
     data = r.json()
     assert data["name"] == "Sean"
     assert data["email"] == "sean@atu.ie"
     assert data["age"] == 20


def test_update_user_404(client):
 updated = user_payload(uid=15, name="john", email="john@atu.ie")
 r = client.put("/api/users/15", json=updated)

 assert r.status_code == 404