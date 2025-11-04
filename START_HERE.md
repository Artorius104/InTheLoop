# 🚀 START HERE - InTheLoop

**Bienvenue dans InTheLoop !** Votre plateforme de veille scientifique intelligente.

## 📍 Vous êtes ici

Vous venez de créer un projet complet de veille scientifique avec :
- ✅ **65+ fichiers** créés automatiquement
- ✅ **Backend FastAPI** avec framework agentic
- ✅ **Frontend React** moderne
- ✅ **7 serveurs MCP** pour sources multiples
- ✅ **Documentation complète**

## ⚡ Démarrage Rapide (5 minutes)

### Option 1 : Installation Automatique ⭐ RECOMMANDÉ

```bash
# 1. Installation (2-3 minutes)
./scripts/setup.sh

# 2. Démarrage
./scripts/start-dev.sh

# 3. Ouvrir le navigateur
# → http://localhost:3000
```

### Option 2 : Installation Manuelle

```bash
# Backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload &

# Frontend  
cd ../frontend
npm install
npm run dev &

# Ouvrir http://localhost:3000
```

## 🎯 Première Utilisation

1. **Ouvrez** http://localhost:3000
2. **Entrez** un sujet : "Large Language Models"
3. **Sélectionnez** : arXiv et Wikipedia (pas de clé API requise)
4. **Cliquez** "Lancer la recherche"
5. **Attendez** 10-20 secondes
6. **Consultez** les résultats !

## 📚 Documentation Essentielle

| Fichier | Quand l'utiliser |
|---------|------------------|
| **[QUICKSTART.md](QUICKSTART.md)** | ⭐ Commencer maintenant (5 min) |
| **[SETUP_COMPLETE.md](SETUP_COMPLETE.md)** | Vue d'ensemble complète |
| **[CHECKLIST.md](CHECKLIST.md)** | Vérifier l'installation |
| **[docs/INSTALLATION.md](docs/INSTALLATION.md)** | Installation détaillée |
| **[docs/USAGE.md](docs/USAGE.md)** | Guide utilisateur complet |
| **[docs/API.md](docs/API.md)** | Documentation API REST |

## 🎓 Comprendre le Projet

### Architecture Simple

```
Frontend (React)
     ↓ HTTP
Backend (FastAPI)
     ↓ Framework Agentic
MCP Servers (7 serveurs)
     ↓ API Calls
Sources Externes (arXiv, etc.)
```

### Workflow

```
1. Utilisateur saisit un sujet
2. Planner Agent crée une stratégie
3. Researcher Agents cherchent en parallèle
4. Analyzer Agent synthétise
5. Reporter Agent génère le rapport
6. Utilisateur voit les résultats
```

## 🔑 Clés API (Optionnel)

**Aucune clé requise pour démarrer !**

Le système fonctionne avec arXiv et Wikipedia sans configuration.

Pour plus de sources, ajoutez dans `.env` :
```bash
SEMANTIC_SCHOLAR_API_KEY=xxx  # Gratuit sur semanticscholar.org
SERPER_API_KEY=xxx            # 2500 recherches gratuites
NEWS_API_KEY=xxx              # 100/jour gratuit
```

## 🎨 Fonctionnalités

### ✅ Disponibles Maintenant
- Recherche multi-sources (6 sources)
- Analyse intelligente par agents
- Interface moderne et responsive
- Rapports détaillés avec top articles
- Historique des recherches
- API REST complète

### 🔄 À Venir (Roadmap)
- WebSocket temps réel
- Cache Redis
- Authentification
- Plus de sources (PubMed, IEEE)
- Export PDF
- Alertes automatiques

## 🧪 Tests Rapides

### Test 1 : Backend
```bash
curl http://localhost:8000/api/health
# Attendu: {"status": "healthy", ...}
```

### Test 2 : Frontend
Ouvrir http://localhost:3000
→ Page d'accueil doit s'afficher

