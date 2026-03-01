from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    APP_TITLE: str
    DB_NAME: str
    LOG_FILE: str
    LOG_LEVEL: str
    HOST: str
    PORT: int

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

settings = Settings()
