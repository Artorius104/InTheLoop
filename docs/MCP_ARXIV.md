# Documentation MCP ArXiv Server

## Vue d'ensemble

Ce projet utilise le serveur MCP ArXiv développé par blazickjp pour accéder aux papiers de recherche ArXiv.

**Repository**: https://github.com/blazickjp/arxiv-mcp-server

## Configuration

Le serveur MCP ArXiv est configuré dans `.kiro/settings/mcp.json` :

```json
{
  "mcpServers": {
    "arxiv": {
      "command": "uvx",
      "args": ["blazickjp/arxiv-mcp-server@latest"],
      "env": {
        "FASTMCP_LOG_LEVEL": "ERROR"
      },
      "disabled": false,
      "autoApprove": [
        "search_arxiv",
        "get_paper_details", 
        "get_paper_pdf"
      ]
    }
  }
}
```

## Outils disponibles

### 1. `search_arxiv`
Recherche des papiers sur ArXiv selon différents critères.

**Paramètres :**
- `query` (string) : Requête de recherche
- `max_results` (int, optionnel) : Nombre maximum de résultats (défaut: 10)
- `sort_by` (string, optionnel) : Critère de tri ("relevance", "lastUpdatedDate", "submittedDate")
- `sort_order` (string, optionnel) : Ordre de tri ("ascending", "descending")

**Exemple d'utilisation :**
```python
# Recherche de papiers sur l'IA
results = await search_arxiv(
    query="artificial intelligence",
    max_results=20,
    sort_by="submittedDate",
    sort_order="descending"
)
```

### 2. `get_paper_details`
Récupère les détails complets d'un papier spécifique.

**Paramètres :**
- `arxiv_id` (string) : Identifiant ArXiv du papier (ex: "2301.07041")

**Exemple d'utilisation :**
```python
# Récupération des détails d'un papier
details = await get_paper_details(arxiv_id="2301.07041")
```

### 3. `get_paper_pdf`
Télécharge le PDF d'un papier de recherche.

**Paramètres :**
- `arxiv_id` (string) : Identifiant ArXiv du papier
- `save_path` (string, optionnel) : Chemin de sauvegarde du PDF

**Exemple d'utilisation :**
```python
# Téléchargement du PDF
pdf_content = await get_paper_pdf(
    arxiv_id="2301.07041",
    save_path="papers/paper_2301.07041.pdf"
)
```

## Structure des données retournées

### Résultat de recherche
```json
{
  "id": "http://arxiv.org/abs/2301.07041v1",
  "title": "Titre du papier",
  "authors": ["Auteur 1", "Auteur 2"],
  "summary": "Résumé du papier...",
  "published": "2023-01-17T18:59:59Z",
  "updated": "2023-01-17T18:59:59Z",
  "categories": ["cs.AI", "cs.LG"],
  "pdf_url": "http://arxiv.org/pdf/2301.07041v1.pdf",
  "arxiv_id": "2301.07041"
}
```

## Installation et prérequis

1. **Installation d'uv et uvx :**
```bash
# Via pip
pip install uv

# Via homebrew (macOS)
brew install uv
```

2. **Le serveur MCP sera automatiquement téléchargé** lors de la première utilisation via uvx.

## Intégration dans le code

Le service ArXiv (`src/services/arxiv_service.py`) doit être mis à jour pour utiliser les outils MCP réels au lieu des données simulées.

### Exemple d'intégration

```python
async def search_papers(self, query: str, max_results: int = 50) -> List[Dict[str, Any]]:
    """Recherche des papiers via MCP ArXiv."""
    try:
        # Appel MCP réel (à implémenter)
        results = await self.mcp_client.call_tool(
            "search_arxiv",
            {
                "query": query,
                "max_results": max_results,
                "sort_by": "submittedDate",
                "sort_order": "descending"
            }
        )
        return self._format_arxiv_results(results)
    except Exception as e:
        self.logger.error(f"Erreur MCP ArXiv: {e}")
        return []
```

## Limitations et considérations

- **Rate limiting** : ArXiv impose des limites sur le nombre de requêtes
- **Taille des résultats** : Limiter le nombre de résultats pour éviter les timeouts
- **Gestion d'erreurs** : Prévoir des fallbacks en cas d'indisponibilité du service
- **Cache** : Considérer la mise en cache des résultats pour réduire les appels API

## Dépannage

### Problèmes courants

1. **Serveur MCP non trouvé** : Vérifier l'installation d'uvx
2. **Timeout des requêtes** : Réduire `max_results` ou ajouter des délais
3. **Erreurs de parsing** : Vérifier le format des identifiants ArXiv

### Logs et debugging

Ajuster le niveau de log dans la configuration :
```json
"env": {
  "FASTMCP_LOG_LEVEL": "DEBUG"
}
```