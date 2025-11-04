#!/bin/bash

# Script d'installation complète du projet InTheLoop

set -e

echo "🎯 Installation de InTheLoop"
echo "=============================="

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Fonction pour vérifier les prérequis
check_requirements() {
    echo -e "\n${BLUE}Vérification des prérequis...${NC}"
    
    # Python
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}❌ Python 3 n'est pas installé${NC}"
        exit 1
    fi
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
    echo -e "${GREEN}✓ Python $PYTHON_VERSION${NC}"
    
    # Node.js
    if ! command -v node &> /dev/null; then
        echo -e "${RED}❌ Node.js n'est pas installé${NC}"
        exit 1
    fi
    NODE_VERSION=$(node --version)
    echo -e "${GREEN}✓ Node.js $NODE_VERSION${NC}"
    
    # npm
    if ! command -v npm &> /dev/null; then
        echo -e "${RED}❌ npm n'est pas installé${NC}"
        exit 1
    fi
    NPM_VERSION=$(npm --version)
    echo -e "${GREEN}✓ npm $NPM_VERSION${NC}"
}

# Installation du backend
install_backend() {
    echo -e "\n${BLUE}📦 Installation du backend...${NC}"
    
    cd backend
    
    # Créer l'environnement virtuel
    if [ ! -d "venv" ]; then
        echo "Création de l'environnement virtuel Python..."
        python3 -m venv venv
    fi
    
    # Activer et installer les dépendances
    source venv/bin/activate
    echo "Installation des dépendances Python..."
    pip install --upgrade pip
    pip install -r requirements.txt
    
    echo -e "${GREEN}✓ Backend installé${NC}"
    cd ..
}

# Installation du frontend
install_frontend() {
    echo -e "\n${BLUE}🎨 Installation du frontend...${NC}"
    
    cd frontend
    
    echo "Installation des dépendances Node.js..."
    npm install
    
    echo -e "${GREEN}✓ Frontend installé${NC}"
    cd ..
}

# Installation des serveurs MCP
install_mcp_servers() {
    echo -e "\n${BLUE}🔌 Installation des serveurs MCP...${NC}"
    
    cd mcp-servers
    
    SERVERS=(
        "arxiv-server"
        "semantic-scholar-server"
        "google-scholar-server"
        "wikipedia-server"
        "web-search-server"
        "webscraping-server"
        "news-server"
    )
    
    for server in "${SERVERS[@]}"; do
        if [ -d "$server" ]; then
            echo -e "${YELLOW}Installation de $server...${NC}"
            cd "$server"
            npm install
            npm run build
            cd ..
            echo -e "${GREEN}✓ $server installé${NC}"
        fi
    done
    
    cd ..
}

# Configuration
setup_config() {
    echo -e "\n${BLUE}⚙️  Configuration...${NC}"
    
    # Créer le dossier logs
    mkdir -p logs
    
    # Créer le fichier .env s'il n'existe pas
    if [ ! -f ".env" ]; then
        if [ -f ".env.example" ]; then
            echo "Création du fichier .env..."
            cp .env.example .env
            echo -e "${GREEN}✓ Fichier .env créé${NC}"
            echo -e "${YELLOW}⚠️  N'oubliez pas de configurer vos clés API dans .env${NC}"
        fi
    else
        echo -e "${GREEN}✓ Fichier .env existe déjà${NC}"
    fi
    
    # Rendre les scripts exécutables
    chmod +x scripts/*.sh
    echo -e "${GREEN}✓ Scripts configurés${NC}"
}

# Afficher les instructions finales
show_instructions() {
    echo -e "\n${GREEN}✅ Installation terminée !${NC}\n"
    echo "📋 Prochaines étapes :"
    echo "   1. Configurez vos clés API dans le fichier .env"
    echo "   2. Lancez le projet avec: ./scripts/start-dev.sh"
    echo ""
    echo "📚 Documentation :"
    echo "   - Installation: docs/INSTALLATION.md"
    echo "   - Utilisation: docs/USAGE.md"
    echo "   - MCP: docs/MCP.md"
    echo ""
    echo "🔗 URLs (après démarrage) :"
    echo "   - Frontend: http://localhost:3000"
    echo "   - Backend API: http://localhost:8000"
    echo "   - API Docs: http://localhost:8000/docs"
    echo ""
}

# Exécution
main() {
    check_requirements
    install_backend
    install_frontend
    install_mcp_servers
    setup_config
    show_instructions
}

main

