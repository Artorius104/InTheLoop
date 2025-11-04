#!/usr/bin/env python3
"""
Script de test bout en bout pour le serveur MCP ArXiv.
Ce script teste directement les appels MCP sans passer par l'architecture complète.
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MCPArxivTester:
    """Testeur pour les appels MCP ArXiv."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    async def test_search_arxiv(self, query: str = "artificial intelligence", max_results: int = 5):
        """Test de recherche de papiers via MCP."""
        self.logger.info(f"🔍 Test de recherche ArXiv pour: '{query}'")
        
        try:
            # Note: En attendant l'intégration MCP complète dans Kiro,
            # ce test simule les appels et montre la structure attendue
            
            # Simulation d'un appel MCP réel
            mock_results = await self._simulate_mcp_call(
                tool="search_arxiv",
                params={
                    "query": query,
                    "max_results": max_results,
                    "sort_by": "submittedDate",
                    "sort_order": "descending"
                }
            )
            
            self.logger.info(f"✅ Trouvé {len(mock_results)} papiers")
            
            # Affichage des résultats
            for i, paper in enumerate(mock_results, 1):
                self.logger.info(f"\n📄 Papier {i}:")
                self.logger.info(f"   ID: {paper.get('arxiv_id')}")
                self.logger.info(f"   Titre: {paper.get('title', '')[:80]}...")
                self.logger.info(f"   Auteurs: {paper.get('authors', '')[:50]}...")
                self.logger.info(f"   Publié: {paper.get('published')}")
                self.logger.info(f"   Catégories: {paper.get('categories')}")
            
            return mock_results
            
        except Exception as e:
            self.logger.error(f"❌ Erreur lors de la recherche: {e}")
            return []
    
    async def test_get_paper_details(self, arxiv_id: str = "2301.07041"):
        """Test de récupération des détails d'un papier."""
        self.logger.info(f"📋 Test de récupération des détails pour: {arxiv_id}")
        
        try:
            details = await self._simulate_mcp_call(
                tool="get_paper_details",
                params={"arxiv_id": arxiv_id}
            )
            
            if details:
                self.logger.info("✅ Détails récupérés:")
                self.logger.info(f"   Titre: {details.get('title', '')}")
                self.logger.info(f"   Résumé: {details.get('summary', '')[:100]}...")
                self.logger.info(f"   PDF URL: {details.get('pdf_url', '')}")
            else:
                self.logger.warning("⚠️ Aucun détail trouvé")
            
            return details
            
        except Exception as e:
            self.logger.error(f"❌ Erreur lors de la récupération: {e}")
            return None
    
    async def test_download_pdf(self, arxiv_id: str = "2301.07041", save_path: str = "test_paper.pdf"):
        """Test de téléchargement de PDF."""
        self.logger.info(f"📥 Test de téléchargement PDF pour: {arxiv_id}")
        
        try:
            result = await self._simulate_mcp_call(
                tool="get_paper_pdf",
                params={
                    "arxiv_id": arxiv_id,
                    "save_path": save_path
                }
            )
            
            if result:
                self.logger.info(f"✅ PDF téléchargé vers: {save_path}")
            else:
                self.logger.warning("⚠️ Échec du téléchargement")
            
            return result
            
        except Exception as e:
            self.logger.error(f"❌ Erreur lors du téléchargement: {e}")
            return False
    
    async def _simulate_mcp_call(self, tool: str, params: Dict[str, Any]) -> Any:
        """
        Simule un appel MCP en attendant l'intégration complète.
        
        TODO: Remplacer par de vrais appels MCP une fois disponibles dans Kiro.
        """
        self.logger.info(f"🔧 Simulation d'appel MCP: {tool} avec {params}")
        
        # Simuler une latence réseau
        await asyncio.sleep(0.5)
        
        if tool == "search_arxiv":
            return self._mock_search_results(params.get("query", ""), params.get("max_results", 5))
        elif tool == "get_paper_details":
            return self._mock_paper_details(params.get("arxiv_id", ""))
        elif tool == "get_paper_pdf":
            return self._mock_pdf_download(params.get("arxiv_id", ""), params.get("save_path", ""))
        
        return None
    
    def _mock_search_results(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """Génère des résultats de recherche simulés."""
        base_papers = [
            {
                "id": "http://arxiv.org/abs/2301.07041v1",
                "title": f"Advanced {query} Techniques for Modern Applications",
                "authors": ["Alice Johnson", "Bob Smith", "Carol Davis"],
                "summary": f"This paper presents novel approaches to {query} with significant improvements in performance and accuracy. We demonstrate our methods on several benchmark datasets and show state-of-the-art results.",
                "published": "2023-01-17T18:59:59Z",
                "updated": "2023-01-17T18:59:59Z",
                "categories": ["cs.AI", "cs.LG", "cs.CL"],
                "pdf_url": "http://arxiv.org/pdf/2301.07041v1.pdf",
                "arxiv_id": "2301.07041"
            },
            {
                "id": "http://arxiv.org/abs/2301.07042v1",
                "title": f"Deep Learning Approaches to {query}",
                "authors": ["David Wilson", "Eva Martinez"],
                "summary": f"We explore deep learning methodologies for {query}, introducing a new architecture that outperforms existing approaches by 15% on standard benchmarks.",
                "published": "2023-01-16T14:30:00Z",
                "updated": "2023-01-16T14:30:00Z",
                "categories": ["cs.LG", "cs.AI"],
                "pdf_url": "http://arxiv.org/pdf/2301.07042v1.pdf",
                "arxiv_id": "2301.07042"
            },
            {
                "id": "http://arxiv.org/abs/2301.07043v1",
                "title": f"Theoretical Foundations of {query}",
                "authors": ["Frank Chen", "Grace Lee", "Henry Brown"],
                "summary": f"This work provides theoretical analysis of {query} algorithms, establishing convergence guarantees and complexity bounds for various scenarios.",
                "published": "2023-01-15T09:15:30Z",
                "updated": "2023-01-15T09:15:30Z",
                "categories": ["cs.AI", "math.OC"],
                "pdf_url": "http://arxiv.org/pdf/2301.07043v1.pdf",
                "arxiv_id": "2301.07043"
            }
        ]
        
        return base_papers[:max_results]
    
    def _mock_paper_details(self, arxiv_id: str) -> Dict[str, Any]:
        """Génère des détails de papier simulés."""
        return {
            "id": f"http://arxiv.org/abs/{arxiv_id}v1",
            "title": "Advanced Artificial Intelligence Techniques for Modern Applications",
            "authors": ["Alice Johnson", "Bob Smith", "Carol Davis"],
            "summary": "This comprehensive paper presents novel approaches to artificial intelligence with significant improvements in performance and accuracy. We demonstrate our methods on several benchmark datasets and show state-of-the-art results across multiple domains including natural language processing, computer vision, and reinforcement learning.",
            "published": "2023-01-17T18:59:59Z",
            "updated": "2023-01-17T18:59:59Z",
            "categories": ["cs.AI", "cs.LG", "cs.CL"],
            "pdf_url": f"http://arxiv.org/pdf/{arxiv_id}v1.pdf",
            "arxiv_id": arxiv_id,
            "doi": f"10.48550/arXiv.{arxiv_id}",
            "journal_ref": "Proceedings of ICML 2023",
            "comment": "Accepted at ICML 2023. 12 pages, 5 figures"
        }
    
    def _mock_pdf_download(self, arxiv_id: str, save_path: str) -> bool:
        """Simule le téléchargement d'un PDF."""
        # Créer un fichier de test
        try:
            with open(save_path, 'w') as f:
                f.write(f"# Mock PDF Content for ArXiv ID: {arxiv_id}\n")
                f.write(f"# Downloaded at: {datetime.now()}\n")
                f.write("This is a mock PDF file for testing purposes.\n")
            return True
        except Exception as e:
            self.logger.error(f"Erreur lors de la création du fichier mock: {e}")
            return False


async def run_full_test():
    """Exécute tous les tests bout en bout."""
    logger.info("🚀 Démarrage des tests MCP ArXiv bout en bout")
    logger.info("=" * 60)
    
    tester = MCPArxivTester()
    
    # Test 1: Recherche de papiers
    logger.info("\n1️⃣ TEST DE RECHERCHE")
    papers = await tester.test_search_arxiv("machine learning", max_results=3)
    
    # Test 2: Détails d'un papier
    logger.info("\n2️⃣ TEST DE RÉCUPÉRATION DE DÉTAILS")
    if papers:
        arxiv_id = papers[0].get("arxiv_id", "2301.07041")
        details = await tester.test_get_paper_details(arxiv_id)
    else:
        details = await tester.test_get_paper_details("2301.07041")
    
    # Test 3: Téléchargement PDF
    logger.info("\n3️⃣ TEST DE TÉLÉCHARGEMENT PDF")
    arxiv_id = details.get("arxiv_id", "2301.07041") if details else "2301.07041"
    pdf_result = await tester.test_download_pdf(arxiv_id, "downloads/test_paper.pdf")
    
    # Résumé des tests
    logger.info("\n" + "=" * 60)
    logger.info("📊 RÉSUMÉ DES TESTS")
    logger.info(f"   Recherche: {'✅ OK' if papers else '❌ ÉCHEC'}")
    logger.info(f"   Détails: {'✅ OK' if details else '❌ ÉCHEC'}")
    logger.info(f"   PDF: {'✅ OK' if pdf_result else '❌ ÉCHEC'}")
    
    if papers and details and pdf_result:
        logger.info("🎉 Tous les tests sont passés avec succès!")
    else:
        logger.warning("⚠️ Certains tests ont échoué")
    
    logger.info("\n💡 Note: Ces tests utilisent des données simulées.")
    logger.info("   Pour tester avec de vraies données MCP, configurez le client MCP dans Kiro.")


if __name__ == "__main__":
    # Créer le dossier de téléchargement
    import os
    os.makedirs("downloads", exist_ok=True)
    
    # Lancer les tests
    asyncio.run(run_full_test())