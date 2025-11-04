#!/bin/bash

# Script de démarrage rapide pour InTheLoop

echo "🚀 Démarrage de InTheLoop"
echo "=========================="
echo ""

# Couleurs
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

# Démarrer le backend en arrière-plan
echo -e "${BLUE}📡 Démarrage du backend...${NC}"
cd backend
source venv/bin/activate
uvicorn main:app --reload --port 8000 > ../backend.log 2>&1 &
BACKEND_PID=$!
cd ..

# Attendre que le backend démarre
sleep 3

# Démarrer le frontend Streamlit
echo -e "${GREEN}🎨 Démarrage du frontend Streamlit...${NC}"
cd backend
source venv/bin/activate
streamlit run ../frontend/app.py --server.port 3000

# Cleanup au Ctrl+C
trap "kill $BACKEND_PID" EXIT

