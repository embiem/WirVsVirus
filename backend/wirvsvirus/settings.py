from pydantic import BaseSettings


class Settings(BaseSettings):
    """General settings.

    Can be overriden by environment variables: i.e. host can be overridden by
    WIRSINDVIRUS_HOST.

    """
    # api settings
    host: str = "127.0.0.1"

    # database settings
    db_db: str = "default"
    db_url: str = "mongodb://root:pass@127.0.0.1:27017/default"

    # authentication settings
    auth_issuer: str = "https://dev-healthkeeper.eu.auth0.com/"
    ath_jwk_uri: str = "https://dev-healthkeeper.eu.auth0.com/.well-known/jwks.json"

    class Config:
        env_prefix = "wirvsvirus_"


settings = Settings()
