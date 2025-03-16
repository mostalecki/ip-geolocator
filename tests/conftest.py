import json

import pytest
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from fastapi.testclient import TestClient

from src.geolocation.models import IpGeolocationRequest
from src.utils.database import get_session
from src.main import app
from tests.utils import get_test_file_data


@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    (monkeypatch.setattr("src.config.config.BASE_IPSTACK_URL", "http://test.url"),)
    (monkeypatch.setattr("src.config.config.IPSTACK_ACCESS_KEY", "test_key"),)


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture()
def geolocation_data():
    with get_test_file_data("test_data/geolocation.json") as fh:
        yield json.loads(fh.read())


@pytest.fixture()
def ipstack_response_success():
    with get_test_file_data("test_data/ipstack_response_success.json") as fh:
        yield json.loads(fh.read())


@pytest.fixture()
def ip_geolocation_request():
    return IpGeolocationRequest(ip_address="151.101.65.140", url="http://facebook.com/")
