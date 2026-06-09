"""Prediction endpoints"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from loguru import logger
import numpy as np

from src.api.schemas import PredictionRequest, PredictionResponse
from src.database.session import get_db
from src.database.models import Prediction
from src.data.collector import DataCollectorFactory
from src.data.preprocessor import DataPreprocessor
from src.models.lstm_model import LSTMModel

router = APIRouter(prefix="/predictions", tags=["predictions"])


@router.post("/predict", response_model=PredictionResponse)
async def predict_price(
    request: PredictionRequest,
    db: Session = Depends(get_db)
):
    """
    Predict next price movement
    
    Args:
        request: Prediction request with symbol and parameters
    
    Returns:
        Price prediction with confidence
    """
    try:
        logger.info(f"Predicting price for {request.symbol}")
        
        # Get historical data
        collector = DataCollectorFactory.create_collector(request.symbol)
        df = await collector.fetch_historical_data(
            request.symbol,
            "daily",
            request.lookback + request.horizon
        )
        
        if df.empty:
            raise HTTPException(status_code=404, detail="No data available")
        
        # Preprocess
        preprocessor = DataPreprocessor()
        df = preprocessor.clean_data(df)
        df = preprocessor.add_technical_features(df)
        
        # Prepare data for model
        X, features = preprocessor.prepare_batch(df, request.lookback)
        
        if X is None:
            raise HTTPException(status_code=400, detail="Insufficient data")
        
        # TODO: Load and use trained model
        # For now, use simple prediction
        current_price = df.iloc[-1]["close"]
        predicted_price = current_price * (1 + np.random.randn() * 0.01)
        confidence = 0.65 + np.random.rand() * 0.2
        
        # Save prediction
        db_pred = Prediction(
            symbol=request.symbol,
            predicted_price=predicted_price,
            confidence=confidence,
            horizon=request.horizon,
        )
        db.add(db_pred)
        db.commit()
        db.refresh(db_pred)
        
        return PredictionResponse(
            symbol=request.symbol,
            predicted_price=predicted_price,
            confidence=confidence,
            horizon=request.horizon,
            timestamp=datetime.utcnow()
        )
    
    except Exception as e:
        logger.error(f"Error predicting: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history/{symbol}")
async def get_predictions(
    symbol: str,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get prediction history for a symbol
    
    Args:
        symbol: Trading symbol
        limit: Number of records
    
    Returns:
        List of predictions
    """
    predictions = db.query(Prediction).filter(
        Prediction.symbol == symbol
    ).order_by(
        Prediction.created_at.desc()
    ).limit(limit).all()
    
    return predictions
