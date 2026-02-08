   Système de Détection de Fraude Bancaire
                                                                   
Application web full-stack de détection automatique de fraudes bancaires utilisant Machine Learning (Isolation Forest) et règles métier. Développée avec Python/FastAPI pour le backend et React pour le frontend.

## Description
Cette application analyse automatiquement les transactions bancaires pour détecter les comportements frauduleux en utilisant :
- **Machine Learning** : Algorithme Isolation Forest pour détecter les anomalies
- **Règles métier** : Analyse des montants élevés, heures inhabituelles, fréquences anormales
- **Scoring hybride** : Combinaison des deux approches pour maximiser la précision

### Fonctionnalités principales
- Dashboard analytique avec KPIs et graphiques interactifs
-  Import et analyse de transactions via CSV
-  Détection multi-critères (montant, heure, localisation, fréquence)
-  Entraînement du modèle Machine Learning
-  Système d'alertes avec validation manuelle
-  Visualisations de données avec Recharts

###  Technologies Utilisées

**Backend**
- Python 3.14
- FastAPI - Framework API REST moderne
- SQLAlchemy - ORM pour la base de données
- Scikit-learn - Machine Learning (Isolation Forest)
- Pandas - Manipulation de données
- Pydantic - Validation de données

**Frontend**
- React 18 - Interface utilisateur
- Recharts - Visualisation de données
- Axios - Communication avec l'API
- React Router - Navigation

**Base de données**
- SQLite - Base de données relationnelle légère

**Conteneurisation** (optionnel)
- Docker & Docker Compose - Configuration fournie pour déploiement

### 🧠 Algorithmes de Détection

#### 1. Détection par Règles (40% du score)
- Montant élevé (> 1000€)
- Heure inhabituelle (23h-6h)
- Haute fréquence (>5 transactions/heure)
- Déviation statistique (>3 écarts-types)

#### 2. Machine Learning (60% du score)
- **Modèle** : Isolation Forest
- **Approche** : Détection d'anomalies non-supervisée
- **Features** : montant, heure, jour de semaine, fréquence

Score_Final = 0.4 × Score_Règles + 0.6 × Score_ML


###  Données de Test
Inclus : 3 datasets synthétiques générés (500, 2000, 5000 transactions)
### Compétences Techniques Démontrées

   **Développement Full-Stack** : Backend Python + Frontend React  
   **Machine Learning** : Isolation Forest, feature engineering  
   **API REST** : Conception et documentation (FastAPI)  
   **Base de données** : Modélisation et requêtes SQL (SQLAlchemy)  
   **Visualisation de données** : Graphiques interactifs  
   **Architecture logicielle** : Séparation des responsabilités (services, API, DB)
