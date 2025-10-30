class TestDB:
    _session = None

    @classmethod
    def set_session(cls, session):
        cls._session = session

    @classmethod
    def get_session(cls):
        return cls._session


class TodoFixtures:
    _client = None

    @classmethod
    def set_client(cls, client):
        cls._client = client

    @staticmethod
    def todo_등록_요청_생성():
        return {"contents": "Test Todo", "is_done": False}

    @classmethod
    def todo_등록_요청(cls, todo_data=None):
        if todo_data is None:
            todo_data = cls.todo_등록_요청_생성()
        response = cls._client.post("/todos", json=todo_data)
        return response.json()

