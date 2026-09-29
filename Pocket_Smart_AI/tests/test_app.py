from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_home_page():
    r = client.get("/")
    assert r.status_code == 200
    assert "PocketSmart" in r.text

def test_home_planner_fallback():
    payload = {
        "budget": 100000,
        "rooms": ["Living Room"],
        "style": "modern",
        "location": "India",
        "items": [{"category": "sofa", "quantity": 1, "notes": ""}]
    }
    r = client.post("/generate-home", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["planner"] == "home"
    assert data["estimated_total"] <= data["budget"]
    assert len(data["recommendations"]) > 0

def test_party_planner_fallback():
    payload = {
        "budget": 50000,
        "guests": 30,
        "event_type": "Birthday",
        "venue": "Home",
        "city": "Chennai",
        "preferences": "vegetarian"
    }
    r = client.post("/generate-party", json=payload)
    assert r.status_code == 200
    assert r.json()["planner"] == "party"

def test_register_and_login():
    email = "test-pocketsmart@example.com"
    # Registration may already exist if tests are run repeatedly.
    r = client.post("/register", json={"name":"Test User","email":email,"password":"password123"})
    assert r.status_code in (200, 409)
    r = client.post("/login", json={"email":email,"password":"password123"})
    assert r.status_code == 200
    assert r.cookies.get("access_token")
