import pytest

from database import repository as todo_repository
from tests.fixtures import TodoFixtures, TestDB


def test_헬스체크(client):
    # when
    response = client.get("/")

    # then
    assert response.status_code == 200
    assert response.json() == {"ping": "pong"}

def test_빈목록조회(client):
    # when
    response = client.get("/todos")

    # then
    assert response.status_code == 200
    assert response.json() == []


def test_목록조회(client):
    # given
    TodoFixtures.todo_등록_요청()
    TodoFixtures.todo_등록_요청()

    # when
    response = client.get("/todos")

    # then
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_생성(client):
    # given & when
    created_todo = TodoFixtures.todo_등록_요청()

    # then
    todo = todo_repository.find_by_id(session=TestDB.get_session(), todo_id=created_todo["id"])

    assert todo is not None
    assert todo.contents == "Test Todo"
    assert todo.is_done is False


def test_삭제(client):
    # given
    created_todo = TodoFixtures.todo_등록_요청()
    todo_id = created_todo["id"]

    # when
    response = client.delete(f"/todos/{todo_id}")

    # then
    assert response.status_code == 204

    todo = todo_repository.find_by_id(session=TestDB.get_session(), todo_id=todo_id)
    assert todo is None


def test_업데이트(client):
    # given
    created_todo = TodoFixtures.todo_등록_요청()
    todo_id = created_todo["id"]

    # when
    response = client.patch(f"/todos/{todo_id}", json={"is_done": True})

    # then
    assert response.status_code == 200
    todo = todo_repository.find_by_id(session=TestDB.get_session(), todo_id=todo_id)
    assert todo.is_done is True