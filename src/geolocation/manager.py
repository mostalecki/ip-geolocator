from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, select

from src.error_handler.exceptions import (
    NotFoundError,
    CancellationError,
)
from src.geolocation.models import IpGeolocationRequest, Geolocation
from src.geolocation.service import GeolocationService


class GeolocationManager:
    def __init__(self, session: Session):
        self.session = session

    async def get_or_create_geolocation(self, request_payload: IpGeolocationRequest) -> Geolocation:
        if request_payload.ip_address:
            query = select(Geolocation).where(Geolocation.ip == str(request_payload.ip_address))
            if geolocation := self.session.exec(query).first():
                return geolocation

        geolocation = await GeolocationService.request_geolocation_data(request_payload)
        self.session.add(geolocation)
        self.session.commit()
        self.session.refresh(geolocation)

        return geolocation

    async def get_geolocation_list(self) -> list[Geolocation]:
        """Returns the list of all geolocation objects."""
        return list(self.session.exec(select(Geolocation)).all())

    async def get_geolocation(self, pk: int) -> Geolocation:
        """
        Get geolocation by id.

        Raises:
            NotFoundError: When geolocation with given id does not exist.
        """
        try:
            return await self._get_geolocation_by_id(pk)
        except NoResultFound:
            raise NotFoundError

    async def delete_geolocation(self, pk: int) -> None:
        """
        Delete geolocation by id.

        Raises:
            CancellationError: When geolocation with given id does not exist.
        """
        geolocation = await self._get_geolocation_by_id(pk)
        try:
            self.session.delete(geolocation)
            self.session.commit()
        except NoResultFound:
            raise CancellationError(pk)

    async def _get_geolocation_by_id(self, pk: int) -> Geolocation:
        """
        Selects geolocation from database by id.

        Raises:
            sqlalchemy.exc.NoResultFound: When geolocation with given id does not exist.
        """
        query = select(Geolocation).where(Geolocation.id == pk)
        return self.session.exec(query).one()
