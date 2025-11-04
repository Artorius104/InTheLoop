#!/usr/bin/env python3
"""
Test complet des outils MCP ArXiv avec téléchargement réel de papiers.
"""

import asyncio
import json
import logging
import httpx
import os
from datetime import datetime
from pathlib import Path

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ArxivMCPTester:
    """Testeur pour les outils MCP ArXiv avec téléchargement réel."""
    
    def __init__(self):
        self.downloads_dir = Path("downloads")
        self.downloads_dir.mkdir(exist_ok=True)
        
    def test_mcp_configuration(self):
        """Vérifie la configuration MCP."""
        logger.info("🔧 Vérification de la configuration MCP ArXiv")
        
        try:
            with open('.kiro/settings/mcp.json', 'r') as f:
                config = json.load(f)
            
            arxiv_config = config.get('mcpServers', {}).get('arxiv', {})
            
            if arxiv_config:
                logger.info("✅ Configuration ArXiv trouvée:")
                logger.info(f"   Command: {arxiv_config.get('command')}")
                logger.info(f"   Args: {arxiv_config.get('args')}")
                logger.info(f"   Disabled: {arxiv_config.get('disabled', False)}")
                logger.info(f"   Auto-approve: {arxiv_config.get('autoApprove', [])}")
                
                if not arxiv_config.get('disabled', False):
                    logger.info("✅ Serveur MCP ArXiv activé")
                    return True
                else:
                    logger.warning("⚠️ Serveur MCP ArXiv désactivé")
                    return False
            else:
                logger.error("❌ Configuration ArXiv non trouvée")
                return False
                
        except FileNotFoundError:
            logger.error("❌ Fichier de configuration MCP non trouvé")
            return False
        except json.JSONDecodeError as e:
            logger.error(f"❌ Erreur de parsing JSON: {e}")
            return False
    
    async def download_paper_pdf(self, arxiv_id: str, title: str = None) -> bool:
        """Télécharge réellement un papier PDF depuis ArXiv."""
        logger.info(f"📥 Téléchargement du papier {arxiv_id}")
        
        # URL du PDF ArXiv
        pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
        
        # Nom du fichier
        safe_title = title.replace(" ", "_").replace("/", "_") if title else arxiv_id
        filename = f"{arxiv_id}_{safe_title[:50]}.pdf"
        filepath = self.downloads_dir / filename
        
        try:
            async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
                logger.info(f"   URL: {pdf_url}")
                logger.info(f"   Fichier: {filename}")
                
                response = await client.get(pdf_url)
                response.raise_for_status()
                
                # Vérifier que c'est bien un PDF
                content_type = response.headers.get('content-type', '')
                if 'pdf' not in content_type.lower():
                    logger.warning(f"⚠️ Type de contenu inattendu: {content_type}")
                
                # Sauvegarder le fichier
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                file_size = filepath.stat().st_size
                logger.info(f"✅ PDF téléchargé avec succès!")
                logger.info(f"   Taille: {file_size:,} bytes ({file_size/1024/1024:.2f} MB)")
                logger.info(f"   Chemin: {filepath}")
                
                return True
                
        except httpx.HTTPStatusError as e:
            logger.error(f"❌ Erreur HTTP {e.response.status_code}: {e}")
            return False
        except httpx.TimeoutException:
            logger.error("❌ Timeout lors du téléchargement")
            return False
        except Exception as e:
            logger.error(f"❌ Erreur lors du téléchargement: {e}")
            return False
    
    async def test_famous_papers(self):
        """Teste le téléchargement de papiers célèbres."""
        logger.info("📚 Test de téléchargement de papiers célèbres")
        
        famous_papers = [
            {
                "id": "1706.03762",
                "title": "Attention Is All You Need",
                "description": "Papier Transformer original (2017)"
            },
            {
                "id": "2303.08774",
                "title": "GPT-4 Technical Report",
                "description": "Rapport technique GPT-4 (2023)"
            },
            {
                "id": "1810.04805",
                "title": "BERT Pre-training",
                "description": "BERT: Pre-training of Deep Bidirectional Transformers (2018)"
            },
            {
                "id": "2106.09685",
                "title": "LoRA Low-Rank Adaptation",
                "description": "LoRA: Low-Rank Adaptation of Large Language Models (2021)"
            }
        ]
        
        successful_downloads = 0
        
        for i, paper in enumerate(famous_papers, 1):
            logger.info(f"\n📄 Papier {i}/4: {paper['description']}")
            logger.info(f"   ID: {paper['id']}")
            logger.info(f"   Titre: {paper['title']}")
            
            success = await self.download_paper_pdf(paper['id'], paper['title'])
            if success:
                successful_downloads += 1
            
            # Pause entre les téléchargements pour être respectueux
            if i < len(famous_papers):
                logger.info("   ⏳ Pause de 2 secondes...")
                await asyncio.sleep(2)
        
        logger.info(f"\n📊 Résumé des téléchargements:")
        logger.info(f"   Réussis: {successful_downloads}/{len(famous_papers)}")
        logger.info(f"   Dossier: {self.downloads_dir.absolute()}")
        
        return successful_downloads == len(famous_papers)
    
    async def test_recent_papers(self):
        """Teste le téléchargement de papiers récents."""
        logger.info("\n🆕 Test de téléchargement de papiers récents")
        
        # Papiers récents intéressants
        recent_papers = [
            {
                "id": "2310.06825",
                "title": "Language Agent Tree Search",
                "description": "LATS: Language Agent Tree Search (2023)"
            },
            {
                "id": "2307.09288",
                "title": "Llama 2 Open Foundation",
                "description": "Llama 2: Open Foundation and Fine-Tuned Chat Models (2023)"
            }
        ]
        
        successful_downloads = 0
        
        for i, paper in enumerate(recent_papers, 1):
            logger.info(f"\n📄 Papier récent {i}/{len(recent_papers)}: {paper['description']}")
            logger.info(f"   ID: {paper['id']}")
            
            success = await self.download_paper_pdf(paper['id'], paper['title'])
            if success:
                successful_downloads += 1
            
            if i < len(recent_papers):
                await asyncio.sleep(2)
        
        return successful_downloads > 0
    
    def list_downloaded_files(self):
        """Liste les fichiers téléchargés."""
        logger.info(f"\n📁 Fichiers téléchargés dans {self.downloads_dir}:")
        
        pdf_files = list(self.downloads_dir.glob("*.pdf"))
        
        if pdf_files:
            total_size = 0
            for pdf_file in sorted(pdf_files):
                size = pdf_file.stat().st_size
                total_size += size
                logger.info(f"   📄 {pdf_file.name} ({size/1024/1024:.2f} MB)")
            
            logger.info(f"\n📊 Total: {len(pdf_files)} fichiers, {total_size/1024/1024:.2f} MB")
        else:
            logger.info("   Aucun fichier PDF trouvé")
        
        return pdf_files


