from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "SDA API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "sda_db"
    
    DATABASE_URL: str | None = None
    
    # Server configuration
    SERVER_HOST: str = "127.0.0.1"  # Use local for Docker, nginx will proxy
    SERVER_PORT: str = "8000"
    
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_URL: str | None = None
    
    @property
    def get_redis_url(self) -> str:
        if self.REDIS_URL:
            return self.REDIS_URL
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/0"
    
    @property
    def sync_database_url(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = 'utf-8'

    @property
    def cors_origins(self) -> List[str]:
        return self.BACKEND_CORS_ORIGINS

settings = Settings()
