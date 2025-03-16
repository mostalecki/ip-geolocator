from datetime import datetime

import pytest
from pydantic import ValidationError

from src.geolocation.models import Geolocation, IpGeolocationRequest


def test_create_geolocation(session, geolocation_data):
    geolocation_data["createdAt"] = datetime.fromisoformat(geolocation_data["createdAt"])
    geolocation = Geolocation(**geolocation_data)
    session.add(geolocation)
    session.commit()
    session.refresh(geolocation)
    assert geolocation.id == 1


def test_ip_geolocation_request_requires_ip_or_url(session, client):
    IpGeolocationRequest(ip_address="127.0.0.1", url="http://google.com")
    IpGeolocationRequest(ip_address=None, url="http://google.com")
    IpGeolocationRequest(ip_address="127.0.0.1", url=None)

    with pytest.raises(ValidationError):
        IpGeolocationRequest(ip_address=None, url=None)
