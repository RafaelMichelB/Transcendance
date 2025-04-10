# Étape 1: Utiliser l'image officielle Python comme base
FROM python:3.10-slim

RUN apt-get update && apt-get install -y curl
# Étape 2: Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Étape 3: Copier les fichiers nécessaires dans le conteneur
# Copier le fichier requirements.txt et l'application FastAPI (si tu en as un)
COPY BackendTest/requirements.txt .

# Étape 4: Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Étape 6: Exposer le port 8000 pour l'application FastAPI
EXPOSE 8000

# Étape 7: Commande pour démarrer le serveur FastAPI avec Uvicorn
CMD ["uvicorn", "backend:app", "--host", "0.0.0.0", "--port", "8000"]

