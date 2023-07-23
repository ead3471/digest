from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from app.models.users import Base

from ..database import get_db
from ..main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"


@pytest.fixture(scope="function")
def testing_session() -> Generator[Session, None, None]:
    print("in session fixture")
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
    TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=engine
    )

    # Recreate all table data
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    session = TestingSessionLocal()
    yield session

    session.close()


@pytest.fixture(scope="module")
def test_app():
    client = TestClient(app)
    yield client
    client.close()
