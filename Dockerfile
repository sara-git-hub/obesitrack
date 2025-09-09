# Utilise une image Python légère
FROM python:3.12-slim

# Définit le répertoire de travail
WORKDIR /app

# Empêche Python de créer des fichiers .pyc
ENV PYTHONDONTWRITEBYTECODE 1
# Force le flush du stdout/stderr (utile pour les logs Docker)
ENV PYTHONUNBUFFERED 1

# Installer les dépendances système (PostgreSQL client & build tools)
RUN apt-get update && apt-get install -y \
    libpq-dev gcc build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copier les fichiers requirements
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l’application
COPY . .

# Exposer le port utilisé par FastAPI
EXPOSE 8000

# Commande de lancement de l’app
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
