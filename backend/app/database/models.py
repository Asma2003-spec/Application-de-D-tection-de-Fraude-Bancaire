from sqlalchemy import Column, Integer, Float, String, DateTime, Boolean, Text
from sqlalchemy.sql import func
from app.database.database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String, unique=True, index=True)
    amount = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    merchant = Column(String)
    category = Column(String)
    location = Column(String)
    user_id = Column(String, index=True)
    
    # Champs calculés
    risk_score = Column(Float, default=0.0)
    is_fraud = Column(Boolean, default=False)
    fraud_type = Column(String, nullable=True)
    
    # Métadonnées
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String, index=True)
    alert_type = Column(String)  # rule_based, ml_based, hybrid
    risk_score = Column(Float)
    severity = Column(String)  # low, medium, high, critical
    reason = Column(Text)
    
    # Statut
    status = Column(String, default="pending")  # pending, confirmed, rejected
    reviewed_by = Column(String, nullable=True)
    reviewed_at = Column(DateTime, nullable=True)
    
    # Métadonnées
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())


class MLModel(Base):
    __tablename__ = "ml_models"

    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String)
    model_type = Column(String)  # isolation_forest, random_forest, etc.
    version = Column(String)
    accuracy = Column(Float)
    precision = Column(Float)
    recall = Column(Float)
    f1_score = Column(Float)
    
    is_active = Column(Boolean, default=False)
    trained_at = Column(DateTime, server_default=func.now())
    model_path = Column(String)
