import uvicorn
from fastapi import FastAPI
from httpx import HTTPError
from sqlalchemy.exc import DatabaseError

from src.config import config
from src.error_handler.handler import ErrorHandler
from src.geolocation.routes import router as geolocation_router


class IpGeolocationAPI(FastAPI):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs, openapi_url=config.OPENAPI_URL)
        self.include_router(geolocation_router, tags=["geolocation"])
        self.add_exception_handler(HTTPError, ErrorHandler.handle_http_exception)
        self.add_exception_handler(DatabaseError, ErrorHandler.handle_database_exception)


app = IpGeolocationAPI()


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
    )
