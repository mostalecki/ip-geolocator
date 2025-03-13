from pydantic import ValidationError

from src.config import config
from src.error_handler.exceptions import InvalidGeolocationError
from src.geolocation.models import Geolocation, IpGeolocationRequest
from src.utils.request import send_request


class GeolocationService:
    @staticmethod
    async def request_geolocation_data(ip_address_request: IpGeolocationRequest) -> Geolocation:
        ip_address_or_url = (
            str(ip_address_request.ip_address) if ip_address_request.ip_address else ip_address_request.url.host
        )

        response = await send_request(
            f"{config.BASE_IPSTACK_URL}/{ip_address_or_url}",
            params={"access_key": config.IPSTACK_ACCESS_KEY},
        )
        try:
            return Geolocation.model_validate(response.json())
        except ValidationError:
            raise InvalidGeolocationError
