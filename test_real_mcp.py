#!/usr/bin/env python3
"""
Script pour tester les vrais appels MCP ArXiv via Kiro.
Ce script montre comment faire des appels MCP réels une fois configurés.
"""

import asyncio
import json
import logging
from pathlib import Path

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def test_mcp_tools():
    """
    Test des outils MCP ArXiv réels.
    
    Note: Ce script nécessite que Kiro soit configuré avec MCP ArXiv.
    Les appels MCP réels doivent être faits via l'interface Kiro.
    """
    logger.info("🔧 Test des outils MCP ArXiv")
    
    # Vérifier la configuration MCP
    mcp_config_path = Path(".kiro/settings/mcp.json")
    if not mcp_config_path.exists():
        logger.error("❌ Configuration MCP non trouvée!")
        return False
    
    with open(mcp_config_path) as f:
        config = json.load(f)
    
    arxiv_config = config.get("mcpServers", {}).get("arxiv")
    if not arxiv_config:
        logger.error("❌ Configuration ArXiv MCP non trouvée!")
        return False
    
    logger.info("✅ Configuration MCP ArXiv trouvée:")
    logger.info(f"   Command: {arxiv_config.get('command')}")
    logger.info(f"   Args: {arxiv_config.get('args')}")
    logger.info(f"   Disabled: {arxiv_config.get('disabled', False)}")
    logger.info(f"   Auto-approve: {arxiv_config.get('autoApprove', [])}")
    
    # Instructions pour les tests réels
    logger.info("\n📋 INSTRUCTIONS POUR LES TESTS RÉELS:")
    logger.info("1. Assurez-vous que 'uv' est installé: pip install uv")
    logger.info("2. Dans Kiro, ouvrez la palette de commandes (Cmd/Ctrl+Shift+P)")
    logger.info("3. Cherchez 'MCP' et sélectionnez 'Reconnect MCP Servers'")
    logger.info("4. Vérifiez que le serveur ArXiv est connecté dans le panneau MCP")
    
    logger.info("\n🧪 TESTS À EFFECTUER MANUELLEMENT DANS KIRO:")
    
    # Test 1: Recherche
    logger.info("\n1️⃣ Test de recherche:")
    logger.info("   Demandez à Kiro: 'Recherche des papiers sur machine learning'")
    logger.info("   Ou utilisez directement l'outil search_arxiv")
    
    # Test 2: Détails
    logger.info("\n2️⃣ Test de détails:")
    logger.info("   Demandez à Kiro: 'Récupère les détails du papier 2301.07041'")
    logger.info("   Ou utilisez directement l'outil get_paper_details")
    
    # Test 3: PDF
    logger.info("\n3️⃣ Test de téléchargement:")
    logger.info("   Demandez à Kiro: 'Télécharge le PDF du papier 2301.07041'")
    logger.info("   Ou utilisez directement l'outil get_paper_pdf")
    
    return True


async def check_prerequisites():
    """Vérifie les prérequis pour MCP ArXiv."""
    logger.info("🔍 Vérification des prérequis...")
    
    # Vérifier uv
    import subprocess
    try:
        result = subprocess.run(['uv', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            logger.info(f"✅ uv installé: {result.stdout.strip()}")
        else:
            logger.warning("⚠️ uv non trouvé, installez avec: pip install uv")
    except FileNotFoundError:
        logger.warning("⚠️ uv non trouvé, installez avec: pip install uv")
    
    # Vérifier uvx
    try:
        result = subprocess.run(['uvx', '--help'], capture_output=True, text=True)
        if result.returncode == 0:
            logger.info("✅ uvx disponible")
        else:
            logger.warning("⚠️ uvx non disponible")
    except FileNotFoundError:
        logger.warning("⚠️ uvx non trouvé (inclus avec uv)")
    
    # Vérifier la configuration
    config_path = Path(".kiro/settings/mcp.json")
    if config_path.exists():
        logger.info("✅ Configuration MCP trouvée")
        return True
    else:
        logger.error("❌ Configuration MCP manquante")
        return False


def create_test_queries():
    """Crée des exemples de requêtes pour tester MCP ArXiv."""
    queries = {
        "search_examples": [
            {
                "description": "Recherche basique",
                "query": "artificial intelligence",
                "max_results": 5
            },
            {
                "description": "Recherche spécialisée",
                "query": "transformer neural networks",
                "max_results": 10,
                "sort_by": "submittedDate",
                "sort_order": "descending"
            },
            {
                "description": "Recherche par catégorie",
                "query": "cat:cs.AI",
                "max_results": 3
            }
        ],
        "paper_examples": [
            "2301.07041",  # Exemple d'ID ArXiv
            "2106.09685",  # LoRA paper
            "1706.03762"   # Attention is All You Need
        ]
    }
    
    logger.info("\n📝 EXEMPLES DE REQUÊTES POUR TESTS:")
    
    for i, example in enumerate(queries["search_examples"], 1):
        logger.info(f"\n{i}. {example['description']}:")
        logger.info(f"   Query: {example['query']}")
        logger.info(f"   Max results: {example['max_results']}")
        if 'sort_by' in example:
            logger.info(f"   Sort: {example['sort_by']} ({example['sort_order']})")
    
    logger.info(f"\n📄 IDs de papiers pour tests de détails:")
    for paper_id in queries["paper_examples"]:
        logger.info(f"   - {paper_id}")
    
    return queries


async def main():
    """Fonction principale."""
    logger.info("🚀 Test MCP ArXiv - Configuration et Prérequis")
    logger.info("=" * 60)
    
    # Vérifier les prérequis
    prereqs_ok = await check_prerequisites()
    
    if not prereqs_ok:
        logger.error("❌ Prérequis manquants, impossible de continuer")
        return
    
    # Tester la configuration MCP
    config_ok = await test_mcp_tools()
    
    if config_ok:
        # Créer des exemples de requêtes
        create_test_queries()
        
        logger.info("\n🎯 PROCHAINES ÉTAPES:")
        logger.info("1. Lancez Kiro IDE")
        logger.info("2. Reconnectez les serveurs MCP")
        logger.info("3. Testez les requêtes ci-dessus")
        logger.info("4. Vérifiez les logs MCP en cas de problème")
    
    logger.info("\n✨ Test de configuration terminé!")


if __name__ == "__main__":
    asyncio.run(main())