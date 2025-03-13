from fastapi import status
from fastapi.responses import JSONResponse

from src.error_handler.exceptions import BaseAppException


class ErrorHandler:
    @classmethod
    def handle_http_exception(cls, *args) -> JSONResponse:
        return cls.convert_error_to_json_response(
            BaseAppException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error occurred while connecting to geolocation provider.",
            )
        )

    @classmethod
    def handle_database_exception(cls, *args) -> JSONResponse:
        return cls.convert_error_to_json_response(
            BaseAppException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Database error occurred.",
            )
        )

    @classmethod
    def convert_error_to_json_response(cls, exception: BaseAppException) -> JSONResponse:
        return JSONResponse(
            status_code=exception.status_code,
            content={"error": exception.detail},
        )
