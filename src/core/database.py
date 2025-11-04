"""
Gestionnaire de base de données pour le stockage des papiers de recherche.
"""

import asyncio
from datetime import datetime
from pathlib import Path
from typing import List, Optional
from sqlalchemy import create_engine, Column, String, DateTime, Text, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel


Base = declarative_base()


class ResearchPaper(Base):
    """Modèle de données pour un papier de recherche."""
    __tablename__ = "research_papers"
    
    arxiv_id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    authors = Column(Text, nullable=False)
    abstract = Column(Text, nullable=False)
    categories = Column(String, nullable=False)
    published_date = Column(DateTime, nullable=False)
    updated_date = Column(DateTime)
    pdf_url = Column(String, nullable=False)
    relevance_score = Column(Float, default=0.0)
    is_processed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class DatabaseManager:
    """Gestionnaire de base de données."""
    
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.engine = None
        self.SessionLocal = None
    
    async def initialize(self):
        """Initialise la base de données."""
        # Créer le dossier data s'il n'existe pas
        if "sqlite" in self.database_url:
            db_path = Path(self.database_url.replace("sqlite:///", ""))
            db_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.engine = create_engine(self.database_url)
        Base.metadata.create_all(bind=self.engine)
        self.SessionLocal = sessionmaker(bind=self.engine)
    
    async def close(self):
        """Ferme la connexion à la base de données."""
        if self.engine:
            self.engine.dispose()
    
    def get_session(self):
        """Retourne une session de base de données."""
        return self.SessionLocal()
    
    async def save_paper(self, paper_data: dict) -> bool:
        """Sauvegarde un papier de recherche."""
        try:
            with self.get_session() as session:
                paper = ResearchPaper(**paper_data)
                session.merge(paper)  # Utilise merge pour éviter les doublons
                session.commit()
                return True
        except Exception as e:
            print(f"Erreur lors de la sauvegarde: {e}")
            return False
    
    async def get_unprocessed_papers(self) -> List[ResearchPaper]:
        """Récupère les papiers non traités."""
        with self.get_session() as session:
            return session.query(ResearchPaper).filter(
                ResearchPaper.is_processed == False
            ).all()