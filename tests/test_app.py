import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_unregister():
    activity = "Chess Club"
    email = "testuser@mergington.edu"

    # 确保先注销（避免已存在）
    client.post(f"/activities/{activity}/unregister?email={email}")

    # 注册
    signup_resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert signup_resp.status_code == 200
    assert "Signed up" in signup_resp.json()["message"]

    # 重复注册应报错
    signup_resp2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert signup_resp2.status_code == 400

    # 注销
    unregister_resp = client.post(f"/activities/{activity}/unregister?email={email}")
    assert unregister_resp.status_code == 200
    assert "Unregistered" in unregister_resp.json()["message"]

    # 重复注销应报错
    unregister_resp2 = client.post(f"/activities/{activity}/unregister?email={email}")
    assert unregister_resp2.status_code == 400


def test_signup_invalid_activity():
    resp = client.post("/activities/Nonexistent/signup?email=abc@mergington.edu")
    assert resp.status_code == 404


def test_unregister_invalid_activity():
    resp = client.post("/activities/Nonexistent/unregister?email=abc@mergington.edu")
    assert resp.status_code == 404
