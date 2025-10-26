"""
Portfolio Management API Endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import List
from datetime import datetime, timedelta

from app.database.init_db import get_db
from app.models.portfolio import Position, PortfolioSnapshot

router = APIRouter()

@router.get("/positions")
async def get_positions(db: AsyncSession = Depends(get_db)):
    """Get current portfolio positions"""
    try:
        result = await db.execute(select(Position))
        positions = result.scalars().all()
        
        return [
            {
                "symbol": pos.symbol,
                "quantity": pos.quantity,
                "avg_entry_price": pos.avg_entry_price,
                "current_price": pos.current_price,
                "unrealized_pnl": pos.unrealized_pnl,
                "unrealized_pnl_percent": pos.unrealized_pnl_percent,
                "market_value": pos.quantity * pos.current_price,
                "stop_loss": pos.stop_loss,
                "take_profit": pos.take_profit
            }
            for pos in positions
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/performance")
async def get_performance(
    days: int = 30,
    db: AsyncSession = Depends(get_db)
):
    """Get portfolio performance history"""
    try:
        start_date = datetime.utcnow() - timedelta(days=days)
        
        result = await db.execute(
            select(PortfolioSnapshot)
            .where(PortfolioSnapshot.timestamp >= start_date)
            .order_by(PortfolioSnapshot.timestamp)
        )
        snapshots = result.scalars().all()
        
        return {
            "history": [
                {
                    "timestamp": snap.timestamp.isoformat(),
                    "total_value": snap.total_value,
                    "cash_balance": snap.cash_balance,
                    "positions_value": snap.positions_value,
                    "total_pnl": snap.total_pnl,
                    "total_pnl_percent": snap.total_pnl_percent,
                    "daily_return": snap.daily_return
                }
                for snap in snapshots
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/metrics")
async def get_portfolio_metrics(db: AsyncSession = Depends(get_db)):
    """Get current portfolio metrics"""
    try:
        # Get latest snapshot
        result = await db.execute(
            select(PortfolioSnapshot)
            .order_by(desc(PortfolioSnapshot.timestamp))
            .limit(1)
        )
        latest = result.scalar_one_or_none()
        
        if not latest:
            return {
                "total_value": 100000.0,
                "cash_balance": 100000.0,
                "positions_value": 0.0,
                "total_pnl": 0.0,
                "total_pnl_percent": 0.0
            }
        
        return {
            "total_value": latest.total_value,
            "cash_balance": latest.cash_balance,
            "positions_value": latest.positions_value,
            "total_pnl": latest.total_pnl,
            "total_pnl_percent": latest.total_pnl_percent,
            "daily_return": latest.daily_return
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
