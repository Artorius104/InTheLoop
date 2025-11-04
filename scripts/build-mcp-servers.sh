#!/bin/bash

# Script pour compiler tous les serveurs MCP

set -e

echo "🔨 Compilation des serveurs MCP..."

# Couleurs
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Vérifier que nous sommes dans le bon répertoire
if [ ! -d "mcp-servers" ]; then
    echo "❌ Erreur: Le dossier mcp-servers n'existe pas"
    exit 1
fi

cd mcp-servers

# Liste des serveurs
SERVERS=(
    "arxiv-server"
    "semantic-scholar-server"
    "google-scholar-server"
    "wikipedia-server"
    "web-search-server"
    "webscraping-server"
    "news-server"
)

# Compiler chaque serveur
for server in "${SERVERS[@]}"; do
    if [ -d "$server" ]; then
        echo -e "\n${YELLOW}Building $server...${NC}"
        cd "$server"
        
        # Installer les dépendances si nécessaire
        if [ ! -d "node_modules" ]; then
            echo "Installation des dépendances..."
            npm install
        fi
        
        # Compiler
        npm run build
        
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✓ $server compilé avec succès${NC}"
        else
            echo "❌ Erreur lors de la compilation de $server"
            exit 1
        fi
        
        cd ..
    else
        echo "⚠️  $server non trouvé, ignoré"
    fi
done

cd ..

echo -e "\n${GREEN}✅ Tous les serveurs MCP ont été compilés avec succès${NC}"

