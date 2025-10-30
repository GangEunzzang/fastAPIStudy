import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from database.connection import get_db
from database.orm import Base
from main import app

TEST_DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
)

# 전역 변수로 관리
_test_client = None
_test_session = None


def get_test_client():
    return _test_client


def get_test_session():
    return _test_session


@pytest.fixture(scope="function", autouse=True)
def setup(request):
    global _test_client, _test_session

    # DB 설정
    Base.metadata.create_all(bind=test_engine)
    session = TestSessionLocal()
    _test_session = session

    # Client 설정
    def override_get_db():
        yield session

    app.dependency_overrides[get_db] = override_get_db
    _test_client = TestClient(app)

    yield

    # 정리
    session.close()
    Base.metadata.drop_all(bind=test_engine)
    app.dependency_overrides.clear()
    _test_client = None
    _test_session = None


@pytest.fixture
def client():
    return get_test_client()

@pytest.fixture
def session():
    return get_test_session()
