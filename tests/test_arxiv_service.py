"""
Tests pour le service ArXiv.
"""

import pytest
import asyncio
from src.services.arxiv_service import ArxivService


@pytest.mark.asyncio
async def test_search_papers():
    """Test de recherche de papiers."""
    service = ArxivService()
    
    papers = await service.search_papers("machine learning", max_results=5)
    
    assert isinstance(papers, list)
    assert len(papers) <= 5
    
    if papers:
        paper = papers[0]
        assert "arxiv_id" in paper
        assert "title" in paper
        assert "authors" in paper
        assert "abstract" in paper


@pytest.mark.asyncio
async def test_search_papers_empty_query():
    """Test avec une requête vide."""
    service = ArxivService()
    
    papers = await service.search_papers("", max_results=1)
    
    assert isinstance(papers, list)