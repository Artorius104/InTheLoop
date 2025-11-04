# Guide d'Installation - InTheLoop

## Prérequis

- Python 3.11 ou supérieur
- Node.js 18 ou supérieur
- npm ou yarn
- Git

## Installation du Backend

### 1. Créer l'environnement virtuel Python

```bash
cd backend
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3. Configuration

Créez un fichier `.env` à la racine du projet :

```bash
# Copier l'exemple
cp .env.example .env

# Éditer avec vos clés API
nano .env  # ou votre éditeur préféré
```

Variables importantes :
- `OPENAI_API_KEY` ou `ANTHROPIC_API_KEY` : Pour les capacités IA (optionnel)
- `SEMANTIC_SCHOLAR_API_KEY` : Pour Semantic Scholar
- `SERPER_API_KEY` : Pour la recherche web
- `NEWS_API_KEY` : Pour les actualités

### 4. Initialiser la base de données

```bash
# La base sera créée automatiquement au premier lancement
python main.py
```

### 5. Lancer le serveur

```bash
# Mode développement
uvicorn main:app --reload --port 8000

# Ou directement
python main.py
```

Le backend sera accessible sur http://localhost:8000

## Installation du Frontend

### 1. Installer les dépendances

```bash
cd frontend
npm install

# ou avec yarn
yarn install
```

### 2. Configuration

Créez un fichier `.env.local` dans le dossier frontend :

```bash
VITE_API_URL=http://localhost:8000/api
```

### 3. Lancer le serveur de développement

```bash
npm run dev

# ou avec yarn
yarn dev
```

Le frontend sera accessible sur http://localhost:3000

## Installation des Serveurs MCP

Les serveurs MCP doivent être compilés avant utilisation :

### 1. Compiler tous les serveurs

```bash
# Script pour compiler tous les serveurs
cd mcp-servers

for dir in */; do
  echo "Building $dir"
  cd "$dir"
  npm install
  npm run build
  cd ..
done
```

### 2. Compiler un serveur spécifique

```bash
cd mcp-servers/arxiv-server
npm install
npm run build
```

### 3. Tester un serveur

```bash
cd mcp-servers/arxiv-server
npm run dev
```

## Vérification de l'installation

### Backend

```bash
curl http://localhost:8000/api/health
```

Réponse attendue :
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00.000000",
  "service": "InTheLoop API"
}
```

### Frontend

Ouvrez http://localhost:3000 dans votre navigateur. Vous devriez voir la page d'accueil.

## Dépannage

### Erreur : Port déjà utilisé

Backend :
```bash
# Changer le port
uvicorn main:app --reload --port 8001
```

Frontend :
```bash
# Le port sera automatiquement changé si 3000 est occupé
# Ou spécifier manuellement dans vite.config.ts
```

### Erreur : Module non trouvé (Python)

```bash
# Réinstaller les dépendances
pip install --upgrade -r requirements.txt
```

### Erreur : Package non trouvé (Node)

```bash
# Supprimer node_modules et réinstaller
rm -rf node_modules
npm install
```

### Base de données corrompue

```bash
# Supprimer et recréer
rm backend/intheloop.db
python backend/main.py
```

## Configuration Avancée

### Utiliser PostgreSQL au lieu de SQLite

Modifier dans `.env` :
```bash
DATABASE_URL=postgresql+asyncpg://user:password@localhost/intheloop
```

Installer le driver :
```bash
pip install asyncpg psycopg2-binary
```

### Configurer CORS

Dans `backend/core/config.py`, modifier `CORS_ORIGINS` :
```python
CORS_ORIGINS = [
    "http://localhost:3000",
    "https://votre-domaine.com"
]
```

### Mode Production

Backend :
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

Frontend :
```bash
npm run build
# Les fichiers seront dans dist/
```

## Prochaines Étapes

- Consultez le [Guide d'Utilisation](USAGE.md)
- Explorez la [Documentation API](API.md)
- Lisez la [Documentation MCP](MCP.md)

