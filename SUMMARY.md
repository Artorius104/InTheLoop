# InTheLoop - Résumé du Projet

## 🎯 Objectif

InTheLoop est une plateforme de **veille scientifique intelligente** qui utilise un **framework agentic** pour automatiser la recherche, l'analyse et la synthèse d'informations scientifiques provenant de multiples sources.

## ✨ Fonctionnalités Principales

### 1. Recherche Multi-Sources
- **arXiv** : Preprints scientifiques (physique, CS, maths)
- **Semantic Scholar** : Articles académiques avec citations
- **Google Scholar** : Recherche académique complète
- **Wikipedia** : Contexte encyclopédique
- **NewsAPI** : Actualités scientifiques et techniques
- **Web Search** : Recherche web générale

### 2. Framework Agentic Intelligent

Le système utilise 5 agents spécialisés qui travaillent en collaboration :

```
Planner → Researchers (parallèle) → Analyzer → Reporter
   ↓           ↓                       ↓           ↓
Stratégie  Collecte données      Analyse     Rapport final
```

### 3. Interface Moderne
- Design responsive et intuitive
- Suivi en temps réel des recherches
- Visualisation des résultats
- Historique des recherches

### 4. Serveurs MCP
7 serveurs MCP (Model Context Protocol) pour interfacer avec les APIs externes de manière standardisée.

## 🏗️ Architecture Technique

### Stack Technologique

**Backend**
- Python 3.11+
- FastAPI (API REST)
- SQLAlchemy (ORM)
- Asyncio (parallélisme)
- Pydantic (validation)

**Frontend**
- React 18 + TypeScript
- Vite (build tool)
- TailwindCSS (styling)
- React Router
- TanStack Query

**MCP Servers**
- TypeScript
- Node.js 18+
- Model Context Protocol SDK

### Base de Données
- SQLite (développement)
- PostgreSQL (production supportée)

## 📊 Workflow Type

1. **Utilisateur** saisit un sujet scientifique
2. **Planner Agent** crée une stratégie de recherche optimale
3. **Researcher Agents** interrogent 5-6 sources en parallèle (~10-30s)
4. **Analyzer Agent** synthétise et analyse les résultats
5. **Reporter Agent** génère un rapport structuré avec :
   - Résumé exécutif
   - Top 10 articles les plus pertinents
   - Découvertes clés
   - Tendances identifiées
   - Recommandations

## 📦 Contenu du Projet

### Structure des Dossiers

```
InTheLoop/
├── backend/              # API Python FastAPI
│   ├── agents/           # Framework agentic (5 agents)
│   ├── api/routes/       # Endpoints REST
│   ├── core/             # Configuration
│   └── models/           # Modèles de données
│
├── frontend/             # Interface React
│   └── src/
│       ├── components/   # Composants UI
│       ├── pages/        # Pages (Home, Research, History)
│       └── services/     # API client
│
├── mcp-servers/          # 7 serveurs MCP
│   ├── arxiv-server/
│   ├── semantic-scholar-server/
│   ├── google-scholar-server/
│   ├── wikipedia-server/
│   ├── web-search-server/
│   ├── webscraping-server/
│   └── news-server/
│
├── docs/                 # Documentation complète
│   ├── INSTALLATION.md
│   ├── USAGE.md
│   ├── API.md
│   └── MCP.md
│
├── scripts/              # Scripts utilitaires
│   ├── setup.sh          # Installation automatique
│   ├── start-dev.sh      # Démarrage dev
│   └── build-mcp-servers.sh
│
└── config/               # Configuration MCP
```

### Fichiers Clés

**Documentation**
- `README.md` - Vue d'ensemble et introduction
- `QUICKSTART.md` - Démarrage en 5 minutes
- `ARCHITECTURE.md` - Architecture détaillée
- `CONTRIBUTING.md` - Guide contributeur

**Configuration**
- `.env.example` - Variables d'environnement
- `config/mcp-config.json` - Configuration MCP

**Backend**
- `backend/main.py` - Point d'entrée API
- `backend/agents/coordinator.py` - Orchestrateur principal
- `backend/api/routes/research.py` - Endpoints recherche

**Frontend**
- `frontend/src/App.tsx` - Application React
- `frontend/src/pages/HomePage.tsx` - Page principale
- `frontend/src/services/api.ts` - Client API

## 🚀 Démarrage Rapide

### Installation Automatique

```bash
./scripts/setup.sh
```

