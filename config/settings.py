"""
ALCIS Configuration Management
"""
import os
from pathlib import Path
from typing import Optional, List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class DatabaseSettings(BaseSettings):
    """Database configuration"""
    model_config = SettingsConfigDict(env_prefix="DATABASE_")
    
    url: str = "postgresql://alcis:alcis@localhost/alcis"
    echo: bool = False
    pool_size: int = 10
    max_overflow: int = 20


class RedisSettings(BaseSettings):
    """Redis configuration"""
    model_config = SettingsConfigDict(env_prefix="REDIS_")
    
    url: str = "redis://localhost:6379/0"
    password: Optional[str] = None
    db: int = 0


class SecuritySettings(BaseSettings):
    """Security configuration"""
    model_config = SettingsConfigDict(env_prefix="SECURITY_")
    
    secret_key: str = "test-secret-key"
    encryption_key: str = "test-encryption-key"
    jwt_algorithm: str = "HS256"
    jwt_expiration: int = 900  # 15 minutes
    password_hash_rounds: int = 12


class CrawlerSettings(BaseSettings):
    """Web crawler configuration"""
    model_config = SettingsConfigDict(env_prefix="CRAWLER_")
    
    user_agents: List[str] = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ]
    default_timeout: int = 30
    max_retries: int = 3
    rate_limit: float = 1.0  # seconds between requests


class AISettings(BaseSettings):
    """AI and ML configuration"""
    model_config = SettingsConfigDict(env_prefix="AI_")
    
    model_name: str = "distilbert-base-uncased"
    confidence_threshold: float = 0.7
    max_reasoning_steps: int = 10


class LoggingSettings(BaseSettings):
    """Logging configuration"""
    model_config = SettingsConfigDict(env_prefix="LOG_")
    
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file_path: Optional[str] = None


class ALCISSettings(BaseSettings):
    """Main ALCIS configuration"""
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"  # This will ignore extra environment variables
    )
    
    # Environment
    environment: str = "development"
    debug: bool = True
    
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


# Global settings instance
settings = ALCISSettings()