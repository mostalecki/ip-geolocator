import httpx
from pydantic import ValidationError

from src.config import config
from src.error_handler.exceptions import InvalidGeolocationError
from src.error_handler.handler import ErrorHandler
from src.error_handler.models import UpstreamError
from src.geolocation.models import Geolocation, IpGeolocationRequest


class GeolocationService:
    """Handles communication with Ipstack geolocation API."""

    async def request_geolocation_data(self, ip_address_request: IpGeolocationRequest) -> Geolocation:
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
        response_json = response.json()
        self._handle_errors(response_json)
        try:
            return Geolocation.model_validate(response_json)
        except ValidationError:
            raise InvalidGeolocationError

    @staticmethod
    def _handle_errors(response_json: dict) -> None:
        """
        Every response returned from Ipstack has status code 200, so it doesn't raise httpx exception.
        This method checks for possible error in payload and forwards it to error handler.
        """
        if response_json.get("success") is False:
            ErrorHandler.handle_upstream_error(UpstreamError(**response_json["error"]))
