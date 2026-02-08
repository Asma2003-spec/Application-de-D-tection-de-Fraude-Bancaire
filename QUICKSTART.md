# 🚀 Guide de Démarrage Rapide

## Installation en 5 minutes

### 1️⃣ Prérequis
```bash
# Vérifier Docker
docker --version
docker-compose --version
```

### 2️⃣ Générer les données de test
```bash
cd backend
python generate_data.py
cd ..
```

### 3️⃣ Lancer l'application
```bash
docker-compose up --build
```

### 4️⃣ Accéder à l'application
- **Frontend:** http://localhost:3000
- **API:** http://localhost:8000
- **Documentation API:** http://localhost:8000/docs

---

## 📝 Premier Test

### Étape 1: Importer des données
1. Ouvrir http://localhost:3000
2. Aller sur **Analyse**
3. Sélectionner `data/raw/transactions_medium.csv`
4. Cliquer sur **Importer**

### Étape 2: Analyser
1. Activer "Détection par règles"
2. Cliquer sur **Lancer l'Analyse**
3. Observer les résultats

### Étape 3: Consulter
1. Aller sur **Dashboard** → Voir les statistiques
2. Aller sur **Transactions** → Liste complète
3. Aller sur **Alertes** → Gérer les fraudes détectées

### Étape 4: Entraîner le ML
1. Retour sur **Analyse**
2. Cliquer sur **Entraîner le Modèle ML**
3. Attendre 30-60 secondes
4. Relancer une analyse avec ML activé

---

## 🎯 Scénarios d'utilisation

### Scénario 1: Analyse de nouvelles transactions
```bash
# 1. Préparer un CSV
# 2. L'importer via l'interface
# 3. Analyser avec règles + ML
# 4. Consulter les alertes
```

### Scénario 2: Améliorer le modèle
```bash
# 1. Importer plus de données
# 2. Ré-entraîner le modèle
# 3. Comparer les performances
```

### Scénario 3: Validation manuelle
```bash
# 1. Aller sur Alertes
# 2. Filtrer par "pending"
# 3. Confirmer ou rejeter chaque alerte
```

---

## 🔧 Commandes Utiles

### Docker
```bash
# Arrêter l'application
docker-compose down

# Voir les logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Redémarrer un service
docker-compose restart backend

# Nettoyer tout
docker-compose down -v
```

### Base de données
```bash
# Accéder à PostgreSQL
docker exec -it fraud_detection_db psql -U fraud_user -d fraud_detection_db

# Compter les transactions
SELECT COUNT(*) FROM transactions;

# Voir les fraudes
SELECT * FROM transactions WHERE is_fraud = true LIMIT 10;

# Stats par catégorie
SELECT category, COUNT(*), AVG(amount) 
FROM transactions 
GROUP BY category;
```

### Backend Python
```bash
# Tester l'API directement
curl http://localhost:8000/health

# Upload CSV via API
curl -X POST "http://localhost:8000/api/transactions/upload-csv" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@data/raw/transactions_small.csv"

# Analyser
curl -X POST "http://localhost:8000/api/analysis/analyze" \
  -H "Content-Type: application/json" \
  -d '{"use_rules": true, "use_ml": true}'
```

---

## ⚠️ Troubleshooting

### Problème: Port déjà utilisé
```bash
# Changer les ports dans docker-compose.yml
# Frontend: "3001:3000"
# Backend: "8001:8000"
```

### Problème: Base de données inaccessible
```bash
# Vérifier que PostgreSQL est bien démarré
docker-compose ps

# Recréer la base
docker-compose down -v
docker-compose up -d postgres
```

### Problème: Frontend ne charge pas
```bash
# Vérifier les logs
docker-compose logs frontend

# Rebuild
docker-compose up --build frontend
```

---

## 📚 Ressources

- **Documentation API:** http://localhost:8000/docs
- **Swagger UI:** http://localhost:8000/redoc
- **README principal:** ../README.md

---

**Bon développement! 🚀**
