"""
Routes API pour les recherches scientifiques
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from core.database import get_session
from models.research import (
    ResearchRequest,
    ResearchResponse,
    ResearchResult,
    ResearchDB,
    ResearchStatus
)
from agents.coordinator import ResearchCoordinator
from sqlalchemy import select

router = APIRouter()


@router.post("/", response_model=ResearchResponse)
async def create_research(
    request: ResearchRequest,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_session)
):
    """
    Crée une nouvelle recherche scientifique
    La recherche sera exécutée en arrière-plan
    """
    # Créer l'enregistrement en base
    research = ResearchDB(
        topic=request.topic,
        status=ResearchStatus.PENDING
    )
    session.add(research)
    await session.commit()
    await session.refresh(research)
    
    # Lancer la recherche en arrière-plan
    background_tasks.add_task(
        run_research,
        research.id,
        request
    )
    
    return ResearchResponse.model_validate(research)


@router.get("/{research_id}", response_model=ResearchResult)
async def get_research(
    research_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Récupère les détails d'une recherche"""
    result = await session.execute(
        select(ResearchDB).where(ResearchDB.id == research_id)
    )
    research = result.scalar_one_or_none()
    
    if not research:
        raise HTTPException(status_code=404, detail="Recherche non trouvée")
    
    return ResearchResult.model_validate(research)


@router.get("/", response_model=List[ResearchResponse])
async def list_researches(
    skip: int = 0,
    limit: int = 10,
    session: AsyncSession = Depends(get_session)
):
    """Liste toutes les recherches"""
    result = await session.execute(
        select(ResearchDB)
        .order_by(ResearchDB.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    researches = result.scalars().all()
    
    return [ResearchResponse.model_validate(r) for r in researches]


async def run_research(research_id: int, request: ResearchRequest):
    """
    Exécute une recherche de manière asynchrone
    Cette fonction est appelée en arrière-plan
    """
    from core.database import async_session_maker
    from datetime import datetime
    
    async with async_session_maker() as session:
        try:
            # Récupérer la recherche
            result = await session.execute(
                select(ResearchDB).where(ResearchDB.id == research_id)
            )
            research = result.scalar_one()
            
            # Mettre à jour le statut
            research.status = ResearchStatus.IN_PROGRESS
            await session.commit()
            
            # Exécuter la recherche avec le coordinateur
            coordinator = ResearchCoordinator()
            results = await coordinator.run_research(
                topic=request.topic,
                sources=request.sources,
                max_results_per_source=request.max_results_per_source
            )
            
            # Sauvegarder les résultats
            research.status = ResearchStatus.COMPLETED
            research.results = results
            research.completed_at = datetime.utcnow()
            
        except Exception as e:
            research.status = ResearchStatus.FAILED
            research.error = str(e)
        
        await session.commit()

