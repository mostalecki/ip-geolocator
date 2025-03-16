import pytest

from src.config import config
from src.error_handler.exceptions import InvalidGeolocationError
from src.geolocation.models import Geolocation
from src.geolocation.service import GeolocationService


@pytest.mark.asyncio
async def test_service_request_geolocation(httpx_mock, ip_geolocation_request, ipstack_response_payload_success):
    httpx_mock.add_response(
        method="GET",
        url=f"{config.BASE_IPSTACK_URL}/151.101.65.140?access_key={config.IPSTACK_ACCESS_KEY}",
        json=ipstack_response_payload_success,
    )
    geolocation = await GeolocationService.request_geolocation_data(ip_geolocation_request)

    assert isinstance(geolocation, Geolocation)


@pytest.mark.asyncio
async def test_service_request_geolocation_invalid_response_data(
    httpx_mock, ip_geolocation_request, ipstack_response_payload_success
):
    httpx_mock.add_response(
        method="GET", url=f"{config.BASE_IPSTACK_URL}/151.101.65.140?access_key={config.IPSTACK_ACCESS_KEY}", json={}
    )
    with pytest.raises(InvalidGeolocationError):
        await GeolocationService.request_geolocation_data(ip_geolocation_request)
