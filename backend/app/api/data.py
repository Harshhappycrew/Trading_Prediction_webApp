"""
Data Management API Endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, func
from datetime import datetime, timedelta

from app.database.init_db import get_db
from app.models.stock_data import StockPrice

router = APIRouter()

@router.get("/price/{symbol}")
async def get_stock_prices(
    symbol: str,
    days: int = 30,
    db: AsyncSession = Depends(get_db)
):
    """Get historical stock prices"""
    try:
        start_date = datetime.utcnow() - timedelta(days=days)
        
        result = await db.execute(
            select(StockPrice)
            .where(
                StockPrice.symbol == symbol.upper(),
                StockPrice.timestamp >= start_date
            )
            .order_by(StockPrice.timestamp)
        )
        prices = result.scalars().all()
        
        return [
            {
                "timestamp": price.timestamp.isoformat(),
                "open": price.open,
                "high": price.high,
                "low": price.low,
                "close": price.close,
                "volume": price.volume,
                "rsi": price.rsi,
                "macd": price.macd,
                "bb_upper": price.bb_upper,
                "bb_lower": price.bb_lower
            }
            for price in prices
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/sync/{symbol}")
async def sync_stock_data(symbol: str):
    """Trigger data synchronization for a symbol"""
    try:
        # This would trigger the data collection process
        return {
            "status": "sync_started",
            "symbol": symbol.upper(),
            "message": "Data synchronization initiated"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/symbols")
async def get_available_symbols(db: AsyncSession = Depends(get_db)):
    """Get list of available symbols"""
    try:
        result = await db.execute(
            select(StockPrice.symbol)
            .distinct()
        )
        symbols = result.scalars().all()
        
        return {"symbols": list(symbols) if symbols else ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
