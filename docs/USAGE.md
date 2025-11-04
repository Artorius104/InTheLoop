# Guide d'Utilisation - InTheLoop

## Démarrage Rapide

### 1. Lancer une Nouvelle Recherche

1. Accédez à la page d'accueil (http://localhost:3000)
2. Entrez votre sujet de recherche scientifique
3. Sélectionnez les sources à interroger (arXiv, Semantic Scholar, etc.)
4. Cliquez sur "Lancer la recherche"

### 2. Suivre une Recherche

- La recherche s'exécute en arrière-plan
- Le statut est mis à jour automatiquement
- Vous pouvez fermer la page et revenir plus tard

### 3. Consulter les Résultats

Une fois terminée, la recherche affiche :
- **Résumé exécutif** : Vue d'ensemble de la recherche
- **Statistiques** : Nombre de résultats par source
- **Découvertes clés** : Points importants identifiés
- **Top articles** : Les publications les plus pertinentes
- **Recommandations** : Suggestions pour approfondir

## Fonctionnalités Détaillées

### Sources Disponibles

#### arXiv
- Base de preprints scientifiques
- Idéal pour : Physique, Mathématiques, Informatique
- Délai : ~2-5 secondes

#### Semantic Scholar
- Base académique avec citations
- Idéal pour : Toutes disciplines
- Limite gratuite : 100 requêtes/5min
- Délai : ~3-7 secondes

#### Google Scholar (via SerpAPI)
- Recherche académique Google
- **Nécessite** : Clé SerpAPI
- Idéal pour : Vue complète
- Délai : ~5-10 secondes

#### Wikipedia
- Articles encyclopédiques
- Idéal pour : Contexte général
- Délai : ~1-3 secondes

#### Actualités
- Articles de presse technique/scientifique
- **Nécessite** : Clé NewsAPI
- Idéal pour : Dernières actualités
- Délai : ~2-5 secondes

#### Recherche Web
- Recherche Google générale
- **Nécessite** : Clé Serper
- Idéal pour : Contexte entreprises
- Délai : ~2-4 secondes

### Optimisation des Recherches

#### Pour Trouver des Articles Récents
```
"Large Language Models 2024"
"Quantum computing latest advances"
```

#### Pour une Vue d'Ensemble
```
"Neural networks survey"
"CRISPR review"
```

#### Pour un Sujet Spécifique
```
"Transformer architecture attention mechanism"
"Graph neural networks molecular generation"
```

### Interprétation des Résultats

#### Score des Articles
Les articles sont classés selon :
- **Citations** : Nombre de fois cité
- **Date** : Publications récentes favorisées
- **Complétude** : Abstract et PDF disponibles

#### Statistiques
- **Résultats totaux** : Nombre d'items trouvés
- **Sources consultées** : Nombre de bases interrogées
- **Top articles** : Articles les mieux notés

#### Recommandations
Le système suggère :
- Affiner la recherche si trop de résultats
- Élargir si pas assez
- Sources complémentaires à consulter

## Exemples d'Utilisation

### Cas 1 : Veille Technologique
**Objectif** : Suivre les avancées en IA

**Configuration** :
- Sujet : "Large Language Models multimodal architectures 2024"
- Sources : arXiv, Semantic Scholar, News
- Résultats : 10 par source

**Résultat attendu** :
- 20-30 articles académiques
- 5-10 actualités récentes
- Insights sur les tendances

### Cas 2 : État de l'Art
**Objectif** : Comprendre un domaine

**Configuration** :
- Sujet : "Quantum computing applications comprehensive review"
- Sources : arXiv, Semantic Scholar, Wikipedia
- Résultats : 15 par source

**Résultat attendu** :
- Articles de référence
- Articles de synthèse
- Contexte historique

### Cas 3 : Analyse Concurrentielle
**Objectif** : Surveiller les entreprises

**Configuration** :
- Sujet : "OpenAI GPT developments"
- Sources : News, Web Search, arXiv
- Résultats : 10 par source

**Résultat attendu** :
- Actualités entreprises
- Annonces produits
- Publications techniques

## Bonnes Pratiques

### Formulation des Requêtes

✅ **Bon** :
- "Transformer neural networks attention mechanism"
- "CRISPR gene editing therapeutic applications"
- "Blockchain consensus protocols comparison"

❌ **À éviter** :
- "IA" (trop vague)
- "Comment marche ChatGPT ?" (formulation question)
- "Intelligence artificielle" (trop large)

### Sélection des Sources

**Recherche Académique** :
- arXiv + Semantic Scholar + Google Scholar

**Veille Rapide** :
- arXiv + News + Web Search

**Contexte Général** :
- Wikipedia + Semantic Scholar + News

### Gestion des Résultats

1. **Première lecture** : Résumé exécutif
2. **Approfondissement** : Top articles
3. **Action** : Suivre les recommandations

## API REST

### Créer une Recherche

```bash
curl -X POST http://localhost:8000/api/research/ \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Neural networks for NLP",
    "sources": ["arxiv", "semantic_scholar"],
    "max_results_per_source": 10
  }'
```

### Consulter une Recherche

```bash
curl http://localhost:8000/api/research/1
```

### Lister les Recherches

```bash
curl http://localhost:8000/api/research/?skip=0&limit=10
```

## Automatisation

### Script Python

```python
import requests
import time

# Créer une recherche
response = requests.post(
    "http://localhost:8000/api/research/",
    json={
        "topic": "Quantum computing",
        "sources": ["arxiv", "semantic_scholar"]
    }
)

research_id = response.json()["id"]

# Attendre la complétion
while True:
    status = requests.get(f"http://localhost:8000/api/research/{research_id}")
    data = status.json()
    
    if data["status"] == "completed":
        print("Terminé !")
        print(data["results"]["report"]["executive_summary"])
        break
    
    time.sleep(5)
```

### Script Shell

```bash
#!/bin/bash

# Créer une recherche
ID=$(curl -s -X POST http://localhost:8000/api/research/ \
  -H "Content-Type: application/json" \
  -d '{"topic": "AI safety"}' | jq -r '.id')

echo "Research ID: $ID"

# Attendre
while true; do
  STATUS=$(curl -s http://localhost:8000/api/research/$ID | jq -r '.status')
  echo "Status: $STATUS"
  
  if [ "$STATUS" = "completed" ]; then
    break
  fi
  
  sleep 5
done

# Résultats
curl -s http://localhost:8000/api/research/$ID | jq '.results.report'
```

## Limitations

### Quotas API
- Semantic Scholar : 100 req/5min
- NewsAPI gratuit : 100 req/jour
- Serper : Selon plan

### Performance
- Temps moyen : 10-30 secondes
- Max simultané : 5 recherches parallèles
- Timeout : 5 minutes

### Contenu
- Langues : Principalement anglais
- Dates : Varie par source
- Complétude : Dépend des APIs

## Support

- Issues : [GitHub](https://github.com/votre-repo/issues)
- Email : support@intheloop.com
- Docs : [Documentation complète](../README.md)

