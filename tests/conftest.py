import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
import sqlite3
from sqlalchemy import create_engine, event, text
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.core.config import settings
from app.core.database import Base, get_db
import app.models  # noqa: F401
from main import app

# In-memory SQLite for testing
TEST_DATABASE_URL = "sqlite:///:memory:"

def assert_not_production_db(url: str):
    """Guards against any test opening or executing against the production database."""
    if ":memory:" in str(url):
        return
    clean = str(url).replace("sqlite:///", "").replace("sqlite://", "")
    if clean:
        resolved = Path(clean).resolve()
        prod_resolved = Path(settings.DATABASE_PATH).resolve()
        if resolved == prod_resolved:
            raise RuntimeError(
                f"CRITICAL TEST GUARD: Test engine resolved to production DATABASE_PATH: {prod_resolved}!"
            )

@pytest.fixture(scope="session")
def engine():
    assert_not_production_db(TEST_DATABASE_URL)
    test_engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
    )

    @event.listens_for(test_engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        if isinstance(dbapi_connection, sqlite3.Connection):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON;")
            cursor.close()

    return test_engine

@pytest.fixture(scope="function")
def db_session(engine):
    connection = engine.connect()
    transaction = connection.begin()
    
    # Create tables
    Base.metadata.create_all(bind=connection)

    # Create FTS5 virtual table in memory
    connection.execute(text("CREATE VIRTUAL TABLE IF NOT EXISTS notes_fts USING fts5(title, content, tags, tokenize='unicode61');"))
    # Create unique indexes
    connection.execute(text("CREATE UNIQUE INDEX IF NOT EXISTS ix_notes_title_lower ON notes (lower(title));"))

    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=connection)
    session = TestingSessionLocal()

    yield session

    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
