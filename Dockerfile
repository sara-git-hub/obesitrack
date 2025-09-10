# Utilise une image Python légère
FROM python:3.12-slim

# Définit le répertoire de travail
WORKDIR /app

# Empêche Python de créer des fichiers .pyc
ENV PYTHONDONTWRITEBYTECODE 1
# Force le flush du stdout/stderr (utile pour les logs Docker)
ENV PYTHONUNBUFFERED 1

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    libpq-dev gcc build-essential \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Copier les fichiers requirements
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Créer le dossier static et télécharger Chart.js
RUN mkdir -p static/js && \
    wget -O static/js/chart.js https://cdn.jsdelivr.net/npm/chart.js/dist/chart.umd.js

# Copier le code de l'application
COPY . .

# Vérification que Chart.js est présent
RUN if [ ! -f "static/js/chart.js" ]; then echo "ERREUR: Chart.js non téléchargé"; exit 1; fi

# Exposer le port utilisé par FastAPI
EXPOSE 8000

# Commande de lancement de l'app
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]