from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.database.database import get_db
from app.database import models
from app.schemas.schemas import AlertResponse, AlertUpdate

router = APIRouter()

@router.get("/", response_model=List[AlertResponse])
async def get_alerts(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    severity: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Récupère la liste des alertes
    """
    query = db.query(models.Alert)
    
    if status:
        query = query.filter(models.Alert.status == status)
    
    if severity:
        query = query.filter(models.Alert.severity == severity)
    
    alerts = query.order_by(models.Alert.created_at.desc()).offset(skip).limit(limit).all()
    
    return alerts


@router.get("/{alert_id}", response_model=AlertResponse)
async def get_alert(
    alert_id: int,
    db: Session = Depends(get_db)
):
    """
    Récupère une alerte par son ID
    """
    alert = db.query(models.Alert).filter(models.Alert.id == alert_id).first()
    
    if not alert:
        raise HTTPException(status_code=404, detail="Alerte non trouvée")
    
    return alert


@router.put("/{alert_id}", response_model=AlertResponse)
async def update_alert(
    alert_id: int,
    update: AlertUpdate,
    db: Session = Depends(get_db)
):
    """
    Met à jour le statut d'une alerte
    """
    alert = db.query(models.Alert).filter(models.Alert.id == alert_id).first()
    
    if not alert:
        raise HTTPException(status_code=404, detail="Alerte non trouvée")
    
    # Valider le statut
    valid_statuses = ['pending', 'confirmed', 'rejected']
    if update.status not in valid_statuses:
        raise HTTPException(
            status_code=400,
            detail=f"Statut invalide. Valeurs acceptées: {', '.join(valid_statuses)}"
        )
    
    # Mettre à jour
    alert.status = update.status
    alert.reviewed_by = update.reviewed_by
    alert.reviewed_at = datetime.now()
    alert.updated_at = datetime.now()
    
    db.commit()
    db.refresh(alert)
    
    return alert


@router.delete("/{alert_id}")
async def delete_alert(
    alert_id: int,
    db: Session = Depends(get_db)
):
    """
    Supprime une alerte
    """
    alert = db.query(models.Alert).filter(models.Alert.id == alert_id).first()
    
    if not alert:
        raise HTTPException(status_code=404, detail="Alerte non trouvée")
    
    db.delete(alert)
    db.commit()
    
    return {"message": "Alerte supprimée"}


@router.get("/transaction/{transaction_id}", response_model=List[AlertResponse])
async def get_alerts_by_transaction(
    transaction_id: str,
    db: Session = Depends(get_db)
):
    """
    Récupère toutes les alertes pour une transaction
    """
    alerts = db.query(models.Alert).filter(
        models.Alert.transaction_id == transaction_id
    ).all()
    
    return alerts
