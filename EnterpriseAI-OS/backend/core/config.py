#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EnterpriseAI-OS - Configuration
إعدادات النظام
"""

from pydantic_settings import BaseSettings
from typing import List, Optional


class Settings(BaseSettings):
    """إعدادات التطبيق"""

    # === Application ===
    APP_NAME: str = "EnterpriseAI-OS"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "production"
    SECRET_KEY: str = "change-me-in-production"

    # === Database ===
    DATABASE_URL: str = "postgresql://enterpriseai:password@localhost:5432/enterpriseai"
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 10

    # === Cache ===
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_POOL_SIZE: int = 50

    # === Analytics ===
    CLICKHOUSE_URL: str = "clickhouse://localhost:8123/enterpriseai"

    # === Message Broker ===
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"
    KAFKA_TOPIC_PREFIX: str = "enterpriseai"

    # === AI ===
    AI_MODEL_PATH: str = "./models"
    AI_GPU_ENABLED: bool = False
    AI_GPU_DEVICE: str = "cuda:0"
    AI_BATCH_SIZE: int = 32
    AI_MAX_TOKENS: int = 4096
    AI_TEMPERATURE: float = 0.7
    AI_TOP_P: float = 0.9

    # === Security ===
    JWT_SECRET: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRY_HOURS: int = 24
    JWT_REFRESH_EXPIRY_DAYS: int = 7

    MFA_ENABLED: bool = True
    MFA_ISSUER: str = "EnterpriseAI-OS"

    ENCRYPTION_KEY: str = "change-me-in-production"

    # === CORS ===
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
    ]

    # === Rate Limiting ===
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW: int = 60

    # === Monitoring ===
    PROMETHEUS_ENABLED: bool = True
    SENTRY_DSN: Optional[str] = None
    LOG_LEVEL: str = "INFO"

    # === Email ===
    SMTP_HOST: str = "localhost"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_TLS: bool = True

    # === File Storage ===
    UPLOAD_DIR: str = "./data/uploads"
    MAX_UPLOAD_SIZE: int = 100 * 1024 * 1024  # 100MB

    # === AI Agents ===
    AGENTS_ENABLED: List[str] = [
        "financial",
        "inventory",
        "production",
        "accounting",
        "audit",
        "investment",
        "revenue",
        "hr",
        "marketing",
        "executive",
        "cross_department"
    ]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()
