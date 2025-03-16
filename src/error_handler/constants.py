from typing import Type

from src.error_handler.exceptions import IpStackAuthorizationError, UserNotActiveError, UsageLimitReachedError

UPSTREAM_ERROR_CODE_MAP: dict[int, Type[BaseException]] = {
    101: IpStackAuthorizationError,
    102: UserNotActiveError,
    104: UsageLimitReachedError,
}
