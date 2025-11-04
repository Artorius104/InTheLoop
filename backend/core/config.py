"""
Configuration de l'application
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    """Configuration globale de l'application"""
    
    # API Keys
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    
    # Search APIs
    GOOGLE_API_KEY: str = ""
    GOOGLE_CSE_ID: str = ""
    SERPER_API_KEY: str = ""
    
    # Scholar APIs
    SEMANTIC_SCHOLAR_API_KEY: str = ""
    
    # News APIs
    NEWS_API_KEY: str = ""
    
    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./intheloop.db"
    
    # Server Config
    BACKEND_PORT: int = 8000
    FRONTEND_PORT: int = 3000
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:3001"]
    
    # MCP Config
    MCP_SERVER_HOST: str = "localhost"
    MCP_SERVER_BASE_PORT: int = 9000
    
    # Agent Config
    MAX_AGENT_ITERATIONS: int = 10
    AGENT_TIMEOUT: int = 300  # secondes
    MAX_CONCURRENT_SEARCHES: int = 5
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )


settings = Settings()

