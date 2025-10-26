"""
Health Check Endpoints
"""
from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/health")
async def health_check():
    """Basic health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "QuantEdge Trading Simulator"
    }

@router.get("/status")
async def system_status():
    """Detailed system status"""
    return {
        "api": "operational",
        "database": "connected",
        "ml_models": "loaded",
        "trading_engine": "active",
        "timestamp": datetime.utcnow().isoformat()
    }
