"""
Routes de santé de l'API
"""
from fastapi import APIRouter
from datetime import datetime

router = APIRouter()


@router.get("/health")
async def health_check():
    """Vérification de l'état de l'API"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "InTheLoop API"
    }


@router.get("/ready")
async def readiness_check():
    """Vérification de la disponibilité de l'API"""
    # Ici on pourrait vérifier la connexion DB, les services externes, etc.
    return {
        "ready": True,
        "timestamp": datetime.utcnow().isoformat()
    }

