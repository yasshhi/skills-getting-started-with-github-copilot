from urllib.parse import quote

from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_and_unregister():
    activity = "Chess Club"
    email = "pytest-test@example.com"

    # Ensure test email is not present before starting
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # Signup
    signup_resp = client.post(f"/activities/{quote(activity)}/signup?email={email}")
    assert signup_resp.status_code == 200
    assert "Signed up" in signup_resp.json().get("message", "")

    # Verify participant added
    resp = client.get("/activities")
    assert email in resp.json()[activity]["participants"]

    # Unregister
    del_resp = client.delete(f"/activities/{quote(activity)}/participants?email={email}")
    assert del_resp.status_code == 200
    assert "Unregistered" in del_resp.json().get("message", "")

    # Verify participant removed
    resp2 = client.get("/activities")
    assert email not in resp2.json()[activity]["participants"]
