from database.orm import Todo

def test_health_check_handler(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"ping": "pong"}


def test_get_todos(client, mocker):
    mocker.patch("main.get_todos", return_value=[
        Todo(id=1, contents="FastAPI Section 0", is_done=True),
        Todo(id=2, contents="FastAPI Section 1", is_done=False),
    ])

    response = client.get("/todos")

    assert response.status_code == 200
    assert isinstance(response.json(), list)

    assert response.json() == [
        {"id": 1, "contents": "FastAPI Section 0", "is_done": True},
        {"id": 2, "contents": "FastAPI Section 1", "is_done": False},
    ]