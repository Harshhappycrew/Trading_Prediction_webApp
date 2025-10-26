"""
Machine Learning API Endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import List

from app.database.init_db import get_db
from app.models.stock_data import MLPrediction

router = APIRouter()

@router.get("/predictions/{symbol}")
async def get_predictions(
    symbol: str,
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    """Get ML predictions for a symbol"""
    try:
        result = await db.execute(
            select(MLPrediction)
            .where(MLPrediction.symbol == symbol.upper())
            .order_by(desc(MLPrediction.timestamp))
            .limit(limit)
        )
        predictions = result.scalars().all()
        
        return [
            {
                "symbol": pred.symbol,
                "timestamp": pred.timestamp.isoformat(),
                "model_name": pred.model_name,
                "predicted_price": pred.predicted_price,
                "predicted_direction": pred.predicted_direction,
                "confidence": pred.confidence,
                "upper_bound": pred.upper_bound,
                "lower_bound": pred.lower_bound
            }
            for pred in predictions
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/signals")
async def get_trading_signals(db: AsyncSession = Depends(get_db)):
    """Get current trading signals from ML models"""
    try:
        # Get latest predictions for all symbols
        symbols = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN"]
        signals = []
        
        for symbol in symbols:
            result = await db.execute(
                select(MLPrediction)
                .where(MLPrediction.symbol == symbol)
                .order_by(desc(MLPrediction.timestamp))
                .limit(1)
            )
            pred = result.scalar_one_or_none()
            
            if pred:
                signals.append({
                    "symbol": pred.symbol,
                    "signal": pred.predicted_direction,
                    "confidence": pred.confidence,
                    "model": pred.model_name,
                    "timestamp": pred.timestamp.isoformat()
                })
        
        return {"signals": signals}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/train/{model_type}")
async def train_model(model_type: str):
    """Trigger ML model training"""
    try:
        # This would trigger the actual training process
        return {
            "status": "training_started",
            "model_type": model_type,
            "message": "Model training initiated in background"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
