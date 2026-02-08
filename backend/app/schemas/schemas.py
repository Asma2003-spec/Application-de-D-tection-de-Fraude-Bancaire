from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class TransactionBase(BaseModel):
    transaction_id: str
    amount: float = Field(..., gt=0)
    timestamp: datetime
    merchant: Optional[str] = None
    category: Optional[str] = None
    location: Optional[str] = None
    user_id: str

class TransactionCreate(TransactionBase):
    pass

class TransactionResponse(TransactionBase):
    id: int
    risk_score: float
    is_fraud: bool
    fraud_type: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class AlertBase(BaseModel):
    transaction_id: str
    alert_type: str
    risk_score: float
    severity: str
    reason: str

class AlertCreate(AlertBase):
    pass

class AlertResponse(AlertBase):
    id: int
    status: str
    reviewed_by: Optional[str] = None
    reviewed_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True

class AlertUpdate(BaseModel):
    status: str
    reviewed_by: Optional[str] = None

class AnalysisRequest(BaseModel):
    transaction_ids: Optional[List[str]] = None
    use_ml: bool = True
    use_rules: bool = True

class AnalysisResponse(BaseModel):
    total_analyzed: int
    frauds_detected: int
    average_risk_score: float
    alerts_created: int
    processing_time: float

class StatsResponse(BaseModel):
    total_transactions: int
    total_frauds: int
    fraud_rate: float
    total_alerts: int
    pending_alerts: int
    confirmed_frauds: int
    total_amount_at_risk: float
