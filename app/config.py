from pydantic import BaseSettings


class Settings(BaseSettings):
    authjwt_secret_key: str
    postgres_url: str
    client_url: str
    timeout: int
    telegram_api_url: str
    telegram_bot_token: str
    telegram_channel_link: str

    class Config:
        env_file = '.env'
