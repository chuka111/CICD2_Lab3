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
