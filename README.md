# 🏥 ObesiTrack - Système de Classification d'Obésité

ObesiTrack est une application web intelligente qui utilise l'IA pour classifier les niveaux d'obésité basés sur des données de santé. Développé avec FastAPI, JavaScript et des modèles de machine learning.

## ✨ Fonctionnalités

### 👤 Pour les utilisateurs
- **🔐 Authentification sécurisée** (JWT tokens)
- **📊 Prédictions en temps réel** de classification d'obésité
- **📋 Historique personnel** des prédictions avec visualisations graphiques
- **👤 Gestion de profil** et données personnelles

### ⚙️ Pour les administrateurs
- **📈 Dashboard admin** avec statistiques détaillées et graphiques Chart.js
- **👥 Gestion des utilisateurs** (création, modification, suppression)
- **🗑️ Gestion des prédictions** (consultation, suppression)
- **📊 Tableaux interactifs** avec filtres et actions

## 🛠️ Technologies utilisées

### Backend
- **Python 3.12** avec FastAPI
- **SQLAlchemy** + PostgreSQL
- **JWT** pour l'authentification
- **Scikit-learn** pour le modèle ML
- **Pydantic** pour la validation des données
- **Jinja2** pour les templates HTML

### Frontend
- **HTML5/CSS3/JavaScript** vanilla
- **Chart.js** pour les visualisations graphiques
- **Templates Jinja2** dynamiques

### Infrastructure
- **Docker** + Docker Compose
- **PostgreSQL** base de données
- **Architecture modulaire** et scalable

## 🏗️ Architecture du projet

```bash
obesitrack/
├── api/ # Code de l'API FastAPI
│ ├── main.py # Point d'entrée de l'application
│ ├── deps.py # Dépendances (DB, auth)
│ ├── models.py # Modèles SQLAlchemy
│ ├── schemas.py # Schémas Pydantic
│ ├── security.py # Utilitaires de sécurité
│ ├── config.py # Configuration
│ └── routes/ # Routes de l'API
│ ├── auth.py # Authentification
│ ├── predictions.py # Prédictions
│ ├── web.py # Pages web
│ ├── admin_web.py # Pages web admin
│ └── admin.py # Administration
├── core/
│ └── templates.py # Initialiser Jinja2
├── ml/ # Modèle de Machine Learning
│ ├── train.py # Script d'entraînement
│ ├── data/ # Données d'entraînement
│ └── model_artifacts/ # Modèle entraîné
├── static/ # Fichiers statiques
│ ├── css/ # Styles CSS
│ └── js/ # JavaScript
│ ├── app.js # Logique applicative
│ └── chart.js # Library Chart.js (local)
├── templates/ # Templates Jinja2
│ ├── users.html # Gestion utilisateurs
│ ├── base.html # Template de base
│ ├── history.html # Historique des prédictions
│ ├── index.html # Page d'accueil
│ ├── login.html # Page de connexion
│ ├── prediction.html # Formulaire de prédiction
│ ├── predictions.html # Liste des prédictions
│ ├── recent_predictions.html # Prédictions récentes (admin)
│ └── register.html # Page d'inscription
├── tests/ # Tests unitaires
├── docker-compose.yml # Configuration Docker Compose
├── Dockerfile # Image Docker de l'application
├── requirements.txt # Dépendances Python
└── README.md # Documentation
```

text

## 🚀 Installation et déploiement

### Prérequis
- Docker et Docker Compose
- Git

### 1. Cloner le projet

```bash
git clone https://github.com/sara-git-hub/obesitrack.git
cd obesitrack
```

2. Configuration de l'environnement

Éditer .env avec vos configurations :

.env
DATABASE_URL=postgresql://user:password@db:5432/obesitrack
SECRET_KEY=votre-secret-key-super-securisee
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

3. Démarrage avec Docker

```bash
docker-compose up -d --build
```

4. Accès à l'application
Application : http://localhost:8000

API Documentation : http://localhost:8000/docs

Admin Dashboard : http://localhost:8000/admin

5. Arrêt de l'application
```bash
docker-compose down
```


🎯 Utilisation
1. Création de compte
Visitez http://localhost:8000/auth/register pour créer un compte.

2. Connexion
Connectez-vous sur http://localhost:8000/auth/login

3. Effectuer une prédiction
Rendez-vous sur http://localhost:8000/web/predict et remplissez le formulaire.

4. Consulter l'historique
Visualisez vos prédictions sur http://localhost:8000/web/history

5. Administration
Accédez au dashboard admin sur http://localhost:8000/admin_web/dashboard (compte admin requis)

🧠 Modèle de Machine Learning
Le modèle utilise un classificateur Gradient Boosting entraîné pour prédire 7 niveaux d'obésité :

Insuffisance pondérale

Poids normal

Surpoids niveau I

Surpoids niveau II

Obésité type I

Obésité type II

Obésité type III

Entraînement du modèle

python train.py

🔒 Sécurité
JWT Authentication avec tokens sécurisés

Password hashing avec bcrypt

Validation des données avec Pydantic

Protection des routes admin
``
🛠️ Développement
Installation pour le développement

python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

pip install -r requirements.txt
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000