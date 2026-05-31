from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    OPEN_WEATHER_API_KEY: str

    REDIS_URL: str
    REDIS_PORT: int

    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    def get_db_url(self):
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    def get_redis_url(self):
        return f"redis://{self.REDIS_URL}"


settings = Settings()  # pyright: ignore[reportCallIssue]
