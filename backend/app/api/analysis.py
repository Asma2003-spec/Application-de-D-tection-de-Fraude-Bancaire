from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.database.database import get_db
from app.database import models
from app.schemas.schemas import AnalysisRequest, AnalysisResponse
from app.services.fraud_analyzer import FraudAnalyzer
import os

router = APIRouter()

# Initialiser l'analyseur
MODEL_PATH = "ml_models/fraud_model.pkl"
analyzer = FraudAnalyzer(
    ml_model_path=MODEL_PATH if os.path.exists(MODEL_PATH) else None
)

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_transactions(
    request: AnalysisRequest,
    db: Session = Depends(get_db)
):
    """
    Analyse des transactions pour détecter les fraudes
    """
    # Récupérer les transactions à analyser
    if request.transaction_ids:
        transactions = db.query(models.Transaction).filter(
            models.Transaction.transaction_id.in_(request.transaction_ids)
        ).all()
    else:
        # Analyser toutes les transactions non analysées
        transactions = db.query(models.Transaction).filter(
            models.Transaction.risk_score == 0.0
        ).all()
    
    if not transactions:
        raise HTTPException(status_code=404, detail="Aucune transaction à analyser")
    
    # Convertir en dict pour l'analyse
    trans_dicts = [
        {
            'transaction_id': t.transaction_id,
            'amount': t.amount,
            'timestamp': t.timestamp,
            'merchant': t.merchant,
            'category': t.category,
            'location': t.location,
            'user_id': t.user_id
        }
        for t in transactions
    ]
    
    # Analyser
    analysis_result = analyzer.analyze_transactions(
        trans_dicts,
        use_rules=request.use_rules,
        use_ml=request.use_ml
    )
    
    # Mettre à jour les transactions et créer les alertes
    alerts_created = 0
    
    for result in analysis_result['results']:
        # Mettre à jour la transaction
        transaction = db.query(models.Transaction).filter(
            models.Transaction.transaction_id == result['transaction_id']
        ).first()
        
        if transaction:
            transaction.risk_score = result['score']
            transaction.is_fraud = result['is_fraud']
            transaction.fraud_type = result['fraud_type']
            transaction.updated_at = datetime.now()
            
            # Créer une alerte si fraude détectée
            if result['is_fraud']:
                alert = models.Alert(
                    transaction_id=result['transaction_id'],
                    alert_type=result['fraud_type'],
                    risk_score=result['score'],
                    severity=result['severity'],
                    reason='; '.join(result['reasons']),
                    status='pending'
                )
                db.add(alert)
                alerts_created += 1
    
    db.commit()
    
    return AnalysisResponse(
        total_analyzed=analysis_result['stats']['total_analyzed'],
        frauds_detected=analysis_result['stats']['frauds_detected'],
        average_risk_score=analysis_result['stats']['average_risk_score'],
        alerts_created=alerts_created,
        processing_time=analysis_result['stats']['processing_time']
    )


@router.post("/train-model")
async def train_model(
    min_transactions: int = 100,
    db: Session = Depends(get_db)
):
    """
    Entraîne le modèle ML sur les données existantes
    """
    # Récupérer toutes les transactions
    transactions = db.query(models.Transaction).all()
    
    if len(transactions) < min_transactions:
        raise HTTPException(
            status_code=400,
            detail=f"Minimum {min_transactions} transactions requises pour l'entraînement"
        )
    
    # Convertir en dict
    trans_dicts = [
        {
            'transaction_id': t.transaction_id,
            'amount': t.amount,
            'timestamp': t.timestamp,
            'user_id': t.user_id,
            'merchant': t.merchant,
            'category': t.category,
            'location': t.location
        }
        for t in transactions
    ]
    
    try:
        # Entraîner
        metrics = analyzer.train_ml_model(trans_dicts)
        
        # Sauvegarder
        os.makedirs('ml_models', exist_ok=True)
        analyzer.save_ml_model(MODEL_PATH)
        
        # Enregistrer dans la DB
        ml_model = models.MLModel(
            model_name="IsolationForest",
            model_type="isolation_forest",
            version="1.0",
            is_active=True,
            model_path=MODEL_PATH
        )
        
        # Désactiver les anciens modèles
        db.query(models.MLModel).update({'is_active': False})
        
        db.add(ml_model)
        db.commit()
        
        return {
            "message": "Modèle entraîné avec succès",
            "metrics": metrics,
            "model_path": MODEL_PATH
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'entraînement: {str(e)}")


@router.get("/model-info")
async def get_model_info():
    """
    Retourne les informations sur les modèles
    """
    return analyzer.get_model_info()
