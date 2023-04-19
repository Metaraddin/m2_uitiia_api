from pydantic import BaseSettings


class Settings(BaseSettings):
    authjwt_secret_key: str
    postgres_url: str
    timeout: int

    class Config:
        env_file = '../.env'
