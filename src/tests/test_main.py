from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_health_check_handler():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"ping": "pong"}


def test_get_todos():
    response = client.get("/todos")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json() == {
        "todos": [
            {"id": 1, "contents": "FastAPI Section 0", "is_done": True},
        ]
    }
