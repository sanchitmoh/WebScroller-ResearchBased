"""
ALCIS Configuration Management
"""
import os
from pathlib import Path
from typing import Optional, List
from pydantic import BaseSettings, Field


class DatabaseSettings(BaseSettings):
    """Database configuration"""
    url: str = Field(default="postgresql://alcis:alcis@localhost/alcis", env="DATABASE_URL")
    echo: bool = Field(default=False, env="DATABASE_ECHO")
    pool_size: int = Field(default=10, env="DATABASE_POOL_SIZE")
    max_overflow: int = Field(default=20, env="DATABASE_MAX_OVERFLOW")


class RedisSettings(BaseSettings):
    """Redis configuration"""
    url: str = Field(default="redis://localhost:6379/0", env="REDIS_URL")
    password: Optional[str] = Field(default=None, env="REDIS_PASSWORD")
    db: int = Field(default=0, env="REDIS_DB")


class SecuritySettings(BaseSettings):
    """Security configuration"""
    secret_key: str = Field(env="SECRET_KEY")
    encryption_key: str = Field(env="ENCRYPTION_KEY")
    jwt_algorithm: str = Field(default="HS256", env="JWT_ALGORITHM")
    jwt_expiration: int = Field(default=900, env="JWT_EXPIRATION")  # 15 minutes
    password_hash_rounds: int = Field(default=12, env="PASSWORD_HASH_ROUNDS")


class CrawlerSettings(BaseSettings):
    """Web crawler configuration"""
    user_agents: List[str] = Field(default=[
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ])
    default_timeout: int = Field(default=30, env="CRAWLER_TIMEOUT")
    max_retries: int = Field(default=3, env="CRAWLER_MAX_RETRIES")
    rate_limit: float = Field(default=1.0, env="CRAWLER_RATE_LIMIT")  # seconds between requests


class AISettings(BaseSettings):
    """AI and ML configuration"""
    model_name: str = Field(default="distilbert-base-uncased", env="AI_MODEL_NAME")
    confidence_threshold: float = Field(default=0.7, env="AI_CONFIDENCE_THRESHOLD")
    max_reasoning_steps: int = Field(default=10, env="AI_MAX_REASONING_STEPS")


class LoggingSettings(BaseSettings):
    """Logging configuration"""
    level: str = Field(default="INFO", env="LOG_LEVEL")
    format: str = Field(default="%(asctime)s - %(name)s - %(levelname)s - %(message)s", env="LOG_FORMAT")
    file_path: Optional[str] = Field(default=None, env="LOG_FILE_PATH")


class ALCISSettings(BaseSettings):
    """Main ALCIS configuration"""
    
    # Environment
    environment: str = Field(default="development", env="ENVIRONMENT")
    debug: bool = Field(default=True, env="DEBUG")
    
    # Project paths
    project_root: Path = Field(default_factory=lambda: Path(__file__).parent.parent)
    data_dir: Path = Field(default_factory=lambda: Path(__file__).parent.parent / "data")
    logs_dir: Path = Field(default_factory=lambda: Path(__file__).parent.parent / "logs")
    
    # Component settings
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    redis: RedisSettings = Field(default_factory=RedisSettings)
    security: SecuritySettings = Field(default_factory=SecuritySettings)
    crawler: CrawlerSettings = Field(default_factory=CrawlerSettings)
    ai: AISettings = Field(default_factory=AISettings)
    logging: LoggingSettings = Field(default_factory=LoggingSettings)
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = ALCISSettings()