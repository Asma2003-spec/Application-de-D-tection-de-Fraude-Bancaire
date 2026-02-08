from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta

from app.database.database import get_db
from app.database import models
from app.schemas.schemas import StatsResponse

router = APIRouter()

@router.get("/", response_model=StatsResponse)
async def get_statistics(
    db: Session = Depends(get_db)
):
    """
    Récupère les statistiques globales
    """
    # Total transactions
    total_transactions = db.query(func.count(models.Transaction.id)).scalar()
    
    # Total fraudes
    total_frauds = db.query(func.count(models.Transaction.id)).filter(
        models.Transaction.is_fraud == True
    ).scalar()
    
    # Taux de fraude
    fraud_rate = (total_frauds / total_transactions * 100) if total_transactions > 0 else 0
    
    # Total alertes
    total_alerts = db.query(func.count(models.Alert.id)).scalar()
    
    # Alertes en attente
    pending_alerts = db.query(func.count(models.Alert.id)).filter(
        models.Alert.status == 'pending'
    ).scalar()
    
    # Fraudes confirmées
    confirmed_frauds = db.query(func.count(models.Alert.id)).filter(
        models.Alert.status == 'confirmed'
    ).scalar()
    
    # Montant total à risque
    total_amount_at_risk = db.query(func.sum(models.Transaction.amount)).filter(
        models.Transaction.is_fraud == True
    ).scalar() or 0.0
    
    return StatsResponse(
        total_transactions=total_transactions or 0,
        total_frauds=total_frauds or 0,
        fraud_rate=round(fraud_rate, 2),
        total_alerts=total_alerts or 0,
        pending_alerts=pending_alerts or 0,
        confirmed_frauds=confirmed_frauds or 0,
        total_amount_at_risk=round(total_amount_at_risk, 2)
    )


@router.get("/daily")
async def get_daily_stats(
    days: int = 30,
    db: Session = Depends(get_db)
):
    """
    Récupère les statistiques quotidiennes
    """
    # Date de début
    start_date = datetime.now() - timedelta(days=days)
    
    # Transactions par jour
    daily_transactions = db.query(
        func.date(models.Transaction.timestamp).label('date'),
        func.count(models.Transaction.id).label('count'),
        func.sum(models.Transaction.amount).label('total_amount')
    ).filter(
        models.Transaction.timestamp >= start_date
    ).group_by(
        func.date(models.Transaction.timestamp)
    ).all()
    
    # Fraudes par jour
    daily_frauds = db.query(
        func.date(models.Transaction.timestamp).label('date'),
        func.count(models.Transaction.id).label('count'),
        func.sum(models.Transaction.amount).label('total_amount')
    ).filter(
        models.Transaction.timestamp >= start_date,
        models.Transaction.is_fraud == True
    ).group_by(
        func.date(models.Transaction.timestamp)
    ).all()
    
    # Formater les résultats
    transactions_data = [
        {
            'date': str(item.date),
            'count': item.count,
            'total_amount': float(item.total_amount) if item.total_amount else 0.0
        }
        for item in daily_transactions
    ]
    
    frauds_data = [
        {
            'date': str(item.date),
            'count': item.count,
            'total_amount': float(item.total_amount) if item.total_amount else 0.0
        }
        for item in daily_frauds
    ]
    
    return {
        'transactions': transactions_data,
        'frauds': frauds_data
    }


@router.get("/by-category")
async def get_stats_by_category(
    db: Session = Depends(get_db)
):
    """
    Statistiques par catégorie
    """
    stats = db.query(
        models.Transaction.category,
        func.count(models.Transaction.id).label('total'),
        func.sum(models.Transaction.is_fraud.cast(db.bind.dialect.BIGINT)).label('frauds'),
        func.avg(models.Transaction.amount).label('avg_amount')
    ).filter(
        models.Transaction.category.isnot(None)
    ).group_by(
        models.Transaction.category
    ).all()
    
    return [
        {
            'category': item.category,
            'total_transactions': item.total,
            'total_frauds': item.frauds or 0,
            'fraud_rate': round((item.frauds or 0) / item.total * 100, 2) if item.total > 0 else 0,
            'average_amount': round(float(item.avg_amount), 2) if item.avg_amount else 0.0
        }
        for item in stats
    ]


@router.get("/by-severity")
async def get_stats_by_severity(
    db: Session = Depends(get_db)
):
    """
    Statistiques des alertes par sévérité
    """
    stats = db.query(
        models.Alert.severity,
        func.count(models.Alert.id).label('count')
    ).group_by(
        models.Alert.severity
    ).all()
    
    return [
        {
            'severity': item.severity,
            'count': item.count
        }
        for item in stats
    ]
