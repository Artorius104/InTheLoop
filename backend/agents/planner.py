"""
Agent Planificateur - Crée la stratégie de recherche
"""
from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)


class PlannerAgent:
    """
    Agent responsable de la planification de la stratégie de recherche
    """
    
    async def create_plan(
        self,
        topic: str,
        requested_sources: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Crée un plan de recherche optimal
        
        Args:
            topic: Sujet de recherche
            requested_sources: Sources demandées (None = toutes)
            
        Returns:
            Plan de recherche avec query raffinée et sources à interroger
        """
        logger.info(f"Planification pour: {topic}")
        
        # Sources disponibles par défaut
        all_sources = [
            "arxiv",
            "semantic_scholar", 
            "google_scholar",
            "wikipedia",
            "news",
            "web_search"
        ]
        
        # Déterminer les sources à utiliser
        if requested_sources:
            sources = [s for s in requested_sources if s in all_sources]
        else:
            sources = all_sources
        
        # Raffiner la requête (ici simplifié, pourrait utiliser un LLM)
        refined_query = self._refine_query(topic)
        
        plan = {
            "original_topic": topic,
            "refined_query": refined_query,
            "sources": sources,
            "strategy": self._determine_strategy(topic),
            "keywords": self._extract_keywords(topic)
        }
        
        logger.info(f"Plan créé: {len(sources)} sources, query: {refined_query}")
        return plan
    
    def _refine_query(self, topic: str) -> str:
        """Raffine la requête de recherche"""
        # Simplification: retourne le topic tel quel
        # Dans une vraie implémentation, on utiliserait un LLM pour raffiner
        return topic.strip()
    
    def _determine_strategy(self, topic: str) -> str:
        """Détermine la stratégie de recherche"""
        # Simplification
        topic_lower = topic.lower()
        
        if any(word in topic_lower for word in ["recent", "new", "latest", "2024", "2025"]):
            return "recent_focus"
        elif any(word in topic_lower for word in ["overview", "survey", "review"]):
            return "comprehensive"
        else:
            return "balanced"
    
    def _extract_keywords(self, topic: str) -> List[str]:
        """Extrait les mots-clés du sujet"""
        # Simplification: split sur les espaces
        # Dans une vraie implémentation, on utiliserait NLP
        words = topic.lower().split()
        # Filtrer les mots trop courts
        keywords = [w for w in words if len(w) > 3]
        return keywords[:5]  # Max 5 keywords

