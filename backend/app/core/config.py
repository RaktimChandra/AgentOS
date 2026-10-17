"""Application configuration"""

from functools import lru_cache
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )
    
    # Application
    APP_NAME: str = "AgentOS"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://agentos:agentos@localhost:5432/agentos"
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 10
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_POOL_SIZE: int = 20
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # OPA (Policy Engine)
    OPA_URL: str = "http://localhost:8181"
    OPA_POLICY_PATH: str = "agentos/auth"
    
    # OpenTelemetry
    OTEL_ENABLED: bool = True
    OTEL_EXPORTER_JAEGER_ENDPOINT: str = "http://localhost:4317"
    OTEL_SERVICE_NAME: str = "agentos-api"
    
    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"
    
    # LLM Providers
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    
    # Budget Defaults
    DEFAULT_TOKEN_BUDGET: int = 100000
    DEFAULT_API_CALL_BUDGET: int = 1000
    DEFAULT_COST_BUDGET: float = 100.0
    DEFAULT_TIME_BUDGET_SECONDS: int = 300
    
    # Execution
    DEFAULT_EXECUTION_TIMEOUT: int = 300
    MAX_EXECUTION_TIMEOUT: int = 3600
    MAX_DELEGATION_DEPTH: int = 5
    
    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_PER_HOUR: int = 1000
    
    # Storage
    REPLAY_STORAGE_PATH: str = "./data/replays"
    TRACE_RETENTION_DAYS: int = 90
    AUDIT_LOG_RETENTION_DAYS: int = 2555  # 7 years


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
