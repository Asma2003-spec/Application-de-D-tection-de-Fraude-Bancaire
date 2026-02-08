# 🚀 Guide de Démarrage SANS Docker

## ⚠️ Utilisez cette méthode si Docker ne fonctionne pas

---

## 📋 Prérequis

- Python 3.11+ installé
- Node.js 18+ installé

---

## 🔧 Installation Étape par Étape

### **Étape 1 : Préparer le Backend**

```powershell
# Ouvrir le projet dans VSCode
cd fraud-detection-app

# Terminal 1 - Backend
cd backend

# Créer environnement virtuel
python -m venv venv

# Activer l'environnement
.\venv\Scripts\activate   # Windows PowerShell
# OU
venv\Scripts\activate.bat  # Windows CMD
# OU
source venv/bin/activate   # Linux/Mac

# Installer les dépendances
pip install -r requirements.txt
```

### **Étape 2 : Configurer SQLite (au lieu de PostgreSQL)**

```powershell
# Dans backend/app/database/
# Copier database_sqlite.py → database.py

# OU remplacer le contenu de database.py par :
```

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite - pas besoin de PostgreSQL
SQLALCHEMY_DATABASE_URL = "sqlite:///./fraud_detection.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### **Étape 3 : Lancer le Backend**

```powershell
# Toujours dans backend/ avec venv activé
uvicorn main:app --reload
```

**Résultat attendu :**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

✅ **Backend prêt !** → http://localhost:8000/docs

---

### **Étape 4 : Lancer le Frontend**

```powershell
# Ouvrir un NOUVEAU terminal dans VSCode (Ctrl + Shift + `)
cd frontend

# Installer les dépendances
npm install

# Lancer l'application
npm start
```

**Résultat attendu :**
```
Compiled successfully!
Local:            http://localhost:3000
```

✅ **Frontend prêt !** → http://localhost:3000

---

## 🎯 Test Rapide

### **1. Vérifier le Backend**

Ouvrir : http://localhost:8000/health

Résultat : `{"status": "healthy"}`

### **2. Tester l'Interface**

1. Ouvrir http://localhost:3000
2. Aller sur **Analyse**
3. Sélectionner `backend/data/raw/transactions_medium.csv`
4. Cliquer **Importer**

✅ Devrait afficher : "2072 transactions créées"

### **3. Lancer une Analyse**

1. Activer "Détection par règles"
2. Cliquer **Lancer l'Analyse**
3. Consulter les résultats

---

## ❌ Dépannage

### Erreur : `Module not found`
```powershell
# Vérifier que venv est activé
# Vous devez voir (venv) au début de la ligne de commande
.\venv\Scripts\activate

# Réinstaller
pip install -r requirements.txt
```

### Erreur : `Port already in use`
```powershell
# Backend sur un autre port
uvicorn main:app --reload --port 8001

# Puis modifier frontend/src/services/api.js :
# const API_URL = 'http://localhost:8001';
```

### Erreur : `npm not found`
```powershell
# Installer Node.js
https://nodejs.org/
```

### Base de données vide
```powershell
# Supprimer et recréer
cd backend
rm fraud_detection.db
uvicorn main:app --reload
# La DB sera recréée automatiquement
```

---

## 📊 Données de Test

Les fichiers CSV sont dans :
```
backend/data/raw/
├── transactions_small.csv    (515 transactions)
├── transactions_medium.csv   (2072 transactions)
└── transactions_large.csv    (5306 transactions)
```

---

## 🎓 Commandes Utiles

```powershell
# Arrêter le backend : Ctrl + C
# Arrêter le frontend : Ctrl + C

# Désactiver venv
deactivate

# Voir les logs backend
# Visible directement dans le terminal

# Tester l'API
http://localhost:8000/docs  # Swagger UI interactif
```

---

## ✅ Checklist de Démarrage

- [ ] Python 3.11+ installé
- [ ] Node.js 18+ installé
- [ ] Backend : venv créé et activé
- [ ] Backend : dépendances installées
- [ ] Backend : database.py modifié pour SQLite
- [ ] Backend : uvicorn lancé (port 8000)
- [ ] Frontend : npm install exécuté
- [ ] Frontend : npm start lancé (port 3000)
- [ ] Test : http://localhost:3000 accessible
- [ ] Test : Import CSV fonctionne

---

**Bon développement ! 🚀**
