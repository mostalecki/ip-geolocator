from sqlalchemy import Sequence
from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, select

from src.error_handler.exceptions import (
    NotFoundError,
    CancellationError,
)
from src.geolocation.models import IpGeolocationRequest, Geolocation
from src.geolocation.service import GeolocationService


class GeolocationManager:
    async def get_or_create_geolocation(self, session: Session, request_payload: IpGeolocationRequest) -> Geolocation:
        if request_payload.ip_address:
            query = select(Geolocation).where(Geolocation.ip == str(request_payload.ip_address))
            if geolocation := session.exec(query).first():
                return geolocation

        geolocation = await GeolocationService.request_geolocation_data(request_payload)
        session.add(geolocation)
        session.commit()
        session.refresh(geolocation)

        return geolocation

    async def get_geolocation_list(self, session: Session) -> Sequence[Geolocation]:
        return session.exec(select(Geolocation)).all()

    async def get_geolocation(self, session: Session, pk: int) -> Geolocation:
        query = select(Geolocation).where(Geolocation.id == pk)
        try:
            return session.exec(query).one()
        except NoResultFound:
            raise NotFoundError

    async def delete_geolocation(self, session: Session, pk: int) -> None:
        query = select(Geolocation).where(Geolocation.id == pk)
        result = session.exec(query)
        try:
            session.delete(result.one())
            session.commit()
        except NoResultFound:
            raise CancellationError(pk)