### Test 3 : Recherche Complète
1. Aller sur http://localhost:3000
2. Rechercher "AI safety"
3. Résultats en ~15 secondes

## 📊 Statistiques

```
65+ fichiers créés
16  fichiers Python (Backend)
16  fichiers TypeScript (Frontend)
7   serveurs MCP
10+ fichiers documentation
~5000 lignes de code
```

## 🐛 Problèmes Fréquents

### Port déjà utilisé
```bash
# Dans .env
BACKEND_PORT=8001
FRONTEND_PORT=3001
```

### Module non trouvé
```bash
# Backend
cd backend && source venv/bin/activate
pip install --force-reinstall -r requirements.txt

# Frontend
cd frontend && rm -rf node_modules && npm install
```

### Recherche échoue
1. Vérifier que backend tourne (http://localhost:8000)
2. Tester avec arXiv seul (pas de clé requise)
3. Voir logs backend dans terminal

## 📞 Aide

- 📖 Documentation complète dans `/docs`
- ✅ Checklist d'installation : [CHECKLIST.md](CHECKLIST.md)
- 🔍 Résumé du projet : [SUMMARY.md](SUMMARY.md)
- 🏗️ Architecture : [ARCHITECTURE.md](ARCHITECTURE.md)

## 🎯 Prochaines Étapes Recommandées

### Étape 1 : Installation (si pas fait)
```bash
./scripts/setup.sh
```

### Étape 2 : Premier lancement
```bash
./scripts/start-dev.sh
```

### Étape 3 : Première recherche
- Ouvrir http://localhost:3000
- Essayer "Neural networks for NLP"

### Étape 4 : Explorer
- Lire [docs/USAGE.md](docs/USAGE.md) pour exemples
- Tester différentes sources
- Consulter l'historique

### Étape 5 : Personnaliser
- Ajouter clés API dans `.env`
- Tester toutes les sources
- Explorer l'API REST

## 💡 Exemples de Recherches

### Recherche Académique
**Sujet** : "Transformer architecture improvements"
**Sources** : arXiv, Semantic Scholar
**Résultat** : Articles récents avec citations

### Veille Technologique  
**Sujet** : "OpenAI GPT-4 developments 2024"
**Sources** : arXiv, News, Web Search
**Résultat** : Mix articles académiques + actualités

### État de l'Art
**Sujet** : "Quantum computing comprehensive survey"
**Sources** : arXiv, Semantic Scholar, Wikipedia
**Résultat** : Vue d'ensemble complète

## 🚀 Aller Plus Loin

### Développement
- Lire [ARCHITECTURE.md](ARCHITECTURE.md)
- Contribuer : [CONTRIBUTING.md](CONTRIBUTING.md)
- Ajouter un serveur MCP : [docs/MCP.md](docs/MCP.md)

### Utilisation Avancée
- API REST : [docs/API.md](docs/API.md)
- Automatisation : Scripts dans [docs/USAGE.md](docs/USAGE.md)
- Déploiement : [docs/INSTALLATION.md](docs/INSTALLATION.md)

## ✅ Checklist Rapide

Avant de commencer :
- [ ] Python 3.11+ installé
- [ ] Node.js 18+ installé
- [ ] Ports 3000 et 8000 libres
- [ ] Connexion internet active

Après installation :
- [ ] Backend répond sur :8000
- [ ] Frontend affiche sur :3000
- [ ] Première recherche réussie

## 🎉 Félicitations !

Vous avez maintenant une plateforme complète de veille scientifique.

**Prêt à commencer ?**

```bash
./scripts/start-dev.sh
```

Puis ouvrez http://localhost:3000 et lancez votre première recherche !

---

**Besoin d'aide ?** Consultez [QUICKSTART.md](QUICKSTART.md) ou [SETUP_COMPLETE.md](SETUP_COMPLETE.md)

**Version** : 1.0.0  
**Status** : ✅ Prêt à l'emploi  
**Date** : Novembre 2025

