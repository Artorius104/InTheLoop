# Documentation API - InTheLoop

## Base URL

```
http://localhost:8000/api
```

## Authentification

Actuellement, aucune authentification n'est requise. Pour une utilisation en production, il est recommandé d'ajouter une authentification par token.

## Endpoints

### Health Check

#### GET `/health`

Vérifie l'état de l'API.

**Réponse** :
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00.000000",
  "service": "InTheLoop API"
}
```

#### GET `/ready`

Vérifie la disponibilité de l'API.

**Réponse** :
```json
{
  "ready": true,
  "timestamp": "2024-01-01T12:00:00.000000"
}
```

### Recherches

#### POST `/research/`

Crée une nouvelle recherche scientifique.

**Corps de la requête** :
```json
{
  "topic": "Large Language Models architectures",
  "sources": ["arxiv", "semantic_scholar", "wikipedia"],
  "max_results_per_source": 10
}
```

**Paramètres** :
- `topic` (string, requis) : Sujet de recherche (3-500 caractères)
- `sources` (array, optionnel) : Liste des sources à interroger
  - Défaut : `["arxiv", "semantic_scholar", "wikipedia"]`
  - Options : `arxiv`, `semantic_scholar`, `google_scholar`, `wikipedia`, `news`, `web_search`
- `max_results_per_source` (integer, optionnel) : Nombre max de résultats par source
  - Défaut : 10
  - Min : 1, Max : 50

**Réponse** (201 Created) :
```json
{
  "id": 1,
  "topic": "Large Language Models architectures",
  "status": "pending",
  "created_at": "2024-01-01T12:00:00.000000",
  "updated_at": null,
  "completed_at": null
}
```

**Statuts possibles** :
- `pending` : En attente de traitement
- `in_progress` : Recherche en cours
- `completed` : Terminée avec succès
- `failed` : Échouée

**Erreurs** :
- `400 Bad Request` : Paramètres invalides
- `500 Internal Server Error` : Erreur serveur

**Exemple cURL** :
```bash
curl -X POST http://localhost:8000/api/research/ \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Neural networks for NLP",
    "sources": ["arxiv", "semantic_scholar"],
    "max_results_per_source": 10
  }'
```

**Exemple Python** :
```python
import requests

response = requests.post(
    "http://localhost:8000/api/research/",
    json={
        "topic": "Quantum computing",
        "sources": ["arxiv", "wikipedia"],
        "max_results_per_source": 10
    }
)

research = response.json()
print(f"Research ID: {research['id']}")
```

#### GET `/research/{id}`

Récupère les détails d'une recherche.

**Paramètres** :
- `id` (integer, requis) : ID de la recherche

**Réponse** (200 OK) :
```json
{
  "id": 1,
  "topic": "Large Language Models architectures",
  "status": "completed",
  "results": {
    "topic": "Large Language Models architectures",
    "plan": { ... },
    "raw_results": {
      "arxiv": [ ... ],
      "semantic_scholar": [ ... ]
    },
    "analysis": {
      "statistics": { ... },
      "key_findings": [ ... ],
      "trends": [ ... ]
    },
    "report": {
      "title": "Veille Scientifique: Large Language Models architectures",
      "executive_summary": "...",
      "top_papers": [ ... ],
      "insights": [ ... ],
      "recommendations": [ ... ]
    },
    "metadata": {
      "total_sources": 2,
      "total_results": 20
    }
  },
  "error": null,
  "created_at": "2024-01-01T12:00:00.000000",
  "completed_at": "2024-01-01T12:00:30.000000"
}
```

**Structure des résultats** :

```typescript
interface ResearchResult {
  id: number;
  topic: string;
  status: "pending" | "in_progress" | "completed" | "failed";
  results?: {
    topic: string;
    plan: Plan;
    raw_results: { [source: string]: Paper[] };
    analysis: Analysis;
    report: Report;
    metadata: Metadata;
  };
  error?: string;
  created_at: string;
  completed_at?: string;
}

interface Paper {
  title: string;
  authors: string[];
  abstract: string;
  url: string;
  published_date?: string;
  source: string;
  citations?: number;
  pdf_url?: string;
}

interface Report {
  title: string;
  executive_summary: string;
  top_papers: Paper[];
  insights: string[];
  trends: string[];
  recommendations: string[];
  statistics: Statistics;
}
```

**Erreurs** :
- `404 Not Found` : Recherche non trouvée
- `500 Internal Server Error` : Erreur serveur

**Exemple cURL** :
```bash
curl http://localhost:8000/api/research/1
```

**Exemple Python avec polling** :
```python
import requests
import time

research_id = 1