async def main():
    """Fonction principale de test."""
    logger.info("🚀 Test complet MCP ArXiv avec téléchargement réel")
    logger.info("=" * 60)
    
    tester = ArxivMCPTester()
    
    # Vérifier la configuration MCP
    config_ok = tester.test_mcp_configuration()
    
    if not config_ok:
        logger.error("❌ Configuration MCP incorrecte, arrêt des tests")
        return
    
    logger.info("\n🎯 DÉMARRAGE DES TESTS DE TÉLÉCHARGEMENT")
    
    try:
        # Test 1: Téléchargement de papiers célèbres
        logger.info("\n" + "="*50)
        success_famous = await tester.test_famous_papers()
        
        # Test 2: Téléchargement de papiers récents
        logger.info("\n" + "="*50)
        success_recent = await tester.test_recent_papers()
        
        # Résumé final
        logger.info("\n" + "="*60)
        logger.info("📊 RÉSUMÉ FINAL DES TESTS")
        logger.info(f"   Papiers célèbres: {'✅ OK' if success_famous else '⚠️ PARTIEL'}")
        logger.info(f"   Papiers récents: {'✅ OK' if success_recent else '⚠️ PARTIEL'}")
        
        # Liste des fichiers téléchargés
        tester.list_downloaded_files()
        
        if success_famous and success_recent:
            logger.info("\n🎉 Tous les tests de téléchargement réussis!")
        else:
            logger.info("\n⚠️ Certains téléchargements ont échoué")
        
        logger.info("\n💡 INSTRUCTIONS POUR TESTER MCP DANS KIRO:")
        logger.info("1. Demandez: 'Recherche des papiers sur transformer'")
        logger.info("2. Utilisez search_arxiv avec query: 'attention is all you need'")
        logger.info("3. Utilisez get_paper_details avec arxiv_id: '1706.03762'")
        logger.info("4. Utilisez get_paper_pdf avec arxiv_id: '1706.03762'")
        
    except KeyboardInterrupt:
        logger.info("\n⏹️ Tests interrompus par l'utilisateur")
    except Exception as e:
        logger.error(f"\n❌ Erreur lors des tests: {e}")
    
    logger.info("\n✨ Tests terminés!")


def test_single_paper():
    """Test rapide d'un seul papier."""
    async def quick_test():
        tester = ArxivMCPTester()
        logger.info("🚀 Test rapide - Téléchargement du papier Transformer")
        success = await tester.download_paper_pdf("1706.03762", "Attention Is All You Need")
        if success:
            logger.info("✅ Test rapide réussi!")
        else:
            logger.error("❌ Test rapide échoué")
    
    asyncio.run(quick_test())


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        test_single_paper()
    else:
        asyncio.run(main())