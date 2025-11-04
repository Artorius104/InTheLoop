# MCP Servers - InTheLoop

Serveurs MCP (Model Context Protocol) pour la veille scientifique.

## Serveurs Disponibles

1. **arxiv-server** - Recherche sur arXiv
2. **semantic-scholar-server** - API Semantic Scholar
3. **google-scholar-server** - Recherche Google Scholar
4. **wikipedia-server** - Accès à Wikipedia
5. **news-server** - Veille presse scientifique
6. **webscraping-server** - Extraction de contenu web
7. **web-search-server** - Recherche web générale

## Installation

Chaque serveur peut être installé et démarré individuellement :

```bash
cd mcp-servers/arxiv-server
npm install
npm start
```

## Configuration

Les serveurs utilisent les variables d'environnement définies dans `.env` à la racine du projet.

## Utilisation avec MCP

Les serveurs sont automatiquement découverts et utilisés par le framework agentic du backend.