while True:
    response = requests.get(f"http://localhost:8000/api/research/{research_id}")
    research = response.json()
    
    status = research["status"]
    print(f"Status: {status}")
    
    if status == "completed":
        print("Results:", research["results"]["report"]["executive_summary"])
        break
    elif status == "failed":
        print("Error:", research["error"])
        break
    
    time.sleep(2)  # Attendre 2 secondes avant de revérifier
```

#### GET `/research/`

Liste toutes les recherches.

**Paramètres de query** :
- `skip` (integer, optionnel) : Nombre d'éléments à sauter (défaut: 0)
- `limit` (integer, optionnel) : Nombre max de résultats (défaut: 10, max: 100)

**Réponse** (200 OK) :
```json
[
  {
    "id": 3,
    "topic": "Latest topic",
    "status": "completed",
    "created_at": "2024-01-01T15:00:00.000000",
    "updated_at": "2024-01-01T15:00:30.000000",
    "completed_at": "2024-01-01T15:00:30.000000"
  },
  {
    "id": 2,
    "topic": "Previous topic",
    "status": "completed",
    "created_at": "2024-01-01T14:00:00.000000",
    "updated_at": "2024-01-01T14:00:25.000000",
    "completed_at": "2024-01-01T14:00:25.000000"
  }
]
```

**Note** : Les résultats sont triés par date de création (plus récent en premier).

**Exemple cURL** :
```bash
curl "http://localhost:8000/api/research/?skip=0&limit=20"
```

**Exemple Python** :
```python
response = requests.get(
    "http://localhost:8000/api/research/",
    params={"skip": 0, "limit": 20}
)
researches = response.json()

for research in researches:
    print(f"{research['id']}: {research['topic']} - {research['status']}")
```

## Codes d'Erreur

| Code | Description |
|------|-------------|
| 200 | Succès |
| 201 | Créé avec succès |
| 400 | Requête invalide |
| 404 | Ressource non trouvée |
| 422 | Validation échouée |
| 500 | Erreur serveur |

## Rate Limiting

Actuellement, aucune limite de taux n'est implémentée. Pour une utilisation en production, il est recommandé d'implémenter un rate limiting.

Limites recommandées :
- 100 requêtes/minute par IP
- 10 recherches simultanées max

## WebSocket (Futur)

Une future version pourrait inclure un support WebSocket pour les mises à jour en temps réel :

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/research/1');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Status update:', data.status);
};
```

## SDK / Clients

### Python

```python
# client.py
import requests
from typing import List, Optional

class InTheLoopClient:
    def __init__(self, base_url: str = "http://localhost:8000/api"):
        self.base_url = base_url
    
    def create_research(
        self,
        topic: str,
        sources: Optional[List[str]] = None,
        max_results: int = 10
    ):
        response = requests.post(
            f"{self.base_url}/research/",
            json={
                "topic": topic,
                "sources": sources,
                "max_results_per_source": max_results
            }
        )
        response.raise_for_status()
        return response.json()
    
    def get_research(self, research_id: int):
        response = requests.get(f"{self.base_url}/research/{research_id}")
        response.raise_for_status()
        return response.json()
    
    def list_researches(self, skip: int = 0, limit: int = 10):
        response = requests.get(
            f"{self.base_url}/research/",
            params={"skip": skip, "limit": limit}
        )
        response.raise_for_status()
        return response.json()

# Usage
client = InTheLoopClient()
research = client.create_research("AI safety")
print(research["id"])
```

### JavaScript/TypeScript

```typescript
// client.ts
class InTheLoopClient {
  constructor(private baseUrl: string = 'http://localhost:8000/api') {}

  async createResearch(
    topic: string,
    sources?: string[],
    maxResults: number = 10
  ) {
    const response = await fetch(`${this.baseUrl}/research/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        topic,
        sources,
        max_results_per_source: maxResults
      })
    });
    return response.json();
  }

  async getResearch(id: number) {
    const response = await fetch(`${this.baseUrl}/research/${id}`);
    return response.json();
  }

  async listResearches(skip: number = 0, limit: number = 10) {
    const response = await fetch(
      `${this.baseUrl}/research/?skip=${skip}&limit=${limit}`
    );
    return response.json();
  }
}

// Usage
const client = new InTheLoopClient();
const research = await client.createResearch('AI safety');
console.log(research.id);
```

## Documentation Interactive

Pour une documentation interactive complète avec tous les schémas et la possibilité de tester les endpoints :

**Swagger UI** : http://localhost:8000/docs
**ReDoc** : http://localhost:8000/redoc

## Changelog API

### v1.0.0 (Actuel)
- Endpoints de base : création, récupération, liste
- Support de 6 sources de données
- Recherche asynchrone en arrière-plan

### Futur
- v1.1.0 : WebSocket pour mises à jour temps réel
- v1.2.0 : Authentification JWT
- v1.3.0 : Rate limiting et quotas
- v2.0.0 : Recherches sauvegardées et alertes

