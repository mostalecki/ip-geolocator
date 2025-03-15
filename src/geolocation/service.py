import httpx
from pydantic import ValidationError

from src.config import config
from src.error_handler.exceptions import InvalidGeolocationError
from src.geolocation.models import Geolocation, IpGeolocationRequest


class GeolocationService:
    """Handles communication with Ipstack geolocation API."""

    @staticmethod
    async def request_geolocation_data(ip_address_request: IpGeolocationRequest) -> Geolocation:
        """
        Requests geolocation data from Ipstack API for given ip or url.

        Raises:
            InvalidGeolocationError: when data received from Ipstack API does not fit Geolocation model schema.
        """
        ip_address_or_url = str(ip_address_request.ip_address or ip_address_request.url.host)

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{config.BASE_IPSTACK_URL}/{ip_address_or_url}",
                params={"access_key": config.IPSTACK_ACCESS_KEY},
            )
        try:
            return Geolocation.model_validate(response.json())
        except ValidationError:
            raise InvalidGeolocationError
