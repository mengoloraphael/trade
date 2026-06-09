"""Portfolio endpoints"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from loguru import logger

from src.api.schemas import PortfolioResponse, PositionResponse, TradeResponse
from src.database.session import get_db
from src.database.models import Portfolio, Position, Trade

router = APIRouter(prefix="/portfolio", tags=["portfolio"])


@router.get("/", response_model=PortfolioResponse)
async def get_portfolio(
    portfolio_id: int = 1,
    db: Session = Depends(get_db)
):
    """
    Get portfolio information
    
    Args:
        portfolio_id: Portfolio ID
    
    Returns:
        Portfolio details
    """
    portfolio = db.query(Portfolio).filter(
        Portfolio.id == portfolio_id
    ).first()
    
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    
    return portfolio


@router.get("/positions", response_model=list[PositionResponse])
async def get_positions(
    portfolio_id: int = 1,
    db: Session = Depends(get_db)
):
    """
    Get open positions
    
    Args:
        portfolio_id: Portfolio ID
    
    Returns:
        List of open positions
    """
    positions = db.query(Position).filter(
        Position.portfolio_id == portfolio_id,
        Position.is_open == True
    ).all()
    
    return positions


@router.get("/trades", response_model=list[TradeResponse])
async def get_trades(
    portfolio_id: int = 1,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get trade history
    
    Args:
        portfolio_id: Portfolio ID
        limit: Number of trades
    
    Returns:
        List of trades
    """
    trades = db.query(Trade).filter(
        Trade.portfolio_id == portfolio_id
    ).order_by(
        Trade.opened_at.desc()
    ).limit(limit).all()
    
    return trades


@router.get("/stats")
async def get_portfolio_stats(
    portfolio_id: int = 1,
    db: Session = Depends(get_db)
):
    """
    Get portfolio statistics
    
    Args:
        portfolio_id: Portfolio ID
    
    Returns:
        Portfolio statistics
    """
    portfolio = db.query(Portfolio).filter(
        Portfolio.id == portfolio_id
    ).first()
    
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    
    trades = db.query(Trade).filter(
        Trade.portfolio_id == portfolio_id
    ).all()
    
    winning_trades = sum(1 for t in trades if t.pnl > 0)
    total_pnl = sum(t.pnl for t in trades)
    
    return {
        "balance": portfolio.balance,
        "unrealized_pnl": portfolio.unrealized_pnl,
        "realized_pnl": portfolio.realized_pnl,
        "total_return": portfolio.total_return,
        "total_trades": len(trades),
        "winning_trades": winning_trades,
        "win_rate": winning_trades / len(trades) if trades else 0,
        "total_pnl": total_pnl,
    }
