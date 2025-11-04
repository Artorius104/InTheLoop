# AI Research Paper Monitoring System

Un système de veille automatisé utilisant l'IA pour surveiller et analyser les papiers de recherche via MCP Arxiv.

## Structure du projet

- `src/` - Code source principal
- `agents/` - Agents IA spécialisés
- `config/` - Configuration et paramètres
- `data/` - Stockage des données et cache
- `tests/` - Tests unitaires et d'intégration
- `docs/` - Documentation

## Installation

```bash
pip install -r requirements.txt
```

## Configuration MCP

Le projet utilise le serveur MCP ArXiv de [blazickjp/arxiv-mcp-server](https://github.com/blazickjp/arxiv-mcp-server) pour accéder aux papiers de recherche.

### Prérequis
```bash
# Installation d'uv (gestionnaire de paquets Python)
pip install uv
```

### Configuration
Le serveur MCP est configuré dans `.kiro/settings/mcp.json` et sera automatiquement téléchargé lors de la première utilisation.

## Usage

```bash
python src/main.py
```
## 
Documentation MCP

Consultez `docs/MCP_ARXIV.md` pour la documentation complète du serveur MCP ArXiv, incluant :
- Configuration détaillée
- Outils disponibles (`search_arxiv`, `get_paper_details`, `get_paper_pdf`)
- Exemples d'utilisation
- Structure des données
- Dépannage