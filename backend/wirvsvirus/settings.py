from pydantic import BaseSettings


class Settings(BaseSettings):

    host: str = "127.0.0.1"

    class Config:
        env_prefix = "wirvsvirus_"


settings = Settings()
