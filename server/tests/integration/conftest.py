"""Shared setup of the integration tests: the real API, from the routes down to SQLite,
working on an empty database file created for each test instead of server/queue.db."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine

from server.database import Base, SessionLocal, engine
from server.main import app


@pytest.fixture
def db(tmp_path):
    """Session on a new empty database, used by the test to add and check rows."""
    test_engine = create_engine(
        f"sqlite:///{tmp_path / 'test.db'}", connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(bind=test_engine)
    # the repositories open their sessions from SessionLocal, so they all use the test database now
    SessionLocal.configure(bind=test_engine)
    session = SessionLocal()
    yield session
    session.close()
    SessionLocal.configure(bind=engine)
    test_engine.dispose()


@pytest.fixture
def client(db):
    """Calls the API like the frontend does, on the same test database."""
    return TestClient(app)
