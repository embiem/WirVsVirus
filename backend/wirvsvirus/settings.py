from pydantic import BaseSettings


class Settings(BaseSettings):

    host: str = "127.0.0.1"
    db_host: str = "db"
    db_port: int = 27017
    db_user: str = "root"
    db_pass: str = "pass"
    db_db: str = "wirvsvirus"

    @property
    def db_url(self):
        return f"mongodb://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_db}"

    class Config:
        env_prefix = "wirvsvirus_"


settings = Settings()
