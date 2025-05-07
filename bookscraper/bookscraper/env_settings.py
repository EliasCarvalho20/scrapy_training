from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    API_KEY: str
    DATABASE_URL: str
