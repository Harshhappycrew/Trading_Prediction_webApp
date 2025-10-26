"""
Stock Data Models
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Index
from app.database.init_db import Base
from datetime import datetime

class StockPrice(Base):
    """Historical stock price data"""
    __tablename__ = "stock_prices"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(10), nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    
    # OHLCV data
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(Integer, nullable=False)
    
    # Technical indicators
    rsi = Column(Float, nullable=True)
    macd = Column(Float, nullable=True)
    macd_signal = Column(Float, nullable=True)
    bb_upper = Column(Float, nullable=True)
    bb_middle = Column(Float, nullable=True)
    bb_lower = Column(Float, nullable=True)
    sma_20 = Column(Float, nullable=True)
    sma_50 = Column(Float, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_symbol_timestamp', 'symbol', 'timestamp'),
    )

class MLPrediction(Base):
    """ML model predictions"""
    __tablename__ = "ml_predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(10), nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    
    # Prediction data
    model_name = Column(String(50), nullable=False)
    predicted_price = Column(Float, nullable=False)
    predicted_direction = Column(String(10), nullable=False)  # UP, DOWN, NEUTRAL
    confidence = Column(Float, nullable=False)
    
    # Bounds
    upper_bound = Column(Float, nullable=True)
    lower_bound = Column(Float, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
