import pytest
from fastapi import status

from src.config import config
from src.error_handler.exceptions import InvalidGeolocationError, BaseAppException
from src.geolocation.models import Geolocation, IpGeolocationRequest
from src.geolocation.service import GeolocationService


@pytest.mark.asyncio
async def test_service_request_geolocation(httpx_mock, ip_geolocation_request, ipstack_response_success):
    httpx_mock.add_response(
        method="GET",
        url=f"{config.BASE_IPSTACK_URL}/151.101.65.140?access_key={config.IPSTACK_ACCESS_KEY}",
        json=ipstack_response_success,
        status_code=status.HTTP_200_OK,
    )
    geolocation = await GeolocationService().request_geolocation_data(ip_geolocation_request)

    assert isinstance(geolocation, Geolocation)


@pytest.mark.asyncio
async def test_service_request_geolocation_invalid_response_data(httpx_mock, ip_geolocation_request):
    httpx_mock.add_response(
        method="GET",
        url=f"{config.BASE_IPSTACK_URL}/151.101.65.140?access_key={config.IPSTACK_ACCESS_KEY}",
        json={},
        status_code=status.HTTP_200_OK,
    )
    with pytest.raises(InvalidGeolocationError):
        await GeolocationService().request_geolocation_data(ip_geolocation_request)


@pytest.mark.asyncio
async def test_service_handles_upstream_errors(httpx_mock, ip_geolocation_request):
    httpx_mock.add_response(
        method="GET",
        url=f"{config.BASE_IPSTACK_URL}/151.101.65.140?access_key={config.IPSTACK_ACCESS_KEY}",
        json={
            "success": False,
            "error": {"code": 106, "type": "invalid_ip_address", "info": "The IP Address supplied is invalid."},
        },
        status_code=status.HTTP_200_OK,
    )
    with pytest.raises(BaseAppException):
        await GeolocationService().request_geolocation_data(ip_geolocation_request)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "ip_address, url, expected_value",
    (
        ("127.0.0.1", None, "127.0.0.1"),
        (None, "https://google.com", "google.com"),
        ("127.0.0.1", "https://google.com", "127.0.0.1"),
    ),
)
async def test_service_handles_selects_correct_ip_or_url(
    httpx_mock, ipstack_response_success, ip_address, url, expected_value
):
    httpx_mock.add_response(
        method="GET",
        url=f"{config.BASE_IPSTACK_URL}/{expected_value}?access_key={config.IPSTACK_ACCESS_KEY}",
        json=ipstack_response_success,
        status_code=status.HTTP_200_OK,
    )
    ip_geolocation_request = IpGeolocationRequest(ip_address=ip_address, url=url)
    await GeolocationService().request_geolocation_data(ip_geolocation_request)
