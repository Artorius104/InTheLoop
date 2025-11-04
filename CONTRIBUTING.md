# Guide de Contribution - InTheLoop

Merci de votre intérêt pour contribuer à InTheLoop ! Ce document explique comment participer au projet.

## Code de Conduite

Soyez respectueux et professionnel dans toutes vos interactions.

## Comment Contribuer

### Signaler un Bug

1. Vérifiez que le bug n'a pas déjà été signalé dans les [Issues](https://github.com/votre-repo/issues)
2. Créez une nouvelle issue avec le template "Bug Report"
3. Incluez :
   - Description claire du problème
   - Étapes pour reproduire
   - Comportement attendu vs actuel
   - Logs/screenshots si pertinent
   - Version de Python/Node
   - OS

### Proposer une Fonctionnalité

1. Vérifiez les issues existantes
2. Créez une issue avec le template "Feature Request"
3. Décrivez :
   - Le problème que ça résout
   - La solution proposée
   - Les alternatives envisagées

### Contribuer du Code

#### 1. Fork et Clone

```bash
git clone https://github.com/votre-username/InTheLoop.git
cd InTheLoop
```

#### 2. Créer une Branche

```bash
git checkout -b feature/ma-fonctionnalite
# ou
git checkout -b fix/mon-bug
```

Convention de nommage :
- `feature/` : Nouvelle fonctionnalité
- `fix/` : Correction de bug
- `docs/` : Documentation
- `refactor/` : Refactoring
- `test/` : Tests

#### 3. Développer

```bash
# Installation
./scripts/setup.sh

# Développer...
# Tester...
```

#### 4. Tester

```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm run lint
npm run build
```

#### 5. Commit

Utilisez des messages de commit clairs :

```bash
git commit -m "feat: ajoute recherche par date pour arXiv"
git commit -m "fix: corrige crash lors de résultats vides"
git commit -m "docs: met à jour le guide d'installation"
```

Convention :
- `feat:` Nouvelle fonctionnalité
- `fix:` Correction de bug
- `docs:` Documentation
- `style:` Formatage
- `refactor:` Refactoring
- `test:` Tests
- `chore:` Maintenance

#### 6. Push et Pull Request

```bash
git push origin feature/ma-fonctionnalite
```

Puis créez une Pull Request sur GitHub avec :
- Titre clair
- Description des changements
- Référence aux issues (#123)
- Screenshots si UI

## Standards de Code

### Python (Backend)

- Style : PEP 8
- Formatter : Black
- Linter : Ruff
- Type hints recommandés

```python
def search_papers(query: str, max_results: int = 10) -> List[Paper]:
    """
    Recherche des articles scientifiques.
    
    Args:
        query: Requête de recherche
        max_results: Nombre max de résultats
        
    Returns:
        Liste d'articles trouvés
    """
    pass
```

### TypeScript (Frontend & MCP)

- Style : ESLint
- Formatter : Prettier (automatique avec ESLint)
- Types stricts

```typescript
interface SearchParams {
  query: string;
  maxResults?: number;
}

async function searchPapers(params: SearchParams): Promise<Paper[]> {
  // ...
}
```

### React (Frontend)

- Composants fonctionnels avec hooks
- TypeScript
- Props typées

```typescript
interface ButtonProps {
  onClick: () => void;
  children: React.ReactNode;
  disabled?: boolean;
}

export function Button({ onClick, children, disabled }: ButtonProps) {
  return (
    <button onClick={onClick} disabled={disabled}>
      {children}
    </button>
  );
}
```

## Structure du Projet

```
InTheLoop/
├── backend/          # FastAPI + Agents
│   ├── agents/       # Agents du framework
│   ├── api/          # Routes API
│   ├── core/         # Configuration
│   └── models/       # Modèles de données
├── frontend/         # React + Vite
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── services/
├── mcp-servers/      # Serveurs MCP
│   ├── arxiv-server/
│   └── ...
├── docs/             # Documentation
└── scripts/          # Scripts utiles
```

## Ajouter un Nouveau Serveur MCP

1. Créer le dossier :
```bash
mkdir -p mcp-servers/mon-server/src
```

2. Créer package.json, tsconfig.json, src/index.ts

3. Implémenter selon [docs/MCP.md](docs/MCP.md)

4. Ajouter à `scripts/build-mcp-servers.sh`

5. Créer un agent correspondant dans `backend/agents/researchers.py`

6. Mettre à jour la documentation

## Tests

### Backend

```bash
cd backend
pytest tests/
pytest tests/test_specific.py
pytest -v  # Verbose
pytest --cov  # Coverage
```

Écrire des tests :
```python
# tests/test_researcher.py
import pytest
from agents.researchers import ArxivResearcher

@pytest.mark.asyncio
async def test_arxiv_search():
    researcher = ArxivResearcher()
    results = await researcher.search("test query", max_results=5)
    assert len(results) > 0
    assert "title" in results[0]
```

### Frontend

```bash
cd frontend
npm run test
npm run test:coverage
```

## Documentation

- Code : Docstrings/JSDoc
- API : Maintenir docs/API.md
- Features : Mettre à jour README.md
- Exemples : Ajouter dans docs/USAGE.md

## Review Process

Les Pull Requests sont reviewées selon :
- ✅ Tests passent
- ✅ Code respecte les standards
- ✅ Documentation à jour
- ✅ Pas de régression
- ✅ Commit messages clairs

## Licence

En contribuant, vous acceptez que vos contributions soient sous la même licence que le projet (voir LICENSE).

## Questions

- Issues GitHub pour bugs/features
- Discussions GitHub pour questions
- Email : dev@intheloop.com

Merci de contribuer ! 🎉

