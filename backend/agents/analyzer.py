"""
Agent Analyseur - Analyse et synthétise les résultats
"""
from typing import Dict, List, Any
import logging
from collections import Counter

logger = logging.getLogger(__name__)


class AnalyzerAgent:
    """
    Agent responsable de l'analyse et de la synthèse des résultats
    """
    
    async def analyze(
        self,
        raw_results: Dict[str, List[Dict[str, Any]]],
        topic: str
    ) -> Dict[str, Any]:
        """
        Analyse les résultats bruts de toutes les sources
        
        Args:
            raw_results: Résultats de chaque source
            topic: Sujet de recherche
            
        Returns:
            Analyse structurée des résultats
        """
        logger.info("Analyse des résultats...")
        
        analysis = {
            "statistics": self._compute_statistics(raw_results),
            "top_sources": self._identify_top_sources(raw_results),
            "key_findings": self._extract_key_findings(raw_results),
            "trends": self._identify_trends(raw_results),
            "recommendations": self._generate_recommendations(raw_results, topic)
        }
        
        return analysis
    
    def _compute_statistics(self, raw_results: Dict[str, List]) -> Dict[str, Any]:
        """Calcule les statistiques générales"""
        total_results = sum(len(results) for results in raw_results.values())
        
        return {
            "total_results": total_results,
            "results_by_source": {
                source: len(results)
                for source, results in raw_results.items()
            },
            "sources_count": len(raw_results)
        }
    
    def _identify_top_sources(self, raw_results: Dict[str, List]) -> List[Dict[str, Any]]:
        """Identifie les sources les plus productives"""
        sources = [
            {
                "name": source,
                "count": len(results),
                "percentage": len(results) / max(sum(len(r) for r in raw_results.values()), 1) * 100
            }
            for source, results in raw_results.items()
        ]
        
        return sorted(sources, key=lambda x: x["count"], reverse=True)
    
    def _extract_key_findings(self, raw_results: Dict[str, List[Dict]]) -> List[str]:
        """Extrait les découvertes clés"""
        findings = []
        
        # Papers les plus cités
        cited_papers = []
        for source in ["arxiv", "semantic_scholar", "google_scholar"]:
            if source in raw_results:
                for paper in raw_results[source]:
                    citations = paper.get("citations", 0)
                    if citations and citations > 100:
                        cited_papers.append(paper)
        
        if cited_papers:
            findings.append(f"Trouvé {len(cited_papers)} articles hautement cités (>100 citations)")
        
        # Articles récents
        recent_count = 0
        for results in raw_results.values():
            for item in results:
                date = item.get("published_date", "")
                if date and ("2024" in str(date) or "2025" in str(date)):
                    recent_count += 1
        
        if recent_count:
            findings.append(f"{recent_count} publications récentes (2024-2025)")
        
        return findings
    
    def _identify_trends(self, raw_results: Dict[str, List[Dict]]) -> List[str]:
        """Identifie les tendances"""
        trends = []
        
        # Analyse des mots-clés fréquents dans les titres
        all_titles = []
        for results in raw_results.values():
            for item in results:
                title = item.get("title", "")
                if title:
                    all_titles.append(title.lower())
        
        if all_titles:
            # Mots communs (très simplifié)
            words = " ".join(all_titles).split()
            common_words = [w for w in words if len(w) > 5]
            word_counts = Counter(common_words).most_common(5)
            
            if word_counts:
                top_word = word_counts[0][0]
                trends.append(f"Terme fréquent: '{top_word}'")
        
        return trends
    
    def _generate_recommendations(
        self,
        raw_results: Dict[str, List],
        topic: str
    ) -> List[str]:
        """Génère des recommandations"""
        recommendations = []
        
        total = sum(len(results) for results in raw_results.values())
        
        if total > 50:
            recommendations.append("Grande quantité de littérature disponible - affiner la recherche pourrait être utile")
        elif total < 10:
            recommendations.append("Peu de résultats - élargir les termes de recherche pourrait être bénéfique")
        
        # Recommander des sources manquantes
        if "wikipedia" in raw_results and raw_results["wikipedia"]:
            recommendations.append("Consulter les pages Wikipedia pour une vue d'ensemble")
        
        if "arxiv" in raw_results and len(raw_results["arxiv"]) > 0:
            recommendations.append("Examiner les preprints arXiv pour les dernières avancées")
        
        return recommendations

