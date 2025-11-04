#!/bin/bash

# Script de démarrage pour le développement
# Lance le backend et le frontend simultanément

set -e

echo "🚀 Démarrage de InTheLoop (mode développement)"

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Fonction pour arrêter tous les processus au Ctrl+C
cleanup() {
    echo -e "\n${YELLOW}Arrêt des services...${NC}"
    pkill -P $$
    exit 0
}

trap cleanup SIGINT SIGTERM

# Vérifier que nous sommes dans le bon répertoire
if [ ! -f "README.md" ]; then
    echo -e "${RED}❌ Erreur: Exécutez ce script depuis la racine du projet${NC}"
    exit 1
fi

# Vérifier l'environnement Python
if [ ! -d "backend/venv" ]; then
    echo -e "${YELLOW}⚠️  Environnement virtuel Python non trouvé${NC}"
    echo "Création de l'environnement virtuel..."
    cd backend
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    cd ..
fi

# Vérifier les dépendances Node frontend
if [ ! -d "frontend/node_modules" ]; then
    echo -e "${YELLOW}⚠️  node_modules non trouvé pour le frontend${NC}"
    echo "Installation des dépendances..."
    cd frontend
    npm install
    cd ..
fi

# Créer le fichier .env s'il n'existe pas
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  Fichier .env non trouvé${NC}"
    if [ -f ".env.example" ]; then
        echo "Création du fichier .env depuis .env.example..."
        cp .env.example .env
        echo -e "${GREEN}✓ Fichier .env créé. N'oubliez pas de configurer vos clés API.${NC}"
    fi
fi

echo -e "\n${GREEN}✓ Vérifications terminées${NC}\n"

# Démarrer le backend
echo -e "${GREEN}🔧 Démarrage du backend (port 8000)...${NC}"
cd backend
source venv/bin/activate
uvicorn main:app --reload --port 8000 > ../logs/backend.log 2>&1 &
BACKEND_PID=$!
cd ..

# Attendre que le backend démarre
echo "Attente du démarrage du backend..."
for i in {1..30}; do
    if curl -s http://localhost:8000/api/health > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Backend démarré${NC}"
        break
    fi
    if [ $i -eq 30 ]; then
        echo -e "${RED}❌ Le backend n'a pas démarré dans les temps${NC}"
        cat logs/backend.log
        cleanup
        exit 1
    fi
    sleep 1
done

# Démarrer le frontend
echo -e "\n${GREEN}🎨 Démarrage du frontend (port 3000)...${NC}"
cd frontend
npm run dev > ../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

# Attendre que le frontend démarre
echo "Attente du démarrage du frontend..."
sleep 3

echo -e "\n${GREEN}✅ InTheLoop est prêt !${NC}\n"
echo "📊 Backend API: http://localhost:8000"
echo "📚 Documentation API: http://localhost:8000/docs"
echo "🌐 Frontend: http://localhost:3000"
echo -e "\n${YELLOW}Appuyez sur Ctrl+C pour arrêter tous les services${NC}\n"

# Afficher les logs en temps réel
tail -f logs/backend.log logs/frontend.log 2>/dev/null || wait

