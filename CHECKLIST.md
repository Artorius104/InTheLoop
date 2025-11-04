# Checklist de Vérification - InTheLoop

Utilisez cette checklist pour vérifier que le projet est correctement installé et fonctionnel.

## ✅ Phase 1 : Vérification des Fichiers

### Documentation
- [ ] README.md existe
- [ ] QUICKSTART.md existe
- [ ] SETUP_COMPLETE.md existe
- [ ] docs/INSTALLATION.md existe
- [ ] docs/USAGE.md existe
- [ ] docs/API.md existe
- [ ] docs/MCP.md existe
- [ ] ARCHITECTURE.md existe
- [ ] CONTRIBUTING.md existe
- [ ] SUMMARY.md existe

### Backend
- [ ] backend/main.py existe
- [ ] backend/requirements.txt existe
- [ ] backend/agents/coordinator.py existe
- [ ] backend/agents/planner.py existe
- [ ] backend/agents/researchers.py existe
- [ ] backend/agents/analyzer.py existe
- [ ] backend/agents/reporter.py existe
- [ ] backend/api/routes/health.py existe
- [ ] backend/api/routes/research.py existe
- [ ] backend/core/config.py existe
- [ ] backend/core/database.py existe
- [ ] backend/models/research.py existe

### Frontend
- [ ] frontend/package.json existe
- [ ] frontend/src/App.tsx existe
- [ ] frontend/src/main.tsx existe
- [ ] frontend/src/pages/HomePage.tsx existe
- [ ] frontend/src/pages/ResearchPage.tsx existe
- [ ] frontend/src/pages/HistoryPage.tsx existe
- [ ] frontend/src/components/Layout.tsx existe
- [ ] frontend/src/services/api.ts existe
- [ ] frontend/vite.config.ts existe
- [ ] frontend/tailwind.config.js existe

### MCP Servers
- [ ] mcp-servers/arxiv-server/src/index.ts existe
- [ ] mcp-servers/semantic-scholar-server/src/index.ts existe
- [ ] mcp-servers/google-scholar-server/src/index.ts existe
- [ ] mcp-servers/wikipedia-server/src/index.ts existe
- [ ] mcp-servers/web-search-server/src/index.ts existe
- [ ] mcp-servers/webscraping-server/src/index.ts existe
- [ ] mcp-servers/news-server/src/index.ts existe

### Scripts
- [ ] scripts/setup.sh existe et est exécutable
- [ ] scripts/start-dev.sh existe et est exécutable
- [ ] scripts/build-mcp-servers.sh existe et est exécutable

### Configuration
- [ ] config/mcp-config.json existe
- [ ] .gitignore existe

## ✅ Phase 2 : Installation

### Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate sur Windows
pip install -r requirements.txt
```

- [ ] Environnement virtuel créé
- [ ] Dépendances Python installées sans erreur
- [ ] FastAPI installé
- [ ] SQLAlchemy installé

### Frontend
```bash
cd frontend
npm install
```

- [ ] node_modules créé
- [ ] Dépendances installées sans erreur
- [ ] React installé
- [ ] Vite installé

### MCP Servers (optionnel)
```bash
cd mcp-servers
./scripts/build-mcp-servers.sh
```

- [ ] arxiv-server compilé
- [ ] semantic-scholar-server compilé
- [ ] Tous les serveurs compilés

## ✅ Phase 3 : Configuration

### Créer .env (optionnel)
```bash
# À la racine du projet
touch .env
```

- [ ] Fichier .env créé
- [ ] Clés API ajoutées (si disponibles)

### Vérifier les Ports
- [ ] Port 8000 libre (backend)
- [ ] Port 3000 libre (frontend)

## ✅ Phase 4 : Tests de Démarrage

### Backend
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload
```

Vérifications :
- [ ] Backend démarre sans erreur
- [ ] Message "Application startup complete"
- [ ] http://localhost:8000 accessible
- [ ] http://localhost:8000/docs affiche Swagger UI

### Test API Backend
```bash
curl http://localhost:8000/api/health
```

Attendu :
```json
{
  "status": "healthy",
  "timestamp": "...",
  "service": "InTheLoop API"
}
```

- [ ] Endpoint /api/health répond
- [ ] Status est "healthy"

### Frontend
```bash
cd frontend
npm run dev
```

Vérifications :
- [ ] Frontend démarre sans erreur
- [ ] http://localhost:3000 accessible
- [ ] Page d'accueil s'affiche correctement
- [ ] Aucune erreur dans la console navigateur

## ✅ Phase 5 : Tests Fonctionnels

### Test 1 : Recherche Simple

1. Aller sur http://localhost:3000
2. Entrer "Neural networks" dans le champ de recherche
3. Sélectionner "arXiv" et "Wikipedia"
4. Cliquer "Lancer la recherche"

