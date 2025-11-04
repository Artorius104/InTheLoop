# Frontend Streamlit - InTheLoop

Interface utilisateur simple et moderne construite avec Streamlit.

## Installation

```bash
cd backend
source venv/bin/activate
pip install streamlit
```

## Lancement

```bash
# Depuis la racine du projet
cd backend
source venv/bin/activate
streamlit run ../frontend/app.py
```

Ou utilisez le script de démarrage automatique :

```bash
./start.sh
```

## Accès

- Frontend : http://localhost:3000
- Backend API : http://localhost:8000
- Documentation API : http://localhost:8000/docs

## Fonctionnalités

✅ Nouvelle recherche scientifique
✅ Sélection des sources
✅ Suivi en temps réel
✅ Historique des recherches
✅ Affichage des résultats détaillés
✅ Top articles avec liens
✅ Recommandations

## Navigation

- **🔍 Nouvelle Recherche** : Créer une nouvelle recherche scientifique
- **📜 Historique** : Consulter toutes vos recherches passées

## Sources disponibles

- **arXiv** : Preprints scientifiques (pas de clé API requise)
- **Semantic Scholar** : Articles académiques avec citations
- **Wikipedia** : Contexte encyclopédique (pas de clé API requise)
- **Actualités** : Articles de presse scientifique (nécessite NEWS_API_KEY)
- **Web Search** : Recherche web générale (nécessite SERPER_API_KEY)

