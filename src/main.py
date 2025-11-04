#!/usr/bin/env python3
"""
Point d'entrée principal du système de veille AI.
"""

import asyncio
import logging
from pathlib import Path

from config.settings import Settings
from agents.research_monitor import ResearchMonitorAgent
from core.database import DatabaseManager


async def main():
    """Fonction principale du système de veille."""
    # Configuration du logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    
    # Chargement de la configuration
    settings = Settings()
    
    # Initialisation de la base de données
    db_manager = DatabaseManager(settings.database_url)
    await db_manager.initialize()
    
    # Création de l'agent de monitoring
    monitor_agent = ResearchMonitorAgent(settings, db_manager)
    
    logger.info("Démarrage du système de veille AI")
    
    try:
        # Lancement du monitoring
        await monitor_agent.start_monitoring()
    except KeyboardInterrupt:
        logger.info("Arrêt du système demandé par l'utilisateur")
    except Exception as e:
        logger.error(f"Erreur critique: {e}")
    finally:
        await db_manager.close()
        logger.info("Système arrêté")


if __name__ == "__main__":
    asyncio.run(main())