from typing import NoReturn

from fastapi import status
from fastapi.responses import JSONResponse
from httpx import HTTPError
from sqlalchemy.exc import DatabaseError

from src.error_handler.constants import UPSTREAM_ERROR_CODE_MAP
from src.error_handler.exceptions import BaseAppException
from src.error_handler.models import UpstreamError
from src.utils.logger import logger


class ErrorHandler:
    @classmethod
    def handle_upstream_error(cls, upstream_error: UpstreamError) -> NoReturn:
        """Handle an upstream error and transform it into BaseAppException"""
        raise UPSTREAM_ERROR_CODE_MAP.get(upstream_error.code, BaseAppException)

    @classmethod
    def handle_base_app_exception(cls, _, base_app_exception: BaseAppException) -> JSONResponse:
        """Global handler for BaseAppException derived exceptions."""
        return cls._convert_error_to_json_response(base_app_exception)

    @classmethod
    def handle_http_exception(cls, _, error: HTTPError) -> JSONResponse:
        """Global handler for httpx exceptions."""
        logger.error(f"Upstream http error occurred: {error}")
        return cls._convert_error_to_json_response(
            BaseAppException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error occurred while connecting to geolocation provider. Please try again later.",
            )
        )

    @classmethod
    def handle_database_exception(cls, _, error: DatabaseError) -> JSONResponse:
        """Global handler for database exceptions."""
        logger.error(f"Database error occurred: {error}")
        return cls._convert_error_to_json_response(
            BaseAppException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Database error occurred. Please try again later.",
            )
        )

    @classmethod
    def _convert_error_to_json_response(cls, exception: BaseAppException) -> JSONResponse:
        """Converts a BaseAppException into JSONResponse."""
        return JSONResponse(
            status_code=exception.status_code,
            content={"error": exception.detail},
        )
