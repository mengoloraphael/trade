"""Backtest endpoints"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from datetime import datetime
from loguru import logger

from src.api.schemas import BacktestRequest, BacktestResultResponse
from src.database.session import get_db
from src.database.models import BacktestResult
from src.data.collector import DataCollectorFactory
from src.data.preprocessor import DataPreprocessor
from src.trading.signals import SignalGenerator
from src.backtesting.backtest import BacktestEngine

router = APIRouter(prefix="/backtests", tags=["backtests"])


@router.post("/run", response_model=BacktestResultResponse)
async def run_backtest(
    request: BacktestRequest,
    db: Session = Depends(get_db)
):
    """
    Run a backtest for a symbol
    
    Args:
        request: Backtest parameters
    
    Returns:
        Backtest results
    """
    try:
        logger.info(f"Running backtest for {request.symbol}")
        
        # Get historical data
        collector = DataCollectorFactory.create_collector(request.symbol)
        df = await collector.fetch_historical_data(
            request.symbol,
            "daily",
            (request.end_date - request.start_date).days
        )
        
        if df.empty:
            raise HTTPException(status_code=404, detail="No data available")
        
        # Filter by date range
        df = df[request.start_date:request.end_date]
        
        # Preprocess
        preprocessor = DataPreprocessor()
        df = preprocessor.clean_data(df)
        df = preprocessor.add_technical_features(df)
        
        # Run backtest
        engine = BacktestEngine(
            initial_balance=request.initial_balance,
            commission_pct=0.001,
            slippage_pct=0.0005,
        )
        
        # Use signal generator as strategy
        strategy = SignalGenerator().generate_signal
        result = engine.run(df, strategy, request.symbol)
        
        # Save result
        db_result = BacktestResult(
            symbol=request.symbol,
            strategy_name="SignalGenerator",
            initial_balance=request.initial_balance,
            final_balance=request.initial_balance * (1 + result.total_return),
            total_return=result.total_return,
            annual_return=result.annual_return,
            win_rate=result.win_rate,
            profit_factor=result.profit_factor,
            max_drawdown=result.max_drawdown,
            sharpe_ratio=result.sharpe_ratio,
            trades_count=result.trades_count,
            winning_trades=result.winning_trades,
            losing_trades=result.losing_trades,
            start_date=request.start_date,
            end_date=request.end_date,
            parameters={
                "max_position_size": request.max_position_size,
                "stop_loss_pct": request.stop_loss_pct,
                "take_profit_pct": request.take_profit_pct,
            },
            trades_data=result.trades,
        )
        db.add(db_result)
        db.commit()
        db.refresh(db_result)
        
        return db_result
    
    except Exception as e:
        logger.error(f"Error running backtest: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/results")
async def get_backtest_results(
    symbol: str = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """
    Get backtest results
    
    Args:
        symbol: Optional symbol filter
        limit: Number of results
    
    Returns:
        List of backtest results
    """
    query = db.query(BacktestResult)
    
    if symbol:
        query = query.filter(BacktestResult.symbol == symbol)
    
    results = query.order_by(
        BacktestResult.created_at.desc()
    ).limit(limit).all()
    
    return results
