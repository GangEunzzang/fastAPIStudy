import pytest
from pytest_bdd import scenarios, given, when, then, parsers

from database import repository as todo_repository
from tests.fixtures import TodoFixtures, TestDB

# Feature 파일 연결
scenarios('features/todo.feature')


# Shared context for storing test data
@pytest.fixture
def context():
    return {}


# Given steps
@given('2개의 Todo가 존재한다')
def create_two_todos(context):
    context['todo1'] = TodoFixtures.todo_등록_요청()
    context['todo2'] = TodoFixtures.todo_등록_요청()


@given('Todo가 생성되어 있다')
def create_todo(context):
    context['created_todo'] = TodoFixtures.todo_등록_요청()
    context['todo_id'] = context['created_todo']['id']


# When steps
@when('Todo를 생성한다')
def when_create_todo(context):
    context['created_todo'] = TodoFixtures.todo_등록_요청()


@when('Todo 목록을 조회한다')
def when_get_todos(client, context):
    context['response'] = client.get("/todos")


@when('Todo를 삭제한다')
def when_delete_todo(client, context):
    context['response'] = client.delete(f"/todos/{context['todo_id']}")


@when('Todo의 완료 상태를 true로 변경한다')
def when_update_todo(client, context):
    context['response'] = client.patch(
        f"/todos/{context['todo_id']}",
        json={"is_done": True}
    )


# Then steps
@then('Todo가 정상적으로 생성된다')
def then_todo_created(context):
    assert context['created_todo']['contents'] == "Test Todo"
    assert context['created_todo']['is_done'] is False
    assert 'id' in context['created_todo']


@then('생성된 Todo를 DB에서 조회할 수 있다')
def then_todo_exists_in_db(context):
    todo_id = context['created_todo']['id']
    todo = todo_repository.find_by_id(session=TestDB.get_session(), todo_id=todo_id)
    assert todo is not None
    assert todo.contents == "Test Todo"
    assert todo.is_done is False


@then('빈 리스트가 반환된다')
def then_empty_list(context):
    assert context['response'].status_code == 200
    assert context['response'].json() == []


@then('2개의 Todo가 반환된다')
def then_two_todos_returned(context):
    assert context['response'].status_code == 200
    assert len(context['response'].json()) == 2


@then('Todo가 삭제된다')
def then_todo_deleted(context):
    assert context['response'].status_code == 204


@then('삭제된 Todo를 DB에서 조회할 수 없다')
def then_todo_not_in_db(context):
    todo = todo_repository.find_by_id(
        session=TestDB.get_session(),
        todo_id=context['todo_id']
    )
    assert todo is None


@then('Todo가 정상적으로 업데이트된다')
def then_todo_updated(context):
    assert context['response'].status_code == 200
    updated_todo = context['response'].json()
    assert updated_todo['is_done'] is True


@then('DB에서 조회한 Todo의 완료 상태가 true이다')
def then_todo_done_in_db(context):
    todo = todo_repository.find_by_id(
        session=TestDB.get_session(),
        todo_id=context['todo_id']
    )
    assert todo is not None
    assert todo.is_done is True
