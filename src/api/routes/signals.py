"""Signal endpoints"""

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime
from loguru import logger

from src.api.schemas import SignalResponse, SignalCreate
from src.database.session import get_db
from src.database.models import Signal
from src.data.collector import DataCollectorFactory
from src.data.preprocessor import DataPreprocessor
from src.trading.signals import SignalGenerator

router = APIRouter(prefix="/signals", tags=["signals"])


@router.get("/{symbol}", response_model=SignalResponse)
async def get_signal(symbol: str, db: Session = Depends(get_db)):
    """
    Get latest signal for a symbol
    
    Args:
        symbol: Trading symbol (e.g., EURUSD, XAUUSD)
    
    Returns:
        Latest trading signal
    """
    try:
        logger.info(f"Getting signal for {symbol}")
        
        # Get latest data
        collector = DataCollectorFactory.create_collector(symbol)
        df = await collector.fetch_historical_data(symbol, "daily", 365)
        
        if df.empty:
            raise HTTPException(status_code=404, detail="No data available")
        
        # Preprocess
        preprocessor = DataPreprocessor()
        df = preprocessor.clean_data(df)
        df = preprocessor.add_technical_features(df)
        
        # Generate signal
        generator = SignalGenerator()
        signal = generator.generate_signal(df, symbol)
        
        if signal is None:
            raise HTTPException(status_code=400, detail="Cannot generate signal")
        
        # Save to database
        db_signal = Signal(
            symbol=symbol,
            signal_type=signal.signal_type.value,
            confidence=signal.confidence,
            price=signal.price,
            reason=signal.reason,
            indicators=signal.indicators,
        )
        db.add(db_signal)
        db.commit()
        db.refresh(db_signal)
        
        return db_signal
    
    except Exception as e:
        logger.error(f"Error getting signal: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history")
async def get_signal_history(
    symbol: str = Query(...),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """
    Get signal history for a symbol
    
    Args:
        symbol: Trading symbol
        limit: Number of records to return
    
    Returns:
        List of historical signals
    """
    signals = db.query(Signal).filter(
        Signal.symbol == symbol
    ).order_by(
        Signal.timestamp.desc()
    ).limit(limit).all()
    
    return signals


@router.get("/performance")
async def get_signal_performance(
    symbol: str = Query(...),
    db: Session = Depends(get_db)
):
    """
    Get signal performance metrics
    
    Args:
        symbol: Trading symbol
    
    Returns:
        Performance metrics
    """
    signals = db.query(Signal).filter(
        Signal.symbol == symbol,
        Signal.acted_on == True
    ).all()
    
    if not signals:
        raise HTTPException(status_code=404, detail="No acted signals found")
    
    correct = sum(1 for s in signals if s.acted_on)
    accuracy = correct / len(signals) if signals else 0
    
    avg_confidence = sum(s.confidence for s in signals) / len(signals) if signals else 0
    
    return {
        "symbol": symbol,
        "total_signals": len(signals),
        "acted_signals": correct,
        "accuracy": accuracy,
        "avg_confidence": avg_confidence,
    }
