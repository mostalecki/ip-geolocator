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
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Not Found"


class DeletionError(BaseAppException):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, pk: int | None = None):
        self.detail = f"Deletion failed: id {pk} not found"
        super().__init__(self.status_code, self.detail)


class InvalidGeolocationError(BaseAppException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Error occurred while fetching geolocation."


class IpStackAuthorizationError(BaseAppException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Error occurred while connecting to geolocation services. Please contact the administrator."


class UsageLimitReachedError(BaseAppException):
    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    detail = "The maximum allowed amount of monthly geolocation API requests has been reached. Please try again later."


class UserNotActiveError(BaseAppException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Error occurred while connecting to geolocation services. Please contact the administrator."
