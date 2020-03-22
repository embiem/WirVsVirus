from pydantic import BaseSettings

from os import environ


class Settings(BaseSettings):
    """General settings.

    Can be overriden by environment variables: i.e. host can be overridden by
    WIRSINDVIRUS_HOST.

    """
    # api settings
    host: str = "127.0.0.1"
    port: int = environ.get("PORT", 8000)

    # database settings
    db_url: str = "mongodb://root:pass@127.0.0.1:27017/default"

    # authentication settings
    auth_issuer: str = "https://dev-healthkeeper.eu.auth0.com/"
    auth_jwks_uri: str = "https://dev-healthkeeper.eu.auth0.com/.well-known/jwks.json"
    auth_token: str = ""  # auth token for testing

    auth_enabled: bool = True

    class Config:
        env_prefix = "wirvsvirus_"


settings = Settings()
