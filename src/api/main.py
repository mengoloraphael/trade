"""Main FastAPI application with routes"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from loguru import logger

from src.config import get_settings
from src.database.session import init_db
from src.api.routes import signals, predictions, backtests, portfolio

# Initialize settings
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown"""
    logger.info("Starting Trade AI application")
    init_db()
    yield
    logger.info("Shutting down Trade AI application")


# Create FastAPI app
app = FastAPI(
    title="Trade AI",
    description="Trading Intelligence Platform for Forex & Gold",
    version="0.2.0",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(signals.router)
app.include_router(predictions.router)
app.include_router(backtests.router)
app.include_router(portfolio.router)


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "app": settings.app_name,
        "environment": settings.environment,
        "version": "0.2.0",
        "demo_mode": settings.demo_mode,
    }


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Trade AI",
        "docs": "/docs",
        "version": "0.2.0",
        "endpoints": {
            "signals": "/signals",
            "predictions": "/predictions",
            "backtests": "/backtests",
            "portfolio": "/portfolio",
        }
    }


# Status endpoint
@app.get("/status")
async def status():
    """Application status"""
    return {
        "app_name": settings.app_name,
        "environment": settings.environment,
        "debug": settings.debug,
        "demo_mode": settings.demo_mode,
        "symbols": {
            "forex_pairs": settings.forex_pairs_list,
            "gold": settings.gold_symbol,
        },
        "models": {
            "type": settings.model_type,
            "lookback": settings.lookback_period,
            "horizon": settings.prediction_horizon,
        }
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
    )
