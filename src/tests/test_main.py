from database import repository as todo_repository


def test_health_check_handler(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"ping": "pong"}


def test_get_todos_empty(client):
    response = client.get("/todos")
    assert response.status_code == 200
    assert response.json() == []


def test_create_todo_and_get_todos(client, test_db):
    todo_data = {"contents": "Test Todo", "is_done": False}
    response = client.post("/todos", json=todo_data)
    assert response.status_code == 200

    created_todo = response.json()
    assert created_todo["contents"] == todo_data["contents"]
    assert created_todo["is_done"] is False
    assert "id" in created_todo

    todo = todo_repository.find_by_id(session=test_db, todo_id=created_todo["id"])
    assert todo is not None
    assert todo.contents == todo_data["contents"]
    assert todo.is_done is False
