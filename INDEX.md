# Index - InTheLoop

Guide complet de navigation dans le projet.

## 🎯 Démarrage Rapide

| Priorité | Fichier | Description |
|----------|---------|-------------|
| ⭐⭐⭐ | **[START_HERE.md](START_HERE.md)** | **COMMENCEZ ICI** - Vue d'ensemble rapide |
| ⭐⭐⭐ | **[QUICKSTART.md](QUICKSTART.md)** | Démarrage en 5 minutes |
| ⭐⭐ | **[SETUP_COMPLETE.md](SETUP_COMPLETE.md)** | Résumé de ce qui a été créé |
| ⭐⭐ | **[CHECKLIST.md](CHECKLIST.md)** | Vérifier l'installation |

## 📚 Documentation Principale

### Vue d'Ensemble
- **[README.md](README.md)** - Introduction et présentation
- **[SUMMARY.md](SUMMARY.md)** - Résumé complet du projet
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Architecture technique détaillée

### Guides Utilisateur
- **[docs/INSTALLATION.md](docs/INSTALLATION.md)** - Installation complète pas à pas
- **[docs/USAGE.md](docs/USAGE.md)** - Guide d'utilisation avec exemples
- **[docs/API.md](docs/API.md)** - Documentation API REST complète
- **[docs/MCP.md](docs/MCP.md)** - Documentation serveurs MCP

### Pour Développeurs
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Comment contribuer au projet
- **[PROJECT_STRUCTURE.txt](PROJECT_STRUCTURE.txt)** - Arborescence complète

## 🏗️ Structure du Code

### Backend (Python/FastAPI)

```
backend/
├── main.py                    # Point d'entrée API
├── requirements.txt           # Dépendances Python
├── agents/                    # Framework agentic
│   ├── coordinator.py         # ⭐ Orchestrateur principal
│   ├── planner.py            # Planification de recherche
│   ├── researchers.py        # ⭐ Chercheurs par source
│   ├── analyzer.py           # Analyse des résultats
│   └── reporter.py           # Génération de rapports
├── api/routes/               # Endpoints REST
│   ├── health.py             # Health checks
│   └── research.py           # ⭐ Routes principales
├── core/                     # Configuration
│   ├── config.py             # Variables de config
│   └── database.py           # Setup base de données
└── models/                   # Modèles de données
    └── research.py           # Modèles de recherche
```

**Fichiers clés** :
- `agents/coordinator.py` - Logique principale du framework agentic
- `agents/researchers.py` - Implémentation de chaque source
- `api/routes/research.py` - Endpoints API

### Frontend (React/TypeScript)

```
frontend/
├── package.json              # Dépendances Node
├── vite.config.ts           # Configuration Vite
├── tailwind.config.js       # Configuration TailwindCSS
├── src/
│   ├── main.tsx             # Point d'entrée React
│   ├── App.tsx              # Composant racine
│   ├── components/          # Composants réutilisables
│   │   └── Layout.tsx       # Layout principal
│   ├── pages/               # Pages de l'application
│   │   ├── HomePage.tsx     # ⭐ Page d'accueil
│   │   ├── ResearchPage.tsx # ⭐ Affichage résultats
│   │   └── HistoryPage.tsx  # Historique recherches
│   └── services/            # Services
│       └── api.ts           # ⭐ Client API
```

**Fichiers clés** :
- `pages/HomePage.tsx` - Interface de saisie
- `pages/ResearchPage.tsx` - Affichage des résultats
- `services/api.ts` - Communication avec backend

### MCP Servers (TypeScript)

```
mcp-servers/
├── arxiv-server/            # ⭐ Recherche arXiv
├── semantic-scholar-server/ # Semantic Scholar
├── google-scholar-server/   # Google Scholar
├── wikipedia-server/        # ⭐ Wikipedia
├── web-search-server/       # Recherche web
├── webscraping-server/      # Web scraping
└── news-server/             # Actualités
```

Chaque serveur contient :
- `package.json` - Dépendances
- `tsconfig.json` - Config TypeScript
- `src/index.ts` - ⭐ Implémentation principale

### Scripts Utilitaires

```
scripts/
├── setup.sh              # ⭐ Installation automatique
├── start-dev.sh          # ⭐ Démarrage développement
└── build-mcp-servers.sh  # Compilation MCP servers
```

### Configuration

```
config/
└── mcp-config.json       # Configuration serveurs MCP
```

## 📖 Documentation par Cas d'Usage

### Je veux commencer rapidement
1. Lire [START_HERE.md](START_HERE.md)
2. Exécuter `./scripts/setup.sh`
3. Exécuter `./scripts/start-dev.sh`

### Je veux comprendre le projet
1. Lire [README.md](README.md)
2. Lire [SUMMARY.md](SUMMARY.md)
3. Lire [ARCHITECTURE.md](ARCHITECTURE.md)

### Je veux installer le projet
1. Lire [QUICKSTART.md](QUICKSTART.md)
2. Suivre [docs/INSTALLATION.md](docs/INSTALLATION.md)
3. Vérifier avec [CHECKLIST.md](CHECKLIST.md)

### Je veux utiliser le projet
1. Lire [docs/USAGE.md](docs/USAGE.md)
2. Tester les exemples
3. Consulter [docs/API.md](docs/API.md) pour l'API

### Je veux développer/contribuer
1. Lire [ARCHITECTURE.md](ARCHITECTURE.md)
2. Lire [CONTRIBUTING.md](CONTRIBUTING.md)
3. Consulter [docs/MCP.md](docs/MCP.md) pour MCP

