"""
QuantEdge - AI-Powered Trading Simulator
Main FastAPI Application Entry Point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from loguru import logger
import sys

from app.api import health, trading, portfolio, ml, data, stocks
from app.database.init_db import init_database

# Configure logging
logger.remove()
logger.add(sys.stderr, level="INFO")
logger.add("logs/quantedge.log", rotation="500 MB", level="DEBUG")

# Create FastAPI app
app = FastAPI(
    title="QuantEdge API",
    description="AI-Powered Quantitative Trading Simulator",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(trading.router, prefix="/api/trading", tags=["trading"])
app.include_router(portfolio.router, prefix="/api/portfolio", tags=["portfolio"])
app.include_router(ml.router, prefix="/api/ml", tags=["machine-learning"])
app.include_router(data.router, prefix="/api/data", tags=["data"])
app.include_router(stocks.router, prefix="/api/stocks", tags=["stocks"])

@app.on_event("startup")
async def startup_event():
    """Initialize database and load ML models on startup"""
    logger.info("Starting QuantEdge Trading Simulator...")
    await init_database()
    logger.info("Database initialized successfully")
    # Load ML models here if needed
    logger.info("QuantEdge is ready!")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down QuantEdge...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
