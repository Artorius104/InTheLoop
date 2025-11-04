# InTheLoop - Veille Scientifique Intelligente

Un système de veille scientifique automatisée utilisant un framework agentic et des serveurs MCP (Model Context Protocol) pour rechercher, analyser et synthétiser l'information scientifique et technique.

## 🎯 Fonctionnalités

- **Recherche Multi-Sources** : Agrège les données de arXiv, Google Scholar, Semantic Scholar, Wikipédia
- **Framework Agentic** : Orchestration intelligente des recherches et analyses
- **Veille Temps Réel** : Suivi des nouveautés et activités des entreprises
- **Interface Web Moderne** : Interface intuitive pour soumettre et visualiser les recherches
- **Web Scraping** : Extraction de contenu depuis diverses sources

## 🏗️ Architecture

```
InTheLoop/
├── backend/           # API FastAPI + Framework Agentic
│   ├── agents/        # Agents spécialisés
│   ├── api/           # Routes API
│   └── services/      # Services métier
├── frontend/          # Interface web React
├── mcp-servers/       # Serveurs MCP personnalisés
└── config/            # Configuration
```

## 🚀 Installation

### Prérequis

- Python 3.11+
- Node.js 18+
- pip et npm

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

### Frontend

```bash
cd frontend
npm install
```

### Configuration MCP

Les serveurs MCP sont configurés dans `config/mcp-config.json`. Ajoutez vos clés API dans un fichier `.env` :

```bash
cp .env.example .env
# Éditez .env avec vos clés API
```

## 🎮 Utilisation

### Lancer le backend

```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --port 8000
```

### Lancer le frontend

```bash
cd frontend
npm run dev
```

L'application sera accessible sur http://localhost:3000

## 🤖 Serveurs MCP Disponibles

- **arxiv-server** : Recherche de publications scientifiques sur arXiv
- **web-search-server** : Recherche web générale (Google, Bing)
- **wikipedia-server** : Accès à Wikipédia
- **google-scholar-server** : Recherche académique via Google Scholar
- **semantic-scholar-server** : API Semantic Scholar pour articles scientifiques
- **webscraping-server** : Extraction de contenu web
- **news-server** : Veille presse scientifique et technique

## 📊 Workflow Agentic

1. **Agent Coordinator** : Reçoit la requête utilisateur
2. **Agent Planner** : Planifie la stratégie de recherche
3. **Agent Researchers** : Recherchent en parallèle sur différentes sources
4. **Agent Analyzer** : Analyse et synthétise les résultats
5. **Agent Reporter** : Génère le rapport final

## 🔧 Technologies

- **Backend** : FastAPI, LangChain, Pydantic
- **Frontend** : React, TailwindCSS, shadcn/ui
- **MCP** : Model Context Protocol servers
- **AI** : OpenAI/Anthropic API

## 📝 License

Voir le fichier LICENSE

## 👥 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou une pull request.

