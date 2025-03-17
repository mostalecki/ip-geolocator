from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from src.geolocation.models import IpGeolocationRequest, Geolocation
from src.geolocation.manager import GeolocationManager
from src.utils.database import get_session

router = APIRouter()


@router.post(
    "/geolocation",
    status_code=status.HTTP_201_CREATED,
    description=(
            "Fetch geolocation data for provided ip address or url. "
            "If both `ipAddress` and `url` are provided, `ipAddress` takes priority."
    )
)
async def create_geolocation(payload: IpGeolocationRequest, session: Session = Depends(get_session)) -> Geolocation:
    return await GeolocationManager(session).create_geolocation(payload)


@router.get("/geolocation")
async def get_geolocation_list(
    session: Session = Depends(get_session),
) -> list[Geolocation]:
    return await GeolocationManager(session).get_geolocation_list()


@router.get("/geolocation/{pk}")
async def get_geolocation_detail(pk: int, session: Session = Depends(get_session)) -> Geolocation:
    return await GeolocationManager(session).get_geolocation(pk)


@router.delete("/geolocation/{pk}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_geolocation(pk: int, session: Session = Depends(get_session)) -> None:
    return await GeolocationManager(session).delete_geolocation(pk)
