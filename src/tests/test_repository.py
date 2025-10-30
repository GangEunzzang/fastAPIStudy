from database import repository as todo_repository
from database.orm import Todo
from schema.request import CreateTodoRequest


def test_save(session):
    # given
    todo = Todo.create(CreateTodoRequest(contents="Test Todo", is_done=False))

    # when
    saved_todo = todo_repository.save(session=session, todo=todo)

    # then
    assert saved_todo.id is not None
    assert saved_todo.contents == "Test Todo"
    assert saved_todo.is_done is False


def test_find_all_empty(session):
    # when
    todos = todo_repository.find_all(session=session)

    # then
    assert len(todos) == 0


def test_find_all(session):
    # given
    todo1 = Todo.create(CreateTodoRequest(contents="Todo 1", is_done=False))
    todo2 = Todo.create(CreateTodoRequest(contents="Todo 2", is_done=True))
    todo_repository.save(session=session, todo=todo1)
    todo_repository.save(session=session, todo=todo2)

    # when
    todos = todo_repository.find_all(session=session)

    # then
    assert len(todos) == 2
    assert todos[0].contents == "Todo 1"
    assert todos[1].contents == "Todo 2"


def test_find_by_id(session):
    # given
    todo = Todo.create(CreateTodoRequest(contents="Test Todo", is_done=False))
    saved_todo = todo_repository.save(session=session, todo=todo)

    # when
    found_todo = todo_repository.find_by_id(session=session, todo_id=saved_todo.id)

    # then
    assert found_todo is not None
    assert found_todo.id == saved_todo.id
    assert found_todo.contents == "Test Todo"


def test_find_by_id_not_found(session):
    # when
    found_todo = todo_repository.find_by_id(session=session, todo_id=9999)

    # then
    assert found_todo is None


def test_update(session):
    # given
    todo = Todo.create(CreateTodoRequest(contents="Test Todo", is_done=False))
    saved_todo = todo_repository.save(session=session, todo=todo)

    # when
    saved_todo.done()
    updated_todo = todo_repository.update(session=session, todo=saved_todo)

    # then
    assert updated_todo.is_done is True
    found_todo = todo_repository.find_by_id(session=session, todo_id=saved_todo.id)
    assert found_todo.is_done is True


def test_delete(session):
    # given
    todo = Todo.create(CreateTodoRequest(contents="Test Todo", is_done=False))
    saved_todo = todo_repository.save(session=session, todo=todo)
    todo_id = saved_todo.id

    # when
    result = todo_repository.delete(session=session, todo_id=todo_id)

    # then
    assert result is True
    found_todo = todo_repository.find_by_id(session=session, todo_id=todo_id)
    assert found_todo is None


def test_delete_not_found(session):
    # when
    result = todo_repository.delete(session=session, todo_id=9999)

    # then
    assert result is False
