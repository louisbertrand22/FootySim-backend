from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "FootySim API"
    DATABASE_URL: str = "sqlite+aiosqlite:///./footysim.db"
    API_PREFIX: str = "/api/v1"
    # CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    class Config:
        env_file = ".env"

settings = Settings()
