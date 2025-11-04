# 🚀 Démarrage Rapide - InTheLoop

## Commandes à exécuter

### Terminal 1 : Backend

```bash
cd /home/artorius/Projects/ESGI/IA/Gestion_Projet/InTheLoop/backend
source venv/bin/activate
uvicorn main:app --reload --port 8000
```

**Vous devriez voir** :
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000
```

✅ **Backend prêt** sur http://localhost:8000

---

### Terminal 2 : Frontend Streamlit

Ouvrez un **nouveau terminal**, puis :

```bash
cd /home/artorius/Projects/ESGI/IA/Gestion_Projet/InTheLoop/backend
source venv/bin/activate
streamlit run ../frontend/app.py
```

**Vous devriez voir** :
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
```

✅ **Frontend prêt** sur http://localhost:8501

---

## 🌐 Accès

Une fois les deux services lancés :

- **Frontend** : http://localhost:8501 (Streamlit change parfois le port)
- **Backend** : http://localhost:8000
- **API Docs** : http://localhost:8000/docs

---

## ✅ Test Rapide

1. Ouvrir http://localhost:8501
2. Entrer : "Large Language Models"
3. Cocher : arXiv + Wikipedia
4. Cliquer : "🚀 Lancer la recherche"
5. Attendre 30-60 secondes
6. Voir les résultats !

---

## 🐛 Problèmes Fréquents

### "command not found: uvicorn"
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

### "Connection refused"
Le backend n'est pas démarré. Lancez-le d'abord (Terminal 1).

### Port déjà utilisé
```bash
# Backend sur autre port
uvicorn main:app --reload --port 8001

# Frontend sur autre port  
streamlit run ../frontend/app.py --server.port 3001
```

---

## 🎯 Script Automatique

Pour tout lancer automatiquement :

```bash
./start.sh
```

**Note** : Ce script lance backend ET frontend ensemble.

---

Prêt à explorer la science ! 🔬

