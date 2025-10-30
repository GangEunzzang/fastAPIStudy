from tests.conftest import get_test_client, get_test_session


def todo_등록_요청_생성():
    return {"contents": "Test Todo", "is_done": False}


def todo_등록_요청(todo_data=None):
    if todo_data is None:
        todo_data = todo_등록_요청_생성()
    client = get_test_client()
    response = client.post("/todos", json=todo_data)
    return response.json()


def get_session():
    return get_test_session()

