# 🛡️ Fraud Detection System

Application web complète de détection de fraude utilisant Machine Learning et règles métier.

## 📋 Table des Matières

- [Fonctionnalités](#fonctionnalités)
- [Architecture](#architecture)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Technologies](#technologies)
- [API Documentation](#api-documentation)
- [Algorithmes](#algorithmes)

## ✨ Fonctionnalités

### 📊 Dashboard
- Vue d'ensemble des statistiques clés
- Graphiques de l'évolution des transactions
- Taux de fraude en temps réel
- Montant total à risque

### 💳 Gestion des Transactions
- Import de données CSV
- Liste paginée avec filtres
- Détails de chaque transaction
- Score de risque individuel

### 🚨 Alertes
- Alertes de fraude en temps réel
- Classification par sévérité (Critical, High, Medium, Low)
- Validation manuelle (Confirmer/Rejeter)
- Historique des décisions

### 🔍 Analyse
- Upload CSV de transactions
- Analyse hybride (Règles + ML)
- Entraînement du modèle ML
- Configuration des paramètres

## 🏗️ Architecture

```
fraud-detection-app/
├── backend/                    # API FastAPI
│   ├── app/
│   │   ├── api/               # Endpoints REST
│   │   │   ├── transactions.py
│   │   │   ├── analysis.py
│   │   │   ├── alerts.py
│   │   │   └── stats.py
│   │   ├── services/          # Logique métier
│   │   │   ├── fraud_analyzer.py
│   │   │   ├── rule_detector.py
│   │   │   └── ml_detector.py
│   │   ├── database/          # Modèles DB
│   │   │   ├── database.py
│   │   │   └── models.py
│   │   └── schemas/           # Schémas Pydantic
│   │       └── schemas.py
│   ├── ml_models/             # Modèles ML sauvegardés
│   ├── generate_data.py       # Générateur de données
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/                   # Interface React
│   ├── src/
│   │   ├── pages/             # Pages principales
│   │   │   ├── Dashboard.js
│   │   │   ├── Transactions.js
│   │   │   ├── Alerts.js
│   │   │   └── Analysis.js
│   │   ├── services/          # API calls
│   │   │   └── api.js
│   │   ├── App.js
│   │   └── index.js
│   ├── package.json
│   └── Dockerfile
│
├── data/                       # Datasets
│   ├── raw/                   # CSV bruts
│   └── processed/             # Données traitées
│
└── docker-compose.yml         # Orchestration
```

## 🚀 Installation

### Prérequis

- Docker & Docker Compose
- Python 3.11+ (pour développement local)
- Node.js 18+ (pour développement local)

### Méthode 1: Docker (Recommandé)

```bash
# Cloner le projet
cd fraud-detection-app

# Générer les données de test
cd backend
python generate_data.py
cd ..

# Lancer l'application
docker-compose up --build
```

L'application sera accessible sur:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Méthode 2: Installation Locale

#### Backend

```bash
cd backend

# Créer environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Installer dépendances
pip install -r requirements.txt

# Générer les données
python generate_data.py

# Lancer le serveur
uvicorn main:app --reload --port 8000
```

#### Frontend

```bash
cd frontend

# Installer dépendances
npm install

# Lancer l'application
npm start
```

#### Base de données PostgreSQL

```bash
# Avec Docker
docker run -d \
  --name fraud-db \
  -e POSTGRES_USER=fraud_user \
  -e POSTGRES_PASSWORD=fraud_password \
  -e POSTGRES_DB=fraud_detection_db \
  -p 5432:5432 \
  postgres:16-alpine
```

## 📖 Utilisation

### 1. Importer des Données

1. Aller sur la page **Analyse**
2. Cliquer sur "Choisir un fichier CSV"
3. Sélectionner un fichier (ex: `data/raw/transactions_medium.csv`)
4. Cliquer sur "Importer"

Format CSV requis:
```csv
transaction_id,user_id,amount,timestamp,merchant,category,location
TXN_001,USER_001,45.99,2024-01-15 14:30:00,Amazon,Shopping,Paris, FR
```

### 2. Analyser les Transactions

1. Configurer les options (Règles + ML)
2. Cliquer sur "Lancer l'Analyse"
3. Consulter les résultats

### 3. Entraîner le Modèle ML

1. Importer au moins 100 transactions
2. Cliquer sur "Entraîner le Modèle ML"
3. Attendre la fin de l'entraînement
4. Le modèle sera automatiquement sauvegardé

### 4. Gérer les Alertes

1. Aller sur la page **Alertes**
2. Filtrer par statut/sévérité
3. Cliquer sur "Confirmer Fraude" ou "Rejeter"

## 🛠️ Technologies

### Backend
- **FastAPI** - Framework web Python moderne
- **SQLAlchemy** - ORM pour PostgreSQL
- **Scikit-learn** - Machine Learning
- **Pandas** - Manipulation de données
- **Pydantic** - Validation de données

### Frontend
- **React** - Library UI
- **Recharts** - Graphiques interactifs
- **Axios** - Requêtes HTTP
- **React Router** - Navigation

### Infrastructure
- **PostgreSQL** - Base de données relationnelle
- **Docker** - Conteneurisation
- **Docker Compose** - Orchestration

## 📡 API Documentation

### Endpoints Principaux

#### Transactions

```bash
# Upload CSV
POST /api/transactions/upload-csv
Content-Type: multipart/form-data

# Liste transactions
GET /api/transactions?skip=0&limit=100&user_id=USER_001

# Détail transaction
GET /api/transactions/{transaction_id}
```

#### Analyse

```bash
# Analyser transactions
POST /api/analysis/analyze
{
  "use_rules": true,
  "use_ml": true,
  "transaction_ids": ["TXN_001", "TXN_002"]  // optionnel
}

# Entraîner modèle
POST /api/analysis/train-model?min_transactions=100

# Info modèle
GET /api/analysis/model-info
```

#### Alertes

```bash
# Liste alertes
GET /api/alerts?status=pending&severity=critical

# Mettre à jour alerte
PUT /api/alerts/{alert_id}
{
  "status": "confirmed",
  "reviewed_by": "Admin"
}
```

#### Statistiques

```bash
# Stats globales
GET /api/stats

# Stats quotidiennes (30 jours)
GET /api/stats/daily?days=30

# Stats par catégorie
GET /api/stats/by-category
```

## 🧠 Algorithmes

### 1. Détection par Règles

**Règles implémentées:**
- ✅ Montant élevé (> 1000€) - Poids: 30%
- ✅ Heure inhabituelle (23h-6h) - Poids: 20%
- ✅ Fréquence élevée (>5 trans/heure) - Poids: 25%
- ✅ Localisation inhabituelle - Poids: 15%
- ✅ Déviation du montant (>3 écarts-types) - Poids: 10%

**Score final:** Somme pondérée des règles déclenchées

### 2. Machine Learning - Isolation Forest

**Principe:**
- Détection d'anomalies non supervisée
- Isole les points suspects dans l'espace des features
- Score basé sur la profondeur de l'arbre nécessaire pour isoler un point

**Features utilisées:**
- `amount` - Montant de la transaction
- `hour` - Heure de la journée
- `day_of_week` - Jour de la semaine
- `is_weekend` - Weekend (0/1)
- `transaction_count_last_hour` - Nombre de transactions récentes

**Paramètres:**
- Contamination: 10% (taux de fraude attendu)
- N_estimators: 100 arbres
- Random_state: 42 (reproductibilité)

### 3. Score Hybride

```
Score Final = 0.4 × Score_Règles + 0.6 × Score_ML
```

**Sévérité:**
- Critical: score ≥ 0.75
- High: 0.55 ≤ score < 0.75
- Medium: 0.35 ≤ score < 0.55
- Low: score < 0.35

## 📊 Données de Test

Le script `generate_data.py` crée 3 datasets:

| Dataset | Transactions | Taux Fraude | Fichier |
|---------|--------------|-------------|---------|
| Small   | 500          | 5%          | transactions_small.csv |
| Medium  | 2000         | 8%          | transactions_medium.csv |
| Large   | 5000         | 10%         | transactions_large.csv |

**Types de fraudes injectées:**
- Montants anormalement élevés
- Transactions nocturnes
- Haute fréquence (rafale de transactions)
- Localisations étrangères suspectes
- Combinaisons multiples

## 🎯 Impact CV

### Compétences Démontrées

**Data Engineering:**
- Pipeline ETL (CSV → PostgreSQL)
- Nettoyage et validation de données
- Gestion de volumes importants

**Machine Learning:**
- Isolation Forest pour détection d'anomalies
- Feature engineering (temporel, comportemental)
- Évaluation de modèles (précision, rappel, F1)

**Backend Development:**
- API REST avec FastAPI
- Architecture modulaire (services, repositories)
- Validation avec Pydantic

**Frontend Development:**
- Interface réactive avec React
- Visualisations avec Recharts
- Communication API avec Axios

**DevOps:**
- Dockerisation complète
- Orchestration avec Docker Compose
- Variables d'environnement

**Analyse Décisionnelle:**
- Règles métier configurables
- Scoring multi-critères
- Système d'alertes par sévérité

## 🔮 Évolutions Futures

- [ ] Analyse en temps réel avec WebSocket
- [ ] Ré-entraînement automatique périodique
- [ ] Détection de patterns complexes (réseaux de neurones)
- [ ] Export PDF des rapports
- [ ] Intégration avec systèmes bancaires (API)
- [ ] Dashboard temps réel avec rafraîchissement auto
- [ ] Tests unitaires et d'intégration
- [ ] CI/CD avec GitHub Actions
- [ ] Déploiement cloud (AWS/GCP/Azure)

## 📝 Licence

Ce projet est un projet éducatif à des fins de portfolio.

## 👤 Auteur

Créé dans le cadre d'un projet de portfolio pour démontrer des compétences en développement full-stack et machine learning.

---

**Note:** Les données générées sont entièrement synthétiques et ne représentent aucune transaction réelle.
