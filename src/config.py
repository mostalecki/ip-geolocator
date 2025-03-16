import os
import sys
from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Default configuration values.
    To override any value, include it in env file or export as env variable.
    """

    OPENAPI_URL: str | None = "/openapi.json"
    BASE_IPSTACK_URL: str
    IPSTACK_ACCESS_KEY: str

    # database
    DATABASE_URL: str = ""

    class Config:
        env_file = os.environ.get("ENV_FILE")


class TestSettings(BaseSettings):
    """
    Test configuration values.
    """

    OPENAPI_URL: str | None = None
    BASE_IPSTACK_URL: str = ""
    IPSTACK_ACCESS_KEY: str = ""
    DATABASE_URL: str = "sqlite:///test.db"


@lru_cache
def get_config():
    if "pytest" in sys.modules:
        return TestSettings()
    return Settings()


config = get_config()
