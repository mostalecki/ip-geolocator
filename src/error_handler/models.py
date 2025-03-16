from src.geolocation.models import BaseModel


class UpstreamError(BaseModel):
    code: int
    type: str
    info: str
