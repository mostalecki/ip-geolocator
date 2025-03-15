from fastapi import HTTPException, status


class BaseAppException(HTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Something went wrong."

    def __init__(
        self,
        status_code: status = None,
        detail: str = None,
    ):
        if status_code:
            self.status_code = status_code
        if detail:
            self.detail = detail


class NotFoundError(BaseAppException):
    status_code = 404
    detail = "Not Found"


class CancellationError(BaseAppException):
    status_code = 400

    def __init__(self, pk: int | None = None):
        self.detail = f"Cancellation failed: id {pk} not found"
        super().__init__(self.status_code, self.detail)


class InvalidGeolocationError(BaseAppException):
    status_code = 400
    detail = "Error occurred while fetching geolocation."
