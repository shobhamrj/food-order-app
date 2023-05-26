from pydantic import BaseSettings


class Settings(BaseSettings):
    db_host: str
    db_pass: str
    db_user: str
    db_database: str
    db_port: int

    class Config:
        env_file = ".env"


settings = Settings()
