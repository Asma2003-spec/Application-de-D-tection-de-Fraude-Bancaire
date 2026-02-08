from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import transactions, analysis, alerts, stats
from app.database.database import engine, Base

# Créer les tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Fraud Detection API",
    description="API de détection de fraude avec ML et règles métier",
    version="1.0.0"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclure les routers
app.include_router(transactions.router, prefix="/api/transactions", tags=["transactions"])
app.include_router(analysis.router, prefix="/api/analysis", tags=["analysis"])
app.include_router(alerts.router, prefix="/api/alerts", tags=["alerts"])
app.include_router(stats.router, prefix="/api/stats", tags=["stats"])

@app.get("/")
async def root():
    return {
        "message": "Fraud Detection API",
        "version": "1.0.0",
        "endpoints": [
            "/api/transactions",
            "/api/analysis",
            "/api/alerts",
            "/api/stats"
        ]
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
