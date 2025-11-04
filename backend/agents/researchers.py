"""
Agents Chercheurs - Recherchent sur différentes sources
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any
import logging
import asyncio

logger = logging.getLogger(__name__)


class BaseResearcher(ABC):
    """Classe de base pour tous les chercheurs"""
    
    def __init__(self, name: str):
        self.name = name
    
    @abstractmethod
    async def search(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """Effectue une recherche"""
        pass
    
    def _create_result(self, **kwargs) -> Dict[str, Any]:
        """Helper pour créer un résultat standardisé"""
        return {
            "source": self.name,
            **kwargs
        }


class ArxivResearcher(BaseResearcher):
    """Chercheur arXiv"""
    
    def __init__(self):
        super().__init__("arxiv")
    
    async def search(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """Recherche sur arXiv"""
        try:
            import arxiv
            
            # Recherche asynchrone simulée
            await asyncio.sleep(0.1)  # Simulation
            
            search = arxiv.Search(
                query=query,
                max_results=max_results,
                sort_by=arxiv.SortCriterion.Relevance
            )
            
            results = []
            for paper in search.results():
                results.append(self._create_result(
                    title=paper.title,
                    authors=[author.name for author in paper.authors],
                    abstract=paper.summary,
                    url=paper.entry_id,
                    pdf_url=paper.pdf_url,
                    published_date=paper.published.strftime("%Y-%m-%d") if paper.published else None,
                    categories=paper.categories
                ))
            
            return results
            
        except Exception as e:
            logger.error(f"Erreur arXiv: {str(e)}")
            return []


class SemanticScholarResearcher(BaseResearcher):
    """Chercheur Semantic Scholar"""
    
    def __init__(self):
        super().__init__("semantic_scholar")
    
    async def search(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """Recherche sur Semantic Scholar"""
        try:
            import httpx
            from core.config import settings
            
            url = "https://api.semanticscholar.org/graph/v1/paper/search"
            params = {
                "query": query,
                "limit": max_results,
                "fields": "title,authors,abstract,url,year,citationCount,publicationDate"
            }
            
            headers = {}
            if settings.SEMANTIC_SCHOLAR_API_KEY:
                headers["x-api-key"] = settings.SEMANTIC_SCHOLAR_API_KEY
            
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params, headers=headers, timeout=30)
                response.raise_for_status()
                data = response.json()
            
            results = []
            for paper in data.get("data", []):
                results.append(self._create_result(
                    title=paper.get("title", ""),
                    authors=[a.get("name", "") for a in paper.get("authors", [])],
                    abstract=paper.get("abstract", ""),
                    url=f"https://www.semanticscholar.org/paper/{paper.get('paperId', '')}",
                    published_date=paper.get("publicationDate"),
                    citations=paper.get("citationCount", 0)
                ))
            
            return results
            
        except Exception as e:
            logger.error(f"Erreur Semantic Scholar: {str(e)}")
            return []


class GoogleScholarResearcher(BaseResearcher):
    """Chercheur Google Scholar"""
    
    def __init__(self):
        super().__init__("google_scholar")
    
    async def search(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """Recherche sur Google Scholar"""
        try:
            from scholarly import scholarly
            
            # Note: scholarly peut être bloqué, utiliser avec prudence
            await asyncio.sleep(0.1)
            
            search_query = scholarly.search_pubs(query)
            
            results = []
            for i, paper in enumerate(search_query):
                if i >= max_results:
                    break
                
                results.append(self._create_result(
                    title=paper.get('bib', {}).get('title', ''),
                    authors=paper.get('bib', {}).get('author', []),
                    abstract=paper.get('bib', {}).get('abstract', ''),
                    url=paper.get('pub_url', ''),
                    published_date=paper.get('bib', {}).get('pub_year'),
                    citations=paper.get('num_citations', 0)
                ))
            
            return results
            
        except Exception as e:
            logger.error(f"Erreur Google Scholar: {str(e)}")
            return []


class WikipediaResearcher(BaseResearcher):
    """Chercheur Wikipedia"""
    
    def __init__(self):
        super().__init__("wikipedia")
    
    async def search(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """Recherche sur Wikipedia"""
        try:
            import wikipedia
            
            await asyncio.sleep(0.1)
            
            # Rechercher des pages
            search_results = wikipedia.search(query, results=max_results)
            
            results = []
            for title in search_results[:max_results]:
                try:
                    page = wikipedia.page(title, auto_suggest=False)
                    results.append(self._create_result(
                        title=page.title,
                        summary=page.summary,
                        url=page.url,
                        categories=page.categories[:5] if hasattr(page, 'categories') else []
                    ))
                except:
                    continue
            
            return results
            
        except Exception as e:
            logger.error(f"Erreur Wikipedia: {str(e)}")
            return []


class NewsResearcher(BaseResearcher):
    """Chercheur d'actualités scientifiques"""
    
    def __init__(self):
        super().__init__("news")
    
    async def search(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """Recherche d'actualités"""
        try:
            import httpx
            from core.config import settings
            
            if not settings.NEWS_API_KEY:
                logger.warning("NEWS_API_KEY non configurée")
                return []
            
            url = "https://newsapi.org/v2/everything"
            params = {
                "q": query,
                "apiKey": settings.NEWS_API_KEY,
                "language": "en",
                "sortBy": "relevancy",
                "pageSize": max_results
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params, timeout=30)
                response.raise_for_status()
                data = response.json()
            
            results = []
            for article in data.get("articles", []):
                results.append(self._create_result(
                    title=article.get("title", ""),
                    description=article.get("description", ""),
                    url=article.get("url", ""),
                    published_date=article.get("publishedAt", ""),
                    source_name=article.get("source", {}).get("name", ""),
                    image_url=article.get("urlToImage")
                ))
            
            return results
            
        except Exception as e:
            logger.error(f"Erreur News: {str(e)}")
            return []


class WebSearchResearcher(BaseResearcher):
    """Chercheur web générique"""
    
    def __init__(self):
        super().__init__("web_search")
    
    async def search(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """Recherche web générique"""
        try:
            import httpx
            from core.config import settings
            
            if not settings.SERPER_API_KEY:
                logger.warning("SERPER_API_KEY non configurée")
                return []
            
            url = "https://google.serper.dev/search"
            payload = {
                "q": query,
                "num": max_results
            }
            headers = {
                "X-API-KEY": settings.SERPER_API_KEY,
                "Content-Type": "application/json"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload, headers=headers, timeout=30)
                response.raise_for_status()
                data = response.json()
            
            results = []
            for result in data.get("organic", [])[:max_results]:
                results.append(self._create_result(
                    title=result.get("title", ""),
                    description=result.get("snippet", ""),
                    url=result.get("link", ""),
                    position=result.get("position", 0)
                ))
            
            return results
            
        except Exception as e:
            logger.error(f"Erreur Web Search: {str(e)}")
            return []

