from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: int
    DATABASE_URL: str
    JWT_SECRET_KEY: str
    BROKER_URL: str

    model_config = SettingsConfigDict(env_file=".env")

# Initialize settings object
settings = Settings()