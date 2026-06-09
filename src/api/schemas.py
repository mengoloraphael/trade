"""Pydantic schemas for API validation"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime
from enum import Enum


class SignalType(str, Enum):
    """Signal types"""
    BUY = "buy"
    SELL = "sell"
    HOLD = "hold"
    STRONG_BUY = "strong_buy"
    STRONG_SELL = "strong_sell"


# Signal Schemas
class SignalCreate(BaseModel):
    """Schema for creating signals"""
    symbol: str
    signal_type: SignalType
    confidence: float = Field(..., ge=0, le=1)
    price: float
    reason: str
    indicators: Optional[Dict] = None


class SignalResponse(SignalCreate):
    """Schema for signal response"""
    id: int
    timestamp: datetime
    acted_on: bool

    class Config:
        from_attributes = True


# Prediction Schemas
class PredictionRequest(BaseModel):
    """Schema for prediction request"""
    symbol: str
    horizon: int = Field(default=5, ge=1, le=100)
    lookback: int = Field(default=60, ge=10, le=500)


class PredictionResponse(BaseModel):
    """Schema for prediction response"""
    symbol: str
    predicted_price: float
    confidence: float
    horizon: int
    timestamp: datetime


# Portfolio Schemas
class PortfolioResponse(BaseModel):
    """Schema for portfolio response"""
    id: int
    name: str
    balance: float
    unrealized_pnl: float
    realized_pnl: float
    total_return: float
    created_at: datetime

    class Config:
        from_attributes = True


# Position Schemas
class PositionResponse(BaseModel):
    """Schema for position response"""
    id: int
    symbol: str
    side: str
    quantity: float
    entry_price: float
    current_price: float
    unrealized_pnl: float
    is_open: bool
    opened_at: datetime

    class Config:
        from_attributes = True


# Trade Schemas
class TradeResponse(BaseModel):
    """Schema for trade response"""
    id: int
    symbol: str
    side: str
    quantity: float
    entry_price: float
    exit_price: Optional[float]
    pnl: float
    pnl_percentage: float
    status: str
    opened_at: datetime

    class Config:
        from_attributes = True


# Backtest Schemas
class BacktestRequest(BaseModel):
    """Schema for backtest request"""
    symbol: str
    start_date: datetime
    end_date: datetime
    initial_balance: float = 10000.0
    max_position_size: float = 0.02
    stop_loss_pct: float = 0.02
    take_profit_pct: float = 0.05


class BacktestResultResponse(BaseModel):
    """Schema for backtest result"""
    id: int
    symbol: str
    initial_balance: float
    final_balance: float
    total_return: float
    win_rate: float
    profit_factor: float
    max_drawdown: float
    sharpe_ratio: float
    trades_count: int
    created_at: datetime

    class Config:
        from_attributes = True


# Market Data Schemas
class MarketDataResponse(BaseModel):
    """Schema for market data"""
    symbol: str
    price: float
    bid: Optional[float]
    ask: Optional[float]
    volume: Optional[float]
    timestamp: datetime


class IndicatorsResponse(BaseModel):
    """Schema for technical indicators"""
    rsi: Optional[float]
    macd: Optional[float]
    macd_signal: Optional[float]
    sma_20: Optional[float]
    sma_50: Optional[float]
    sma_200: Optional[float]
    bb_upper: Optional[float]
    bb_lower: Optional[float]
    bb_middle: Optional[float]
    atr: Optional[float]
    timestamp: datetime


# Error Schema
class ErrorResponse(BaseModel):
    """Schema for error response"""
    detail: str
    error_code: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
