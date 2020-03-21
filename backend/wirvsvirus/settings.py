from pydantic import BaseSettings


class Settings(BaseSettings):

    host: str = "127.0.0.1"
    db_db: str = "default"
    db_url: str = "mongodb://root:pass@127.0.0.1:27017/default"

    class Config:
        env_prefix = "wirvsvirus_"


settings = Settings()