### Démarrage

```bash
./scripts/start-dev.sh
```

### URLs
- Frontend : http://localhost:3000
- API : http://localhost:8000
- Docs API : http://localhost:8000/docs

## 📝 API REST

### Endpoints Principaux

**POST /api/research/** - Créer une recherche
```json
{
  "topic": "Large Language Models",
  "sources": ["arxiv", "semantic_scholar"],
  "max_results_per_source": 10
}
```

**GET /api/research/{id}** - Récupérer une recherche

**GET /api/research/** - Liste des recherches

Voir [docs/API.md](docs/API.md) pour la documentation complète.

## 🔑 Clés API

### Requis
Aucune ! Le système fonctionne avec arXiv et Wikipedia sans clés.

### Optionnelles mais Recommandées
- **Semantic Scholar** : Gratuit, 1000 req/5min avec clé
- **Serper** : Gratuit 2500 recherches, puis $5/1000
- **NewsAPI** : Gratuit 100 req/jour
- **SerpAPI** : Pour Google Scholar

## 📊 Statistiques du Projet

**Code**
- ~50 fichiers sources
- Backend : ~1500 lignes Python
- Frontend : ~800 lignes TypeScript/React
- MCP Servers : ~1200 lignes TypeScript
- Documentation : ~3000 lignes

**Composants**
- 5 agents intelligents
- 7 serveurs MCP
- 3 pages frontend
- 10+ composants React
- 5 endpoints API

**Tests**
- Tests unitaires backend
- Tests d'intégration
- Linting automatique

## 🎓 Cas d'Usage

### 1. Veille Technologique
Restez à jour sur les dernières avancées en IA, quantum computing, etc.

### 2. Recherche Académique
Trouvez rapidement les articles les plus pertinents sur un sujet.

### 3. État de l'Art
Obtenez une vue d'ensemble complète d'un domaine scientifique.

### 4. Analyse Concurrentielle
Surveillez les publications d'entreprises et laboratoires.

## 🔮 Évolutions Futures

### v1.1
- WebSocket pour mises à jour temps réel
- Cache Redis pour performances
- Authentification JWT

### v1.2
- Plus de sources (PubMed, IEEE, ACM)
- Export PDF des rapports
- Alertes automatiques

### v2.0
- Synthèse avancée avec LLMs
- Graphes de citations interactifs
- Recommandations personnalisées
- API publique

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [README.md](README.md) | Introduction générale |
| [QUICKSTART.md](QUICKSTART.md) | Démarrage en 5 minutes |
| [INSTALLATION.md](docs/INSTALLATION.md) | Guide d'installation détaillé |
| [USAGE.md](docs/USAGE.md) | Guide d'utilisation complet |
| [API.md](docs/API.md) | Documentation API REST |
| [MCP.md](docs/MCP.md) | Documentation serveurs MCP |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Architecture technique |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Guide contributeur |

## 🛠️ Technologies et Bibliothèques

### Backend
- `fastapi` - Framework web
- `uvicorn` - Serveur ASGI
- `sqlalchemy` - ORM
- `pydantic` - Validation
- `arxiv` - Client arXiv
- `httpx` - Client HTTP async

### Frontend
- `react` - UI framework
- `react-router-dom` - Routing
- `@tanstack/react-query` - Data fetching
- `axios` - HTTP client
- `lucide-react` - Icônes
- `tailwindcss` - CSS utility-first
- `date-fns` - Manipulation dates

### MCP Servers
- `@modelcontextprotocol/sdk` - SDK MCP
- `arxiv-api` - Client arXiv
- `cheerio` - Web scraping
- `node-fetch` - HTTP client

## 🤝 Contribution

Les contributions sont les bienvenues ! Voir [CONTRIBUTING.md](CONTRIBUTING.md).

## 📄 Licence

Voir le fichier [LICENSE](LICENSE).

## 👥 Auteurs

Projet développé pour ESGI - IA - Gestion de Projet.

## 🔗 Ressources

- [FastAPI](https://fastapi.tiangolo.com/)
- [React](https://react.dev/)
- [MCP Protocol](https://spec.modelcontextprotocol.io/)
- [arXiv API](https://info.arxiv.org/help/api/)
- [Semantic Scholar API](https://api.semanticscholar.org/)

---

**Status** : ✅ Projet Complet et Fonctionnel

**Version** : 1.0.0

**Date** : Novembre 2025

