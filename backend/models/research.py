"""
Modèles de données pour les recherches
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, Enum
from sqlalchemy.sql import func
from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum as PyEnum

from core.database import Base


class ResearchStatus(str, PyEnum):
    """Statuts possibles d'une recherche"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class ResearchDB(Base):
    """Modèle de base de données pour une recherche"""
    __tablename__ = "researches"
    
    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String(500), nullable=False)
    status = Column(Enum(ResearchStatus), default=ResearchStatus.PENDING)
    results = Column(JSON, nullable=True)
    error = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)


# Pydantic Models pour API
class ResearchRequest(BaseModel):
    """Requête de recherche"""
    topic: str = Field(..., min_length=3, max_length=500, description="Sujet scientifique à rechercher")
    sources: Optional[list[str]] = Field(
        default=["arxiv", "semantic_scholar", "wikipedia"],
        description="Sources à interroger"
    )
    max_results_per_source: Optional[int] = Field(default=10, ge=1, le=50)


class ResearchResponse(BaseModel):
    """Réponse de recherche"""
    id: int
    topic: str
    status: ResearchStatus
    created_at: datetime
    updated_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ResearchResult(BaseModel):
    """Résultats détaillés d'une recherche"""
    id: int
    topic: str
    status: ResearchStatus
    results: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class PaperResult(BaseModel):
    """Résultat d'un article scientifique"""
    title: str
    authors: list[str]
    abstract: str
    url: str
    published_date: Optional[str] = None
    source: str
    citations: Optional[int] = None
    pdf_url: Optional[str] = None


class NewsResult(BaseModel):
    """Résultat d'un article de presse"""
    title: str
    description: str
    url: str
    published_date: str
    source: str
    image_url: Optional[str] = None

