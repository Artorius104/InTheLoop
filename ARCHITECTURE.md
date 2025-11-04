# Architecture - InTheLoop

## Vue d'Ensemble

InTheLoop est une plateforme de veille scientifique utilisant un framework agentic pour orchestrer la recherche d'informations à travers multiples sources.

## Architecture Globale

```
┌─────────────────────────────────────────────────────┐
│                    Frontend (React)                  │
│            UI moderne avec TailwindCSS               │
└──────────────────┬──────────────────────────────────┘
                   │ HTTP/REST
                   ▼
┌─────────────────────────────────────────────────────┐
│              Backend (FastAPI)                       │
│  ┌───────────────────────────────────────────────┐  │
│  │         Framework Agentic                      │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐   │  │
│  │  │Planner   │→ │Researchers│→ │Analyzer  │   │  │
│  │  │Agent     │  │(parallel) │  │Agent     │   │  │
│  │  └──────────┘  └──────────┘  └──────────┘   │  │
│  │                       ↓                        │  │
│  │                  ┌──────────┐                 │  │
│  │                  │Reporter  │                 │  │
│  │                  │Agent     │                 │  │
│  │                  └──────────┘                 │  │
│  └───────────────────────────────────────────────┘  │
│                       │                              │
│                       │ MCP Protocol                 │
│                       ▼                              │
│  ┌───────────────────────────────────────────────┐  │
│  │           MCP Servers (TypeScript)            │  │
│  │  [arXiv] [Scholar] [Wiki] [News] [Web]       │  │
│  └───────────────────────────────────────────────┘  │
└──────────────────┬──────────────────────────────────┘
                   │ HTTPS/API Calls
                   ▼
┌─────────────────────────────────────────────────────┐
│              External APIs                           │
│  • arXiv.org                                        │
│  • Semantic Scholar API                             │
│  • Wikipedia API                                    │
│  • Google (via Serper)                              │
│  • NewsAPI                                          │
└─────────────────────────────────────────────────────┘
```

## Composants Principaux

### 1. Frontend (React + TypeScript)

**Technologies** :
- React 18 + TypeScript
- Vite (build tool)
- TailwindCSS (styling)
- React Router (routing)
- TanStack Query (data fetching)

**Structure** :
```
frontend/
├── src/
│   ├── components/      # Composants réutilisables
│   │   └── Layout.tsx
│   ├── pages/           # Pages de l'app
│   │   ├── HomePage.tsx
│   │   ├── ResearchPage.tsx
│   │   └── HistoryPage.tsx
│   ├── services/        # API clients
│   │   └── api.ts
│   ├── App.tsx          # Composant racine
│   └── main.tsx         # Point d'entrée
```

**Flow** :
1. Utilisateur soumet une recherche
2. Requête POST vers backend
3. Polling automatique pour updates
4. Affichage des résultats formatés

### 2. Backend (FastAPI + Python)

**Technologies** :
- FastAPI (framework web)
- SQLAlchemy (ORM)
- Pydantic (validation)
- Asyncio (async/await)

**Structure** :
```
backend/
├── agents/              # Framework agentic
│   ├── coordinator.py   # Orchestration
│   ├── planner.py       # Planification
│   ├── researchers.py   # Chercheurs
│   ├── analyzer.py      # Analyse
│   └── reporter.py      # Rapports
├── api/
│   └── routes/          # Endpoints REST
│       ├── health.py
│       └── research.py
├── core/                # Configuration
│   ├── config.py
│   └── database.py
├── models/              # Modèles de données
│   └── research.py
└── main.py              # Point d'entrée
```

### 3. Framework Agentic

Le cœur du système utilise une architecture multi-agents :

#### Agent Coordinator
**Rôle** : Orchestre les autres agents
**Input** : Requête utilisateur
**Output** : Résultats complets

```python
class ResearchCoordinator:
    async def run_research(topic, sources, max_results):
        # 1. Planifier
        plan = await planner.create_plan(topic, sources)
        
        # 2. Rechercher (parallèle)
        results = await asyncio.gather(*[
            researcher.search(plan.query, max_results)
            for researcher in researchers
        ])
        
        # 3. Analyser
        analysis = await analyzer.analyze(results)
        
        # 4. Rapporter
        report = await reporter.generate(analysis)
        
        return report
```

#### Agent Planner
**Rôle** : Crée la stratégie de recherche
- Raffine la requête
- Sélectionne les sources
- Extrait les mots-clés
- Détermine la stratégie (recent_focus, comprehensive, balanced)

#### Agent Researchers
**Rôle** : Recherchent sur les sources externes
- Un researcher par source
- Exécution parallèle (asyncio)
- Gestion des erreurs individuelles
- Normalisation des résultats

**Researchers disponibles** :
- `ArxivResearcher` : arXiv.org
- `SemanticScholarResearcher` : Semantic Scholar
- `GoogleScholarResearcher` : Google Scholar (via SerpAPI)
- `WikipediaResearcher` : Wikipedia
- `NewsResearcher` : NewsAPI
- `WebSearchResearcher` : Serper API

#### Agent Analyzer
**Rôle** : Analyse les résultats bruts
- Statistiques globales
- Identification des tendances
- Extraction des insights
- Scoring des articles

#### Agent Reporter
**Rôle** : Génère le rapport final
- Résumé exécutif
- Top articles
- Recommandations
- Formatage pour UI

### 4. MCP Servers (TypeScript)

**Model Context Protocol** : Standard pour interfacer avec des sources de données.

Chaque serveur MCP :
- Expose des "tools" (fonctions)
- Communique via stdio
- Retourne des résultats structurés