### Je rencontre un problème
1. Consulter [CHECKLIST.md](CHECKLIST.md)
2. Voir section dépannage dans [QUICKSTART.md](QUICKSTART.md)
3. Lire [docs/INSTALLATION.md](docs/INSTALLATION.md)

## 🔍 Trouver de l'Information

### Par Sujet

**Installation**
- [QUICKSTART.md](QUICKSTART.md) - Rapide
- [docs/INSTALLATION.md](docs/INSTALLATION.md) - Détaillé
- [CHECKLIST.md](CHECKLIST.md) - Vérification

**Utilisation**
- [START_HERE.md](START_HERE.md) - Premiers pas
- [docs/USAGE.md](docs/USAGE.md) - Guide complet
- [SETUP_COMPLETE.md](SETUP_COMPLETE.md) - Vue d'ensemble

**API**
- [docs/API.md](docs/API.md) - Documentation REST
- [docs/MCP.md](docs/MCP.md) - Serveurs MCP

**Architecture & Code**
- [ARCHITECTURE.md](ARCHITECTURE.md) - Architecture technique
- [CONTRIBUTING.md](CONTRIBUTING.md) - Guide développeur
- [PROJECT_STRUCTURE.txt](PROJECT_STRUCTURE.txt) - Arborescence

**Référence Rapide**
- [SUMMARY.md](SUMMARY.md) - Résumé projet
- [INDEX.md](INDEX.md) - Ce fichier

### Par Type de Fichier

**Markdown (.md)** - Documentation
- 11 fichiers à la racine
- 4 fichiers dans `docs/`

**Python (.py)** - Backend
- 16 fichiers dans `backend/`
- Framework agentic + API

**TypeScript (.ts/.tsx)** - Frontend & MCP
- 16 fichiers dans `frontend/src/`
- 7 serveurs dans `mcp-servers/`

**Configuration (.json, .js)**
- `package.json` - Dépendances Node
- `tsconfig.json` - Config TypeScript
- `vite.config.ts` - Config Vite
- `tailwind.config.js` - Config TailwindCSS
- `mcp-config.json` - Config MCP

**Scripts (.sh)** - Automatisation
- `setup.sh` - Installation
- `start-dev.sh` - Démarrage
- `build-mcp-servers.sh` - Compilation

## 📊 Métriques du Projet

```
Total fichiers:    74
Fichiers Python:   16
Fichiers TS/TSX:   16
Serveurs MCP:      7
Pages frontend:    3
Agents backend:    5
Documentation:     15+
Scripts:           3
```

## 🎓 Parcours d'Apprentissage Recommandé

### Niveau 1 : Débutant (1-2 heures)
1. ✅ Lire [START_HERE.md](START_HERE.md)
2. ✅ Installer avec [QUICKSTART.md](QUICKSTART.md)
3. ✅ Faire première recherche
4. ✅ Consulter [docs/USAGE.md](docs/USAGE.md)

### Niveau 2 : Utilisateur (2-4 heures)
1. ✅ Comprendre [ARCHITECTURE.md](ARCHITECTURE.md)
2. ✅ Tester toutes les sources
3. ✅ Utiliser l'API REST [docs/API.md](docs/API.md)
4. ✅ Automatiser avec scripts

### Niveau 3 : Développeur (4-8 heures)
1. ✅ Lire code backend (`agents/`)
2. ✅ Lire code frontend (`pages/`)
3. ✅ Comprendre MCP [docs/MCP.md](docs/MCP.md)
4. ✅ Contribuer [CONTRIBUTING.md](CONTRIBUTING.md)

## 🔗 Liens Rapides

### Démarrage
- [START_HERE.md](START_HERE.md) - Commencer ici
- [QUICKSTART.md](QUICKSTART.md) - Installation rapide
- [CHECKLIST.md](CHECKLIST.md) - Vérification

### Documentation
- [README.md](README.md) - Introduction
- [SUMMARY.md](SUMMARY.md) - Résumé
- [docs/](docs/) - Documentation détaillée

### Code
- [backend/](backend/) - Backend Python
- [frontend/](frontend/) - Frontend React
- [mcp-servers/](mcp-servers/) - Serveurs MCP

### Outils
- [scripts/](scripts/) - Scripts utilitaires
- [config/](config/) - Configuration

## ❓ FAQ Rapide

**Q: Par où commencer ?**
A: Lire [START_HERE.md](START_HERE.md) puis exécuter `./scripts/setup.sh`

**Q: Ai-je besoin de clés API ?**
A: Non ! Le système fonctionne avec arXiv et Wikipedia sans clés

**Q: Comment contribuer ?**
A: Lire [CONTRIBUTING.md](CONTRIBUTING.md)

**Q: Où est l'API REST ?**
A: Documentation dans [docs/API.md](docs/API.md), URL: http://localhost:8000/docs

**Q: Comment ajouter une source ?**
A: Suivre le guide dans [docs/MCP.md](docs/MCP.md)

## 📞 Support

- 📖 Documentation complète dans ce fichier
- ✅ Checklist : [CHECKLIST.md](CHECKLIST.md)
- 🐛 Issues : Créer une issue GitHub
- 💬 Questions : Discussions GitHub

---

**Navigation** : Tous les chemins sont relatifs à la racine du projet

**Mise à jour** : Novembre 2025

**Version** : 1.0.0

