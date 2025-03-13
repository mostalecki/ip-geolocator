import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Default configuration values.
    To override any value, include it in env file or export as env variable.
    """

    # URL where the OpenAPI schemas are served. If it's None, all documentation
    # UI is disabled. Locally, override this setting to enable documentation.
    # Example: OPENAPI_URL: Optional[str] = "/openapi.json"
    OPENAPI_URL: str | None = "/openapi.json"
    BASE_IPSTACK_URL: str
    IPSTACK_ACCESS_KEY: str

    # database
    DATABASE_URL: str = ""
    DATABASE_MIGRATION_URL: str = ""
    DATABASE_ISOLATION_LEVEL: str = "REPEATABLE READ"

    class Config:
        env_file = os.environ.get("ENV_FILE")


config = Settings()
