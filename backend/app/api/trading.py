"""
Trading API Endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import List
from datetime import datetime

from app.database.init_db import get_db
from app.models.trades import Trade, Order, OrderSide, OrderType, OrderStatus
from pydantic import BaseModel

router = APIRouter()

class OrderRequest(BaseModel):
    symbol: str
    side: str
    quantity: int
    order_type: str = "MARKET"
    price: float = None

class TradeResponse(BaseModel):
    id: int
    symbol: str
    side: str
    quantity: int
    price: float
    pnl: float = None
    timestamp: datetime

@router.post("/orders")
async def create_order(
    order_req: OrderRequest,
    db: AsyncSession = Depends(get_db)
):
    """Create a new trading order"""
    try:
        order = Order(
            symbol=order_req.symbol.upper(),
            order_type=OrderType[order_req.order_type],
            side=OrderSide[order_req.side],
            quantity=order_req.quantity,
            price=order_req.price,
            status=OrderStatus.PENDING
        )
        
        db.add(order)
        await db.commit()
        await db.refresh(order)
        
        return {
            "order_id": order.id,
            "status": order.status.value,
            "message": "Order created successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/trades", response_model=List[TradeResponse])
async def get_trades(
    limit: int = 50,
    db: AsyncSession = Depends(get_db)
):
    """Get recent trade history"""
    try:
        result = await db.execute(
            select(Trade)
            .order_by(desc(Trade.timestamp))
            .limit(limit)
        )
        trades = result.scalars().all()
        
        return [
            TradeResponse(
                id=trade.id,
                symbol=trade.symbol,
                side=trade.side.value,
                quantity=trade.quantity,
                price=trade.price,
                pnl=trade.pnl,
                timestamp=trade.timestamp
            )
            for trade in trades
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/orders")
async def get_orders(
    status: str = None,
    db: AsyncSession = Depends(get_db)
):
    """Get order history"""
    try:
        query = select(Order).order_by(desc(Order.created_at))
        
        if status:
            query = query.where(Order.status == OrderStatus[status])
        
        result = await db.execute(query.limit(50))
        orders = result.scalars().all()
        
        return [
            {
                "id": order.id,
                "symbol": order.symbol,
                "side": order.side.value,
                "quantity": order.quantity,
                "price": order.price,
                "status": order.status.value,
                "created_at": order.created_at.isoformat()
            }
            for order in orders
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
