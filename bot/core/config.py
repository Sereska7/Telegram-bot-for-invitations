from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


load_dotenv()


class Settings(BaseSettings):
    TOKEN: str
    DB_URL: str
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int

    db_echo: bool = False

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
