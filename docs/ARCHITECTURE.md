# Architecture du Système de Veille AI

## Vue d'ensemble

Le système de veille AI est conçu pour surveiller automatiquement les nouveaux papiers de recherche sur ArXiv et les analyser selon leur pertinence.

## Composants principaux

### 1. Agent de Monitoring (`ResearchMonitorAgent`)
- Orchestre le processus de veille
- Planifie les cycles de recherche
- Coordonne les différents services

### 2. Service ArXiv (`ArxivService`)
- Interface avec MCP ArXiv
- Recherche et récupération des papiers
- Gestion du cache des requêtes

### 3. Analyseur IA (`AIAnalyzer`)
- Évaluation de la pertinence
- Génération de résumés
- Extraction de mots-clés

### 4. Gestionnaire de Base de Données (`DatabaseManager`)
- Stockage des papiers et métadonnées
- Gestion des états de traitement
- Historique des analyses

## Flux de données

1. **Recherche** : L'agent lance des requêtes périodiques via ArXiv
2. **Analyse** : Chaque papier est analysé par l'IA pour sa pertinence
3. **Stockage** : Les résultats sont sauvegardés en base
4. **Traitement** : Les papiers pertinents sont traités (notifications, résumés)

## Configuration MCP

Le système utilise MCP ArXiv configuré dans `.kiro/settings/mcp.json` pour accéder aux données de recherche.