# Documentation MCP - Model Context Protocol

## Qu'est-ce que MCP ?

MCP (Model Context Protocol) est un protocole permettant aux applications d'interagir avec des sources de données externes via des serveurs standardisés. Dans InTheLoop, les serveurs MCP permettent de récupérer des informations scientifiques de diverses sources.

## Architecture

```
┌─────────────────┐
│  Backend Agent  │
│   (Python)      │
└────────┬────────┘
         │
         │ Appelle
         │
┌────────▼────────┐
│  MCP Servers    │
│  (TypeScript)   │
├─────────────────┤
│ • arxiv         │
│ • semantic      │
│ • wikipedia     │
│ • news          │
│ • webscraping   │
└────────┬────────┘
         │
         │ API Calls
         │
┌────────▼────────┐
│ External APIs   │
│ • arXiv API     │
│ • Semantic      │
│ • NewsAPI       │
│ • etc...        │
└─────────────────┘
```

## Serveurs Disponibles

### 1. arXiv Server

**Description** : Recherche d'articles scientifiques sur arXiv.org

**Tools disponibles** :
- `search_arxiv` : Recherche par mots-clés
- `get_arxiv_paper` : Récupère un article par ID

**Exemple** :
```typescript
{
  "name": "search_arxiv",
  "arguments": {
    "query": "neural networks",
    "maxResults": 10,
    "sortBy": "relevance"
  }
}
```

**Configuration** :
- Aucune clé API requise
- Rate limit : ~3 req/sec

### 2. Semantic Scholar Server

**Description** : Accès à l'API Semantic Scholar pour articles académiques

**Tools disponibles** :
- `search_papers` : Recherche d'articles
- `get_paper` : Détails d'un article
- `get_paper_citations` : Citations d'un article

**Exemple** :
```typescript
{
  "name": "search_papers",
  "arguments": {
    "query": "machine learning",
    "limit": 10
  }
}
```

**Configuration** :
- Clé API recommandée : `SEMANTIC_SCHOLAR_API_KEY`
- Sans clé : 100 req/5min
- Avec clé : 1000 req/5min

### 3. Wikipedia Server

**Description** : Recherche et récupération d'articles Wikipedia

**Tools disponibles** :
- `search_wikipedia` : Recherche d'articles
- `get_article` : Contenu complet
- `get_summary` : Résumé d'un article

**Exemple** :
```typescript
{
  "name": "search_wikipedia",
  "arguments": {
    "query": "artificial intelligence",
    "limit": 5
  }
}
```

**Configuration** :
- Aucune clé API requise
- Rate limit : Respecter les guidelines Wikipedia

### 4. Google Scholar Server

**Description** : Recherche académique via SerpAPI

**Tools disponibles** :
- `search_scholar` : Recherche d'articles
- `get_citations` : Citations d'un article

**Exemple** :
```typescript
{
  "name": "search_scholar",
  "arguments": {
    "query": "quantum computing",
    "num": 10,
    "year_low": 2020
  }
}
```

**Configuration** :
- **Requis** : `SERPAPI_KEY`
- Prix : Varie selon plan SerpAPI
- Alternative gratuite : scholarly (limité)

### 5. Web Search Server

**Description** : Recherche web via Serper API

**Tools disponibles** :
- `search_web` : Recherche générale
- `search_news` : Recherche d'actualités

**Exemple** :
```typescript
{
  "name": "search_web",
  "arguments": {
    "query": "OpenAI latest developments",
    "num": 10
  }
}
```

**Configuration** :
- **Requis** : `SERPER_API_KEY`
- Gratuit : 2500 recherches
- Puis : $5/1000 recherches

### 6. News Server

**Description** : Actualités via NewsAPI

**Tools disponibles** :
- `search_news` : Recherche d'articles
- `get_top_headlines` : Derniers titres
- `search_tech_news` : Actualités tech/science

**Exemple** :
```typescript
{
  "name": "search_tech_news",
  "arguments": {
    "query": "artificial intelligence",
    "pageSize": 10
  }
}
```

**Configuration** :
- **Requis** : `NEWS_API_KEY`
- Gratuit : 100 req/jour
- Pro : À partir de $449/mois

### 7. Web Scraping Server

**Description** : Extraction de contenu web

**Tools disponibles** :
- `scrape_url` : Extraire contenu HTML
- `extract_text` : Texte brut
- `extract_links` : Tous les liens
- `get_metadata` : Métadonnées de page

**Exemple** :
```typescript
{
  "name": "scrape_url",
  "arguments": {
    "url": "https://example.com/article",
    "selector": ".article-content"
  }
}
```

**Configuration** :
- Aucune clé API requise
- Respecter robots.txt
- Rate limiting conseillé

