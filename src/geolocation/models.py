from datetime import datetime

from pydantic import IPvAnyAddress, AnyUrl, model_validator
from pydantic.alias_generators import to_camel
from sqlmodel import SQLModel, Field
from sqlmodel._compat import SQLModelConfig


class BaseModel(SQLModel):
    model_config = SQLModelConfig(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
        coerce_numbers_to_str=True,
    )


class IpGeolocationRequest(BaseModel):
    ip_address: IPvAnyAddress | None = None
    url: AnyUrl | None = None

    @model_validator(mode="after")
    def check_ip_or_url_provided(self) -> "IpGeolocationRequest":
        if not (self.ip_address or self.url):
            raise ValueError("You must provide one of: ip_address, url")
        return self


class Geolocation(BaseModel, table=True):
    id: int | None = Field(default=None, nullable=False, primary_key=True)
    ip: str
    type: str
    continent_code: str
    continent_name: str
    country_code: str
    country_name: str
    region_code: str
    region_name: str
    city: str
    zip: str
    latitude: str
    longitude: str
    created_at: datetime | None = None
    url: str | None = None
