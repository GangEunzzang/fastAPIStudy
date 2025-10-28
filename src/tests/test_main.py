from database import repository as todo_repository

from tests import fixtures as todo_fixtures


def test_헬스체크_호출시_정상응답_반환(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"ping": "pong"}


def test_빈목록_조회시_빈리스트_반환(client):
    response = client.get("/todos")

    assert response.status_code == 200
    assert response.json() == []


def test_todo생성_후_db조회가능(client, test_db):
    created_todo = todo_fixtures.todo_등록_요청(client)

    assert created_todo["contents"] == "Test Todo"
    assert created_todo["is_done"] is False
    assert "id" in created_todo

    todo = todo_repository.find_by_id(session=test_db, todo_id=created_todo["id"])

    assert todo is not None
    assert todo.contents == "Test Todo"
    assert todo.is_done is False
