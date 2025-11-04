"""
InTheLoop - Main FastAPI Application
Point d'entrée de l'API backend
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from api.routes import research, health
from core.config import settings
from core.database import init_db

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestion du cycle de vie de l'application"""
    logger.info("🚀 Démarrage de InTheLoop...")
    await init_db()
    logger.info("✅ Base de données initialisée")
    yield
    logger.info("👋 Arrêt de InTheLoop")


app = FastAPI(
    title="InTheLoop API",
    description="API de veille scientifique intelligente avec framework agentic",
    version="1.0.0",
    lifespan=lifespan
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(health.router, prefix="/api", tags=["Health"])
app.include_router(research.router, prefix="/api/research", tags=["Research"])


@app.get("/")
async def root():
    """Page d'accueil de l'API"""
    return {
        "name": "InTheLoop API",
        "version": "1.0.0",
        "description": "Veille scientifique intelligente",
        "docs": "/docs",
        "status": "operational"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.BACKEND_PORT,
        reload=True
    )

