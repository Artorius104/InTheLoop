# Makefile pour le projet de veille AI

.PHONY: install test run clean lint format

# Installation des dépendances
install:
	pip install -r requirements.txt

# Exécution des tests
test:
	pytest tests/ -v

# Lancement de l'application
run:
	python src/main.py

# Nettoyage des fichiers temporaires
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache/

# Vérification du code
lint:
	flake8 src/ tests/
	mypy src/

# Formatage du code
format:
	black src/ tests/

# Création des dossiers nécessaires
setup:
	mkdir -p data logs
	cp .env.example .env

# Installation complète
dev-setup: install setup
	@echo "Projet configuré pour le développement"