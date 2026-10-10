
import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.core.database import Base
from app.main import app
from app.api.dependencies import get_db

from fastapi.testclient import TestClient


TEST_DATABASE_URL = "sqlite:///./test_identity.db"


test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={
        "check_same_thread": False
    },
)


@pytest.fixture(scope="function")
def db():

    Base.metadata.drop_all(
        test_engine
    )

    Base.metadata.create_all(
        test_engine
    )

    with Session(test_engine) as session:

        yield session

    Base.metadata.drop_all(
        test_engine
    )


@pytest.fixture(scope="function")
def client(db):

    def override_get_db():

        yield db

    app.dependency_overrides[
        get_db
    ] = override_get_db

    with TestClient(app) as test_client:

        yield test_client

    app.dependency_overrides.clear()
