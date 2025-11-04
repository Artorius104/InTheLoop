"""
Configuration du système de veille.
"""

from pathlib import Path
from typing import List, Optional
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Configuration principale de l'application."""
    
    # API Keys
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    
    # Database
    database_url: str = Field("sqlite:///data/research_papers.db", env="DATABASE_URL")
    
    # Monitoring
    check_interval_hours: int = Field(24, env="CHECK_INTERVAL_HOURS")
    max_papers_per_query: int = Field(50, env="MAX_PAPERS_PER_QUERY")
    
    # Research domains
    research_domains: List[str] = Field(
        default=[
            "artificial intelligence",
            "machine learning",
            "deep learning",
            "natural language processing",
            "computer vision"
        ]
    )
    
    # Notifications
    enable_notifications: bool = Field(True, env="ENABLE_NOTIFICATIONS")
    notification_webhook_url: Optional[str] = Field(None, env="NOTIFICATION_WEBHOOK_URL")
    
    # Logging
    log_level: str = Field("INFO", env="LOG_LEVEL")
    log_file: str = Field("logs/app.log", env="LOG_FILE")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"