from datetime import datetime

import factory
import faker
from src.geolocation.models import Geolocation

fake = faker.Faker()


class GeolocationFactory(factory.Factory):
    class Meta:
        model = Geolocation

    ip = fake.ipv4()
    type = "ipv4"
    continent_code = "EU"
    continent_name = "Europe"
    country_code = fake.country_code()
    country_name = fake.country()
    region_code = ""
    region_name = ""
    city = fake.city()
    zip = fake.postcode()
    latitude = factory.LazyAttribute(lambda obj: str(fake.latitude()))
    longitude = factory.LazyAttribute(lambda obj: str(fake.longitude()))
    created_at = datetime.now()
    url = fake.url()