**Exemple** :
```typescript
class ArxivServer {
  tools = [
    {
      name: "search_arxiv",
      inputSchema: { query: string, maxResults: number },
      handler: async (args) => { /* ... */ }
    }
  ]
}
```

### 5. Base de Données

**SQLite** (par défaut, PostgreSQL supporté)

**Modèle** :
```sql
CREATE TABLE researches (
  id INTEGER PRIMARY KEY,
  topic VARCHAR(500) NOT NULL,
  status VARCHAR(20),
  results JSON,
  error TEXT,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  completed_at TIMESTAMP
);
```

## Flux de Données

### 1. Création d'une Recherche

```
┌──────────┐     POST /research/     ┌──────────┐
│ Frontend │ ──────────────────────> │ Backend  │
└──────────┘                         └────┬─────┘
                                          │
                                          │ 1. Crée DB record
                                          │ 2. Lance background task
                                          │ 3. Retourne 201 Created
                                          │
                                          ▼
                                    ┌──────────────┐
                                    │ Coordinator  │
                                    │   Agent      │
                                    └──────┬───────┘
                                          │
                    ┌─────────────────────┼─────────────────────┐
                    │                     │                     │
                    ▼                     ▼                     ▼
              ┌──────────┐          ┌──────────┐          ┌──────────┐
              │ arXiv    │          │ Scholar  │          │ Wiki     │
              │ MCP      │          │ MCP      │          │ MCP      │
              └────┬─────┘          └────┬─────┘          └────┬─────┘
                   │                     │                     │
                   └─────────────────────┴─────────────────────┘
                                          │
                                          ▼
                                    ┌──────────────┐
                                    │   Analyzer   │
                                    │    Agent     │
                                    └──────┬───────┘
                                          │
                                          ▼
                                    ┌──────────────┐
                                    │   Reporter   │
                                    │    Agent     │
                                    └──────┬───────┘
                                          │
                                          │ Update DB
                                          ▼
                                    [COMPLETED]
```

### 2. Récupération des Résultats

```
┌──────────┐     GET /research/1     ┌──────────┐
│ Frontend │ <────────────────────── │ Backend  │
└────┬─────┘                         └────┬─────┘
     │                                     │
     │ Polling every 2s                    │ Query DB
     │ if pending/in_progress              │
     │                                     │
     └─────────────────────────────────────┘
```

## Patterns et Principes

### 1. Separation of Concerns

- **Frontend** : Uniquement UI/UX
- **Backend** : Logique métier
- **MCP Servers** : Intégration API externes
- **Agents** : Intelligence et orchestration

### 2. Async/Await

Tout est asynchrone pour maximiser les performances :

```python
# Recherches parallèles
results = await asyncio.gather(
    arxiv_search(),
    scholar_search(),
    wiki_search()
)
```

### 3. Error Handling

Chaque couche gère ses erreurs :

```python
try:
    results = await researcher.search(query)
except Exception as e:
    logger.error(f"Research failed: {e}")
    results = []  # Continue avec résultats vides
```

### 4. Type Safety

- Python : Type hints + Pydantic
- TypeScript : Interfaces strictes
- API : Validation automatique

### 5. Extensibilité

Ajouter une source :
1. Créer MCP server
2. Créer Researcher agent
3. Enregistrer dans coordinator

## Performance

### Optimisations

1. **Recherches parallèles** : asyncio.gather()
2. **Background tasks** : FastAPI BackgroundTasks
3. **Streaming possible** : WebSocket (futur)
4. **Cache** : À implémenter (Redis)

### Métriques Typiques

- Temps de recherche : 10-30 secondes
- Sources simultanées : 5-6
- Throughput : ~10 recherches/minute
- Latence API : <100ms (hors recherche)

## Sécurité

### Actuel

- Validation des inputs (Pydantic)
- CORS configuré
- Rate limiting des APIs externes

### À Implémenter

- Authentification JWT
- Rate limiting global
- HTTPS en production
- Secrets management (Vault)

## Déploiement

### Development

```bash
./scripts/start-dev.sh
```

### Production

**Backend** :
```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

**Frontend** :
```bash
npm run build
# Servir dist/ avec nginx
```

**Docker** :
```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    ports: ['8000:8000']
  frontend:
    build: ./frontend
    ports: ['3000:3000']
  postgres:
    image: postgres:15
```

## Monitoring

### Logs

- Backend : Logs structurés (JSON)
- MCP Servers : stderr
- Frontend : Console + Sentry

### Métriques

À implémenter :
- Prometheus
- Grafana
- AlertManager

## Tests

### Backend

```bash
pytest tests/
pytest --cov
```

### Frontend

```bash
npm test
npm run test:e2e  # Playwright
```

### MCP Servers

```bash
npm test
```

## Documentation

- **README.md** : Vue d'ensemble
- **QUICKSTART.md** : Démarrage rapide
- **docs/INSTALLATION.md** : Installation détaillée
- **docs/USAGE.md** : Guide utilisateur
- **docs/API.md** : Documentation API
- **docs/MCP.md** : Serveurs MCP
- **ARCHITECTURE.md** : Ce document
- **CONTRIBUTING.md** : Guide contributeur

## Évolutions Futures

### Court Terme (v1.1)
- WebSocket pour updates temps réel
- Cache Redis
- Authentification

### Moyen Terme (v1.2)
- Plus de sources (PubMed, IEEE, ACM)
- Alertes et veille automatique
- Export PDF des rapports

### Long Terme (v2.0)
- IA pour synthèse avancée (LLM)
- Graphes de citations
- Recommandations personnalisées
- API publique avec quotas

## Ressources

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [React Docs](https://react.dev/)
- [MCP Spec](https://spec.modelcontextprotocol.io/)
- [arXiv API](https://info.arxiv.org/help/api/)

