"""
Agent Coordinateur - Orchestre les agents de recherche
"""
import asyncio
from typing import Dict, List, Any, Optional
import logging

from agents.planner import PlannerAgent
from agents.researchers import (
    ArxivResearcher,
    SemanticScholarResearcher,
    GoogleScholarResearcher,
    WikipediaResearcher,
    NewsResearcher,
    WebSearchResearcher
)
from agents.analyzer import AnalyzerAgent
from agents.reporter import ReporterAgent

logger = logging.getLogger(__name__)


class ResearchCoordinator:
    """
    Coordinateur principal du framework agentic
    Orchestre les différents agents pour réaliser une veille scientifique complète
    """
    
    def __init__(self):
        self.planner = PlannerAgent()
        self.analyzer = AnalyzerAgent()
        self.reporter = ReporterAgent()
        
        # Map des chercheurs disponibles
        self.researchers = {
            "arxiv": ArxivResearcher(),
            "semantic_scholar": SemanticScholarResearcher(),
            "google_scholar": GoogleScholarResearcher(),
            "wikipedia": WikipediaResearcher(),
            "news": NewsResearcher(),
            "web_search": WebSearchResearcher()
        }
    
    async def run_research(
        self,
        topic: str,
        sources: Optional[List[str]] = None,
        max_results_per_source: int = 10
    ) -> Dict[str, Any]:
        """
        Execute une recherche complète sur un sujet scientifique
        
        Args:
            topic: Sujet de recherche
            sources: Liste des sources à interroger (None = toutes)
            max_results_per_source: Nombre max de résultats par source
            
        Returns:
            Dictionnaire contenant les résultats de la recherche
        """
        logger.info(f"🎯 Début de la recherche sur: {topic}")
        
        try:
            # Étape 1: Planification
            logger.info("📋 Phase de planification...")
            plan = await self.planner.create_plan(topic, sources)
            
            # Étape 2: Recherche parallèle
            logger.info(f"🔍 Lancement de {len(plan['sources'])} recherches parallèles...")
            search_tasks = []
            
            for source_name in plan['sources']:
                if source_name in self.researchers:
                    researcher = self.researchers[source_name]
                    task = researcher.search(
                        query=plan['refined_query'],
                        max_results=max_results_per_source
                    )
                    search_tasks.append((source_name, task))
            
            # Exécuter toutes les recherches en parallèle
            raw_results = {}
            for source_name, task in search_tasks:
                try:
                    results = await task
                    raw_results[source_name] = results
                    logger.info(f"✅ {source_name}: {len(results)} résultats")
                except Exception as e:
                    logger.error(f"❌ Erreur {source_name}: {str(e)}")
                    raw_results[source_name] = []
            
            # Étape 3: Analyse et synthèse
            logger.info("🧠 Phase d'analyse...")
            analysis = await self.analyzer.analyze(raw_results, topic)
            
            # Étape 4: Génération du rapport
            logger.info("📊 Génération du rapport...")
            report = await self.reporter.generate_report(
                topic=topic,
                raw_results=raw_results,
                analysis=analysis
            )
            
            logger.info("✅ Recherche terminée avec succès")
            
            return {
                "topic": topic,
                "plan": plan,
                "raw_results": raw_results,
                "analysis": analysis,
                "report": report,
                "metadata": {
                    "total_sources": len(raw_results),
                    "total_results": sum(len(results) for results in raw_results.values())
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de la recherche: {str(e)}")
            raise

