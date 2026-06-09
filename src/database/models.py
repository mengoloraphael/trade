"""SQLAlchemy models for Trade AI"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Enum, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum
from loguru import logger

Base = declarative_base()


class User(Base):
    """User model"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    initial_balance = Column(Float, default=10000.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    portfolios = relationship("Portfolio", back_populates="user")
    trades = relationship("Trade", back_populates="user")
    signals = relationship("Signal", back_populates="user")


class Portfolio(Base):
    """Portfolio model"""
    __tablename__ = "portfolios"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    name = Column(String)
    balance = Column(Float)
    unrealized_pnl = Column(Float, default=0.0)
    realized_pnl = Column(Float, default=0.0)
    total_return = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="portfolios")
    positions = relationship("Position", back_populates="portfolio")
    trades = relationship("Trade", back_populates="portfolio")


class Position(Base):
    """Trading position model"""
    __tablename__ = "positions"

    id = Column(Integer, primary_key=True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"), index=True)
    symbol = Column(String, index=True)
    side = Column(String)  # "long" or "short"
    quantity = Column(Float)
    entry_price = Column(Float)
    current_price = Column(Float)
    stop_loss = Column(Float)
    take_profit = Column(Float)
    unrealized_pnl = Column(Float, default=0.0)
    opened_at = Column(DateTime, default=datetime.utcnow)
    closed_at = Column(DateTime, nullable=True)
    is_open = Column(Boolean, default=True)

    # Relationships
    portfolio = relationship("Portfolio", back_populates="positions")
    trades = relationship("Trade", back_populates="position")


class Trade(Base):
    """Trade execution model"""
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"), index=True)
    position_id = Column(Integer, ForeignKey("positions.id"), nullable=True)
    symbol = Column(String, index=True)
    side = Column(String)  # "buy" or "sell"
    quantity = Column(Float)
    entry_price = Column(Float)
    exit_price = Column(Float, nullable=True)
    pnl = Column(Float, default=0.0)
    pnl_percentage = Column(Float, default=0.0)
    commission = Column(Float, default=0.0)
    status = Column(String, default="open")  # "open", "closed", "cancelled"
    opened_at = Column(DateTime, default=datetime.utcnow)
    closed_at = Column(DateTime, nullable=True)
    reason = Column(String)
    metadata = Column(JSON, default={})

    # Relationships
    user = relationship("User", back_populates="trades")
    portfolio = relationship("Portfolio", back_populates="trades")
    position = relationship("Position", back_populates="trades")


class Signal(Base):
    """Trading signal model"""
    __tablename__ = "signals"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    symbol = Column(String, index=True)
    signal_type = Column(String)  # "buy", "sell", "hold", "strong_buy", "strong_sell"
    confidence = Column(Float)  # 0 to 1
    price = Column(Float)
    reason = Column(String)
    indicators = Column(JSON)  # JSON with indicator values
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    acted_on = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="signals")


class Prediction(Base):
    """Price prediction model"""
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True)
    symbol = Column(String, index=True)
    predicted_price = Column(Float)
    confidence = Column(Float)
    horizon = Column(Integer)  # periods ahead
    actual_price = Column(Float, nullable=True)
    accuracy = Column(Float, nullable=True)  # calculated after horizon
    created_at = Column(DateTime, default=datetime.utcnow)
    verified_at = Column(DateTime, nullable=True)


class BacktestResult(Base):
    """Backtest result model"""
    __tablename__ = "backtest_results"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    symbol = Column(String)
    strategy_name = Column(String)
    initial_balance = Column(Float)
    final_balance = Column(Float)
    total_return = Column(Float)
    annual_return = Column(Float)
    win_rate = Column(Float)
    profit_factor = Column(Float)
    max_drawdown = Column(Float)
    sharpe_ratio = Column(Float)
    trades_count = Column(Integer)
    winning_trades = Column(Integer)
    losing_trades = Column(Integer)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    parameters = Column(JSON)  # Strategy parameters used
    trades_data = Column(JSON)  # Detailed trades
    created_at = Column(DateTime, default=datetime.utcnow)


class PriceData(Base):
    """Historical price data"""
    __tablename__ = "price_data"

    id = Column(Integer, primary_key=True)
    symbol = Column(String, index=True)
    timeframe = Column(String)  # "1m", "5m", "15m", "1h", "4h", "1d", etc.
    timestamp = Column(DateTime, index=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        # Composite index for symbol and timestamp
        # CREATE INDEX idx_symbol_timestamp ON price_data(symbol, timestamp),
    )
