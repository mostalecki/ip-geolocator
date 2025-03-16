from datetime import datetime

import pytest
from freezegun import freeze_time
from sqlmodel import select

from src.error_handler.exceptions import NotFoundError, DeletionError
from src.geolocation.manager import GeolocationManager
from src.geolocation.models import Geolocation
from tests.factories import GeolocationFactory


@pytest.mark.asyncio
@freeze_time("2025-03-16 20:00:00")
async def test_manager_create_geolocation(mocker, session, geolocation_data, ip_geolocation_request):
    mock_geolocation = Geolocation(**geolocation_data)
    mock_geolocation.created_at = None
    mock_geolocation.url = None
    mocker.patch("src.geolocation.service.GeolocationService.request_geolocation_data", return_value=mock_geolocation)

    result = await GeolocationManager(session).create_geolocation(ip_geolocation_request)
    assert result.id is not None
    assert result.url == str(ip_geolocation_request.url)
    assert result.created_at == datetime(2025, 3, 16, 20, 0, 0)


@pytest.mark.asyncio
async def test_manager_get_geolocation_list(session):
    manager = GeolocationManager(session)
    result = await manager.get_geolocation_list()
    assert len(result) == 0

    session.add(GeolocationFactory.create())
    session.add(GeolocationFactory.create())
    session.add(GeolocationFactory.create())
    session.commit()
    result = await GeolocationManager(session).get_geolocation_list()
    assert len(result) == 3


@pytest.mark.asyncio
async def test_manager_get_geolocation(session):
    geolocation = GeolocationFactory.create()
    session.add(geolocation)
    session.commit()
    session.refresh(geolocation)

    result = await GeolocationManager(session).get_geolocation(pk=geolocation.id)
    assert geolocation == result


@pytest.mark.asyncio
async def test_manager_get_geolocation_does_not_exist(session):
    with pytest.raises(NotFoundError):
        await GeolocationManager(session).get_geolocation(pk=1)


@pytest.mark.asyncio
async def test_manager_delete_geolocation(session):
    geolocation = GeolocationFactory.create()
    session.add(geolocation)
    session.commit()
    session.refresh(geolocation)

    result = await GeolocationManager(session).delete_geolocation(pk=geolocation.id)
    geolocation_list = session.exec(select(Geolocation)).all()

    assert result is None
    assert len(geolocation_list) == 0


@pytest.mark.asyncio
async def test_manager_delete_geolocation_does_not_exist(session):
    with pytest.raises(DeletionError):
        await GeolocationManager(session).delete_geolocation(pk=1)
