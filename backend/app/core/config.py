from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    secret_key: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60
    database_url: str = "sqlite:///./exam_bread.db"
    max_upload_size_mb: int = 20

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)


settings = Settings()
