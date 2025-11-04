"""
Agent Rapporteur - Génère les rapports finaux
"""
from typing import Dict, List, Any
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class ReporterAgent:
    """
    Agent responsable de la génération du rapport final
    """
    
    async def generate_report(
        self,
        topic: str,
        raw_results: Dict[str, List[Dict[str, Any]]],
        analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Génère un rapport complet de la recherche
        
        Args:
            topic: Sujet de recherche
            raw_results: Résultats bruts
            analysis: Analyse des résultats
            
        Returns:
            Rapport structuré
        """
        logger.info("Génération du rapport...")
        
        report = {
            "title": f"Veille Scientifique: {topic}",
            "generated_at": datetime.utcnow().isoformat(),
            "executive_summary": self._create_executive_summary(topic, analysis),
            "detailed_results": self._organize_results_by_source(raw_results),
            "top_papers": self._select_top_papers(raw_results),
            "insights": analysis.get("key_findings", []),
            "trends": analysis.get("trends", []),
            "recommendations": analysis.get("recommendations", []),
            "statistics": analysis.get("statistics", {}),
            "sources_used": list(raw_results.keys())
        }
        
        return report
    
    def _create_executive_summary(self, topic: str, analysis: Dict) -> str:
        """Crée un résumé exécutif"""
        stats = analysis.get("statistics", {})
        total = stats.get("total_results", 0)
        sources = stats.get("sources_count", 0)
        
        summary = (
            f"Recherche effectuée sur le sujet '{topic}'. "
            f"Total de {total} résultats trouvés à travers {sources} sources. "
        )
        
        findings = analysis.get("key_findings", [])
        if findings:
            summary += f"Points clés: {', '.join(findings[:2])}."
        
        return summary
    
    def _organize_results_by_source(
        self,
        raw_results: Dict[str, List[Dict]]
    ) -> Dict[str, List[Dict]]:
        """Organise les résultats par source"""
        organized = {}
        
        for source, results in raw_results.items():
            if results:
                organized[source] = {
                    "count": len(results),
                    "items": results[:10]  # Top 10 par source
                }
        
        return organized
    
    def _select_top_papers(
        self,
        raw_results: Dict[str, List[Dict]]
    ) -> List[Dict[str, Any]]:
        """Sélectionne les meilleurs papiers"""
        all_papers = []
        
        # Collecter tous les papiers avec citations
        for source in ["arxiv", "semantic_scholar", "google_scholar"]:
            if source in raw_results:
                for paper in raw_results[source]:
                    if paper.get("title"):
                        all_papers.append({
                            **paper,
                            "score": self._compute_paper_score(paper)
                        })
        
        # Trier par score
        all_papers.sort(key=lambda x: x["score"], reverse=True)
        
        # Retourner top 10
        return all_papers[:10]
    
    def _compute_paper_score(self, paper: Dict) -> float:
        """Calcule un score pour un papier"""
        score = 0.0
        
        # Citations
        citations = paper.get("citations", 0)
        if citations:
            score += min(citations / 100, 10)  # Max 10 points
        
        # Date de publication récente
        date = paper.get("published_date", "")
        if date and ("2024" in str(date) or "2025" in str(date)):
            score += 5
        
        # Présence d'abstract
        if paper.get("abstract"):
            score += 2
        
        # PDF disponible
        if paper.get("pdf_url"):
            score += 1
        
        return score