## Développement

### Créer un Nouveau Serveur MCP

1. **Structure du projet** :
```
mcp-servers/my-server/
├── package.json
├── tsconfig.json
└── src/
    └── index.ts
```

2. **package.json** :
```json
{
  "name": "@intheloop/my-server",
  "version": "1.0.0",
  "type": "module",
  "main": "dist/index.js",
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js",
    "dev": "tsx watch src/index.ts"
  },
  "dependencies": {
    "@modelcontextprotocol/sdk": "^0.5.0"
  }
}
```

3. **src/index.ts** :
```typescript
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';

class MyServer {
  private server: Server;

  constructor() {
    this.server = new Server(
      { name: 'my-server', version: '1.0.0' },
      { capabilities: { tools: {} } }
    );
    this.setupHandlers();
  }

  private setupHandlers(): void {
    this.server.setRequestHandler(ListToolsRequestSchema, async () => ({
      tools: [
        {
          name: 'my_tool',
          description: 'Description of my tool',
          inputSchema: {
            type: 'object',
            properties: {
              param: { type: 'string' }
            },
            required: ['param']
          }
        }
      ]
    }));

    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      // Implement tool logic
      return {
        content: [{ type: 'text', text: 'Result' }]
      };
    });
  }

  async run(): Promise<void> {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
  }
}

new MyServer().run();
```

4. **Compiler et tester** :
```bash
npm install
npm run build
npm run dev
```

### Intégration Backend

Dans `backend/agents/researchers.py` :

```python
class MyResearcher(BaseResearcher):
    def __init__(self):
        super().__init__("my_server")
    
    async def search(self, query: str, max_results: int = 10):
        # Appeler le serveur MCP
        # Implémenter la logique
        pass
```

## Bonnes Pratiques

### 1. Gestion des Erreurs

```typescript
try {
  const result = await fetchData();
  return { content: [{ type: 'text', text: JSON.stringify(result) }] };
} catch (error) {
  return {
    content: [{
      type: 'text',
      text: `Error: ${error.message}`
    }]
  };
}
```

### 2. Rate Limiting

```typescript
class RateLimiter {
  private lastCall = 0;
  private minInterval = 1000; // 1 sec

  async throttle() {
    const now = Date.now();
    const elapsed = now - this.lastCall;
    if (elapsed < this.minInterval) {
      await new Promise(r => setTimeout(r, this.minInterval - elapsed));
    }
    this.lastCall = Date.now();
  }
}
```

### 3. Cache

```typescript
class Cache {
  private cache = new Map<string, any>();
  private ttl = 3600000; // 1 hour

  get(key: string): any | null {
    const item = this.cache.get(key);
    if (item && Date.now() < item.expires) {
      return item.value;
    }
    return null;
  }

  set(key: string, value: any): void {
    this.cache.set(key, {
      value,
      expires: Date.now() + this.ttl
    });
  }
}
```

### 4. Logging

```typescript
console.error('[MCP Server] Info message');  // Logs
console.log('Data');  // Stdout (éviter)
```

## Tests

### Test Manuel

```bash
cd mcp-servers/my-server
npm run dev
```

Puis dans un autre terminal :
```bash
echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | node dist/index.js
```

### Test d'Intégration

```python
# backend/tests/test_mcp.py
import pytest
from agents.researchers import MyResearcher

@pytest.mark.asyncio
async def test_my_researcher():
    researcher = MyResearcher()
    results = await researcher.search("test query")
    assert len(results) > 0
```

## Déploiement

### Production

1. **Compiler tous les serveurs** :
```bash
./scripts/build-mcp-servers.sh
```

2. **Vérifier la config** :
```bash
cat config/mcp-config.json
```

3. **Variables d'environnement** :
```bash
export SEMANTIC_SCHOLAR_API_KEY="..."
export SERPER_API_KEY="..."
export NEWS_API_KEY="..."
```

### Docker

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY mcp-servers/ ./
RUN npm install && npm run build
CMD ["node", "dist/index.js"]
```

## Monitoring

### Logs

```bash
# Voir les logs d'un serveur
tail -f logs/mcp-arxiv.log
```

### Métriques

Implémenter dans chaque serveur :
- Nombre de requêtes
- Temps de réponse
- Erreurs

## Ressources

- [MCP Specification](https://spec.modelcontextprotocol.io/)
- [MCP SDK TypeScript](https://github.com/modelcontextprotocol/typescript-sdk)
- [arXiv API](https://info.arxiv.org/help/api/index.html)
- [Semantic Scholar API](https://api.semanticscholar.org/)
- [SerpAPI](https://serpapi.com/)
- [NewsAPI](https://newsapi.org/)

