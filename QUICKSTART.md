# Démarrage Rapide - InTheLoop

## Installation en 5 minutes

### 1. Cloner et installer

```bash
# Cloner le projet (si depuis Git)
git clone <url-repo>
cd InTheLoop

# Ou si déjà cloné, installation automatique
./scripts/setup.sh
```

### 2. Configurer les clés API (optionnel)

Éditez le fichier `.env` :

```bash
# Minimum requis (aucune clé nécessaire pour démarrer)
# arXiv et Wikipedia fonctionnent sans clés

# Optionnel mais recommandé
SEMANTIC_SCHOLAR_API_KEY=votre_cle_ici

# Pour fonctionnalités avancées
SERPER_API_KEY=votre_cle_ici
NEWS_API_KEY=votre_cle_ici
```

**Note** : Vous pouvez commencer sans aucune clé API ! Le système fonctionnera avec arXiv et Wikipedia.

### 3. Démarrer l'application

```bash
./scripts/start-dev.sh
```

Attendez quelques secondes, puis ouvrez :
- **Frontend** : http://localhost:3000
- **API** : http://localhost:8000/docs

### 4. Première recherche

1. Accédez à http://localhost:3000
2. Entrez un sujet : "Large Language Models"
3. Sélectionnez les sources : arXiv, Wikipedia
4. Cliquez sur "Lancer la recherche"
5. Attendez 10-30 secondes
6. Consultez les résultats !

## Installation Manuelle

Si le script automatique ne fonctionne pas :

### Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Serveurs MCP (optionnel)

```bash
cd mcp-servers/arxiv-server
npm install
npm run build
```

## Test de l'Installation

### Vérifier le backend

```bash
curl http://localhost:8000/api/health
```

Devrait retourner :
```json
{
  "status": "healthy",
  "timestamp": "...",
  "service": "InTheLoop API"
}
```

### Vérifier le frontend

Ouvrez http://localhost:3000 dans votre navigateur. Vous devriez voir la page d'accueil.

## Obtenir les Clés API (optionnel)

### Semantic Scholar (Recommandé)
1. Visitez https://www.semanticscholar.org/product/api
2. Créez un compte gratuit
3. Obtenez votre clé API
4. Ajoutez dans `.env` : `SEMANTIC_SCHOLAR_API_KEY=votre_cle`

### Serper (Pour recherche web)
1. Visitez https://serper.dev
2. Inscription gratuite : 2500 recherches
3. Obtenez votre clé API
4. Ajoutez dans `.env` : `SERPER_API_KEY=votre_cle`

### NewsAPI (Pour actualités)
1. Visitez https://newsapi.org
2. Plan gratuit : 100 requêtes/jour
3. Obtenez votre clé API
4. Ajoutez dans `.env` : `NEWS_API_KEY=votre_cle`

## Exemples de Recherche

### Recherche Simple
**Sujet** : "Neural networks for computer vision"
**Sources** : arXiv, Wikipedia
**Temps** : ~10 secondes

### Recherche Complète
**Sujet** : "Quantum computing applications in cryptography"
**Sources** : arXiv, Semantic Scholar, Wikipedia, News
**Temps** : ~30 secondes

### Veille Technologique
**Sujet** : "GPT-4 architecture improvements 2024"
**Sources** : arXiv, News, Web Search
**Temps** : ~20 secondes

## Dépannage Rapide

### Le backend ne démarre pas

```bash
# Vérifier Python
python3 --version  # Doit être 3.11+

# Réinstaller les dépendances
cd backend
pip install --force-reinstall -r requirements.txt
```

### Le frontend ne démarre pas

```bash
# Vérifier Node
node --version  # Doit être 18+

# Réinstaller
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Port déjà utilisé

```bash
# Changer les ports dans .env
BACKEND_PORT=8001
FRONTEND_PORT=3001
```

### Erreur "Module not found"

```bash
# Backend
cd backend
source venv/bin/activate
pip install <module-manquant>

# Frontend
cd frontend
npm install <module-manquant>
```

## Arrêter l'Application

Appuyez sur `Ctrl+C` dans le terminal où vous avez lancé `start-dev.sh`

Ou manuellement :
```bash
# Tuer tous les processus
pkill -f "uvicorn main:app"
pkill -f "vite"
```

## Prochaines Étapes

1. 📖 Lisez le [Guide d'Utilisation](docs/USAGE.md)
2. 🔧 Consultez la [Documentation MCP](docs/MCP.md)
3. 🚀 Explorez l'[API](http://localhost:8000/docs)
4. 💡 Testez différents sujets de recherche

## Besoin d'Aide ?

- 📚 [Documentation complète](README.md)
- 🐛 [Signaler un bug](https://github.com/votre-repo/issues)
- 💬 [Discussions](https://github.com/votre-repo/discussions)

---

**Prêt à explorer la science ! 🚀**

