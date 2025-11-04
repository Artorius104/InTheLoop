"""
Agent principal de monitoring des papiers de recherche.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any

from config.settings import Settings
from core.database import DatabaseManager
from services.arxiv_service import ArxivService
from services.ai_analyzer import AIAnalyzer


class ResearchMonitorAgent:
    """Agent de monitoring des papiers de recherche."""
    
    def __init__(self, settings: Settings, db_manager: DatabaseManager):
        self.settings = settings
        self.db_manager = db_manager
        self.arxiv_service = ArxivService()
        self.ai_analyzer = AIAnalyzer(settings.openai_api_key)
        self.logger = logging.getLogger(__name__)
        self.is_running = False
    
    async def start_monitoring(self):
        """Démarre le processus de monitoring."""
        self.is_running = True
        self.logger.info("Démarrage du monitoring des papiers de recherche")
        
        while self.is_running:
            try:
                await self._monitoring_cycle()
                
                # Attendre avant le prochain cycle
                await asyncio.sleep(self.settings.check_interval_hours * 3600)
                
            except Exception as e:
                self.logger.error(f"Erreur dans le cycle de monitoring: {e}")
                await asyncio.sleep(300)  # Attendre 5 minutes avant de réessayer
    
    async def stop_monitoring(self):
        """Arrête le monitoring."""
        self.is_running = False
        self.logger.info("Arrêt du monitoring demandé")
    
    async def _monitoring_cycle(self):
        """Exécute un cycle complet de monitoring."""
        self.logger.info("Début du cycle de monitoring")
        
        # 1. Rechercher de nouveaux papiers
        new_papers = await self._search_new_papers()
        self.logger.info(f"Trouvé {len(new_papers)} nouveaux papiers")
        
        # 2. Analyser et scorer les papiers
        for paper in new_papers:
            try:
                # Analyser la pertinence
                relevance_score = await self.ai_analyzer.analyze_relevance(
                    paper['title'], 
                    paper['abstract']
                )
                paper['relevance_score'] = relevance_score
                
                # Sauvegarder en base
                await self.db_manager.save_paper(paper)
                
            except Exception as e:
                self.logger.error(f"Erreur lors de l'analyse du papier {paper.get('arxiv_id')}: {e}")
        
        # 3. Traiter les papiers non traités
        await self._process_unprocessed_papers()
        
        self.logger.info("Cycle de monitoring terminé")
    
    async def _search_new_papers(self) -> List[Dict[str, Any]]:
        """Recherche de nouveaux papiers sur ArXiv."""
        all_papers = []
        
        for domain in self.settings.research_domains:
            try:
                papers = await self.arxiv_service.search_papers(
                    query=domain,
                    max_results=self.settings.max_papers_per_query
                )
                all_papers.extend(papers)
                
            except Exception as e:
                self.logger.error(f"Erreur lors de la recherche pour '{domain}': {e}")
        
        return all_papers
    
    async def _process_unprocessed_papers(self):
        """Traite les papiers non traités."""
        unprocessed = await self.db_manager.get_unprocessed_papers()
        
        for paper in unprocessed:
            try:
                # Ici vous pouvez ajouter des traitements supplémentaires
                # comme l'envoi de notifications, la génération de résumés, etc.
                
                # Marquer comme traité
                paper.is_processed = True
                
            except Exception as e:
                self.logger.error(f"Erreur lors du traitement du papier {paper.arxiv_id}: {e}")