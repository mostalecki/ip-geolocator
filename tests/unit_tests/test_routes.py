import pytest
from fastapi import status

from src.geolocation.models import Geolocation
from tests.factories import GeolocationFactory


@pytest.mark.asyncio
async def test_create_geolocation(mocker, session, client, geolocation_data):
    mock_geolocation = Geolocation(**geolocation_data)
    mock_geolocation.created_at = None
    mock_geolocation.url = None
    mocker.patch("src.geolocation.service.GeolocationService.request_geolocation_data", return_value=mock_geolocation)

    result = client.post("/geolocation", json={"ipAddress": "151.101.65.140", "url": None})
    assert result.status_code == status.HTTP_201_CREATED


@pytest.mark.asyncio
async def test_get_geolocation_list(session, client):
    result = client.get("/geolocation")
    assert result.status_code == status.HTTP_200_OK
    assert len(result.json()) == 0

    geolocations = GeolocationFactory.create_batch(5)
    for geolocation in geolocations:
        session.add(geolocation)
    session.commit()

    result = client.get("/geolocation")
    assert result.status_code == status.HTTP_200_OK
    assert len(result.json()) == 5


@pytest.mark.asyncio
async def test_get_geolocation(session, client):
    geolocation = GeolocationFactory.create()
    session.add(geolocation)
    session.commit()
    session.refresh(geolocation)

    result = client.get(f"/geolocation/{geolocation.id}")
    assert result.status_code == status.HTTP_200_OK
    assert result.json()["id"] == geolocation.id


@pytest.mark.asyncio
async def test_get_geolocation_not_found(session, client):
    result = client.get("/geolocation/1337")
    assert result.status_code == status.HTTP_404_NOT_FOUND
    assert result.json()["error"] == "Not Found"


@pytest.mark.asyncio
async def test_delete_geolocation(session, client):
    geolocation = GeolocationFactory.create()
    session.add(geolocation)
    session.commit()
    session.refresh(geolocation)

    result = client.delete(f"/geolocation/{geolocation.id}")
    assert result.status_code == status.HTTP_204_NO_CONTENT
    assert result.text == ""


@pytest.mark.asyncio
async def test_delete_geolocation_not_found(session, client):
    result = client.delete("/geolocation/1337")
    assert result.status_code == status.HTTP_400_BAD_REQUEST
    assert result.json()["error"] == "Deletion failed: id 1337 not found"
