#!/bin/bash

# Backend structure
mkdir -p backend/app/{api,models,services,database,utils,schemas}
mkdir -p backend/tests
mkdir -p backend/ml_models

# Frontend structure
mkdir -p frontend/src/{components,pages,services,utils,assets}
mkdir -p frontend/public

# Data directories
mkdir -p data/{raw,processed,models}

# Docs
mkdir -p docs

echo "✅ Structure créée avec succès!"
