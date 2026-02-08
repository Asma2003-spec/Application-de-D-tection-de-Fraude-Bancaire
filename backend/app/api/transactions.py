from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import pandas as pd
import io
from datetime import datetime

from app.database.database import get_db
from app.database import models
from app.schemas.schemas import TransactionResponse, TransactionCreate

router = APIRouter()

@router.post("/upload-csv")
async def upload_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload un fichier CSV de transactions
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Le fichier doit être au format CSV")
    
    try:
        # Lire le CSV
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        
        # Valider les colonnes requises
        required_columns = ['transaction_id', 'amount', 'timestamp', 'user_id']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            raise HTTPException(
                status_code=400, 
                detail=f"Colonnes manquantes: {', '.join(missing_columns)}"
            )
        
        # Convertir timestamp
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Insérer dans la DB
        transactions_created = 0
        transactions_skipped = 0
        
        for _, row in df.iterrows():
            # Vérifier si existe déjà
            existing = db.query(models.Transaction).filter(
                models.Transaction.transaction_id == row['transaction_id']
            ).first()
            
            if existing:
                transactions_skipped += 1
                continue
            
            transaction = models.Transaction(
                transaction_id=row['transaction_id'],
                amount=float(row['amount']),
                timestamp=row['timestamp'],
                user_id=row['user_id'],
                merchant=row.get('merchant'),
                category=row.get('category'),
                location=row.get('location')
            )
            
            db.add(transaction)
            transactions_created += 1
        
        db.commit()
        
        return {
            "message": "Fichier importé avec succès",
            "transactions_created": transactions_created,
            "transactions_skipped": transactions_skipped,
            "total_rows": len(df)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'import: {str(e)}")


@router.get("/", response_model=List[TransactionResponse])
async def get_transactions(
    skip: int = 0,
    limit: int = 100,
    user_id: str = None,
    is_fraud: bool = None,
    db: Session = Depends(get_db)
):
    """
    Récupère la liste des transactions avec pagination
    """
    query = db.query(models.Transaction)
    
    if user_id:
        query = query.filter(models.Transaction.user_id == user_id)
    
    if is_fraud is not None:
        query = query.filter(models.Transaction.is_fraud == is_fraud)
    
    transactions = query.order_by(models.Transaction.timestamp.desc()).offset(skip).limit(limit).all()
    
    return transactions


@router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(
    transaction_id: str,
    db: Session = Depends(get_db)
):
    """
    Récupère une transaction par son ID
    """
    transaction = db.query(models.Transaction).filter(
        models.Transaction.transaction_id == transaction_id
    ).first()
    
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction non trouvée")
    
    return transaction


@router.post("/", response_model=TransactionResponse)
async def create_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db)
):
    """
    Crée une nouvelle transaction
    """
    # Vérifier si existe déjà
    existing = db.query(models.Transaction).filter(
        models.Transaction.transaction_id == transaction.transaction_id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Transaction déjà existante")
    
    db_transaction = models.Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    
    return db_transaction


@router.delete("/{transaction_id}")
async def delete_transaction(
    transaction_id: str,
    db: Session = Depends(get_db)
):
    """
    Supprime une transaction
    """
    transaction = db.query(models.Transaction).filter(
        models.Transaction.transaction_id == transaction_id
    ).first()
    
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction non trouvée")
    
    db.delete(transaction)
    db.commit()
    
    return {"message": "Transaction supprimée"}
