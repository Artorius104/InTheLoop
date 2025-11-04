"""
Service pour interagir avec ArXiv via MCP.
Utilise le serveur MCP ArXiv de blazickjp/arxiv-mcp-server.
"""

import asyncio
from datetime import datetime
from typing import List, Dict, Any, Optional
import logging


class ArxivService:
    """Service pour rechercher des papiers sur ArXiv via MCP."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        # TODO: Initialiser le client MCP une fois disponible
        self.mcp_client = None
    
    async def search_papers(
        self, 
        query: str, 
        max_results: int = 50,
        sort_by: str = "submittedDate",
        sort_order: str = "descending"
    ) -> List[Dict[str, Any]]:
        """
        Recherche des papiers sur ArXiv via MCP.
        
        Utilise l'outil 'search_arxiv' du serveur MCP ArXiv.
        """
        self.logger.info(f"Recherche de papiers pour: {query}")
        
        try:
            if self.mcp_client:
                # Appel MCP réel
                results = await self.mcp_client.call_tool(
                    "search_arxiv",
                    {
                        "query": query,
                        "max_results": max_results,
                        "sort_by": sort_by,
                        "sort_order": sort_order
                    }
                )
                return self._format_arxiv_results(results)
            else:
                # Fallback vers les données de test
                self.logger.warning("Client MCP non initialisé, utilisation des données de test")
                return await self._mock_arxiv_search(query, max_results)
                
        except Exception as e:
            self.logger.error(f"Erreur lors de la recherche MCP: {e}")
            return await self._mock_arxiv_search(query, max_results)
    
    async def _mock_arxiv_search(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """Données de test en attendant l'intégration MCP."""
        mock_papers = [
            {
                "arxiv_id": "2024.01001",
                "title": f"Advanced {query} Techniques",
                "authors": "John Doe, Jane Smith",
                "abstract": f"This paper presents novel approaches to {query} with significant improvements...",
                "categories": "cs.AI, cs.LG",
                "published_date": datetime.now(),
                "updated_date": datetime.now(),
                "pdf_url": "https://arxiv.org/pdf/2024.01001.pdf"
            }
        ]
        
        # Simuler une latence réseau
        await asyncio.sleep(0.1)
        
        return mock_papers[:max_results]
    
    async def get_paper_details(self, arxiv_id: str) -> Optional[Dict[str, Any]]:
        """Récupère les détails d'un papier spécifique via MCP."""
        self.logger.info(f"Récupération des détails pour: {arxiv_id}")
        
        try:
            if self.mcp_client:
                result = await self.mcp_client.call_tool(
                    "get_paper_details",
                    {"arxiv_id": arxiv_id}
                )
                return result
            else:
                self.logger.warning("Client MCP non initialisé")
                return None
                
        except Exception as e:
            self.logger.error(f"Erreur lors de la récupération des détails: {e}")
            return None
    
    async def download_pdf(self, arxiv_id: str, save_path: str) -> bool:
        """Télécharge le PDF d'un papier via MCP."""
        self.logger.info(f"Téléchargement du PDF pour: {arxiv_id}")
        
        try:
            if self.mcp_client:
                result = await self.mcp_client.call_tool(
                    "get_paper_pdf",
                    {
                        "arxiv_id": arxiv_id,
                        "save_path": save_path
                    }
                )
                return result is not None
            else:
                self.logger.warning("Client MCP non initialisé")
                return False
                
        except Exception as e:
            self.logger.error(f"Erreur lors du téléchargement: {e}")
            return False
    
    def _format_arxiv_results(self, raw_results: Any) -> List[Dict[str, Any]]:
        """Formate les résultats bruts de MCP ArXiv."""
        if not raw_results:
            return []
        
        formatted_papers = []
        
        # Adapter selon le format exact retourné par le serveur MCP
        for paper in raw_results:
            formatted_paper = {
                "arxiv_id": paper.get("arxiv_id", ""),
                "title": paper.get("title", ""),
                "authors": ", ".join(paper.get("authors", [])),
                "abstract": paper.get("summary", ""),
                "categories": ", ".join(paper.get("categories", [])),
                "published_date": self._parse_date(paper.get("published")),
                "updated_date": self._parse_date(paper.get("updated")),
                "pdf_url": paper.get("pdf_url", "")
            }
            formatted_papers.append(formatted_paper)
        
        return formatted_papers
    
    def _parse_date(self, date_str: Optional[str]) -> Optional[datetime]:
        """Parse une date au format ArXiv."""
        if not date_str:
            return None
        
        try:
            # Format ArXiv: "2023-01-17T18:59:59Z"
            return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        except Exception as e:
            self.logger.warning(f"Erreur de parsing de date {date_str}: {e}")
            return None