Vérifications :
- [ ] Recherche créée (redirection vers /research/1)
- [ ] Status "En cours" affiché
- [ ] Status passe à "Terminée" après 10-30s
- [ ] Résultats affichés correctement
- [ ] Résumé exécutif présent
- [ ] Top articles listés
- [ ] Statistiques affichées

### Test 2 : Historique

1. Retourner à l'accueil
2. Créer une 2ème recherche
3. Aller sur "Historique"

Vérifications :
- [ ] Les 2 recherches sont listées
- [ ] Dates affichées correctement
- [ ] Status corrects
- [ ] Clic redirige vers la recherche

### Test 3 : API REST

```bash
# Créer une recherche via API
curl -X POST http://localhost:8000/api/research/ \
  -H "Content-Type: application/json" \
  -d '{"topic": "AI safety", "sources": ["arxiv"]}'

# Noter l'ID retourné, puis :
curl http://localhost:8000/api/research/1
```

Vérifications :
- [ ] POST crée une recherche (status 201)
- [ ] ID retourné
- [ ] GET récupère la recherche
- [ ] Résultats présents quand status=completed

## ✅ Phase 6 : Tests Avancés (optionnel)

### Avec Clés API

Si vous avez configuré les clés :

1. Test Semantic Scholar
   - [ ] Recherche avec source "semantic_scholar"
   - [ ] Résultats avec citations

2. Test Web Search
   - [ ] Recherche avec source "web_search"
   - [ ] Résultats web présents

3. Test News
   - [ ] Recherche avec source "news"
   - [ ] Articles de presse présents

### Tests de Charge

```bash
# Créer 5 recherches simultanées
for i in {1..5}; do
  curl -X POST http://localhost:8000/api/research/ \
    -H "Content-Type: application/json" \
    -d "{\"topic\": \"test $i\"}" &
done
```

- [ ] Toutes les recherches traitées
- [ ] Pas de crash
- [ ] Temps raisonnables

## ✅ Phase 7 : Vérification du Code

### Backend

```bash
cd backend
source venv/bin/activate

# Tests (si disponibles)
pytest

# Linting
ruff check .
```

- [ ] Pas d'erreur de linting majeure
- [ ] Tests passent (si présents)

### Frontend

```bash
cd frontend

# Linting
npm run lint

# Build
npm run build
```

- [ ] Pas d'erreur de linting
- [ ] Build réussit
- [ ] Dossier dist/ créé

## ✅ Phase 8 : Documentation

### Vérifier que la documentation est claire

- [ ] README.md explique bien le projet
- [ ] QUICKSTART.md permet de démarrer en 5 min
- [ ] INSTALLATION.md couvre tous les cas
- [ ] USAGE.md donne des exemples concrets
- [ ] API.md documente tous les endpoints
- [ ] MCP.md explique les serveurs

### Tester les exemples de code

Tester quelques exemples du guide :
- [ ] Exemple Python client (USAGE.md)
- [ ] Exemple cURL (API.md)
- [ ] Exemple création serveur MCP (MCP.md)

## ✅ Phase 9 : Performance

### Mesurer les temps

- [ ] Recherche arXiv seul : < 10s
- [ ] Recherche multi-sources : < 30s
- [ ] Réponse API (hors recherche) : < 100ms
- [ ] Chargement frontend : < 2s

### Vérifier les ressources

- [ ] Backend : < 200 MB RAM
- [ ] Frontend build : < 5 MB
- [ ] Pas de memory leak après plusieurs recherches

## ✅ Phase 10 : Production Ready (optionnel)

### Sécurité

- [ ] CORS bien configuré
- [ ] Validation des inputs (Pydantic)
- [ ] Pas de clés API en dur dans le code
- [ ] .env dans .gitignore

### Déploiement

- [ ] Frontend build sans erreur
- [ ] Backend peut tourner avec Gunicorn
- [ ] Variables d'environnement bien gérées
- [ ] Documentation de déploiement présente

## 📊 Score Final

Comptez vos ✅ :

- **0-30** : Installation incomplète, voir INSTALLATION.md
- **31-60** : Installation de base OK, continuer les tests
- **61-90** : Très bon, projet fonctionnel
- **91+** : Excellent, projet production-ready !

## 🐛 En Cas de Problème

### Backend ne démarre pas
1. Vérifier Python 3.11+
2. Vérifier venv activé
3. Réinstaller dépendances
4. Voir logs dans terminal

### Frontend ne démarre pas
1. Vérifier Node 18+
2. Supprimer node_modules et réinstaller
3. Vérifier port 3000 libre

### Tests échouent
1. Vérifier que backend et frontend tournent
2. Vérifier les URLs (localhost:8000 et 3000)
3. Vérifier la connexion réseau

### Recherche échoue
1. Vérifier les logs backend
2. Tester avec arXiv seul (pas de clé requise)
3. Vérifier la connexion internet

## 📞 Support

Si des problèmes persistent :
- Consulter docs/INSTALLATION.md
- Créer une issue GitHub
- Contacter le support

---

**Bonne chance ! 🚀**

