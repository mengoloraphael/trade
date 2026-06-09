"""Alpha Vantage API integration for Forex and commodities data"""

import requests
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, Dict
from loguru import logger
from src.config import settings


class AlphaVantageClient:
    """Client for Alpha Vantage API"""

    BASE_URL = "https://www.alphavantage.co/query"

    def __init__(self, api_key: Optional[str] = None):
        """Initialize Alpha Vantage client"""
        self.api_key = api_key or settings.alpha_vantage_api_key
        if not self.api_key:
            logger.warning("Alpha Vantage API key not configured")
        logger.info("AlphaVantageClient initialized")

    def get_forex_daily(self, pair: str, outputsize: str = "full") -> pd.DataFrame:
        """
        Get daily forex data

        Args:
            pair: e.g., "EURUSD"
            outputsize: "compact" or "full"

        Returns:
            DataFrame with OHLCV data
        """
        logger.info(f"Fetching forex daily data for {pair}")

        params = {
            "function": "FX_DAILY",
            "from_symbol": pair[:3],
            "to_symbol": pair[3:],
            "outputsize": outputsize,
            "apikey": self.api_key,
        }

        try:
            response = requests.get(self.BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()

            if "Error Message" in data:
                logger.error(f"API Error: {data['Error Message']}")
                return pd.DataFrame()

            if "Time Series FX (Daily)" not in data:
                logger.warning(f"No data returned for {pair}")
                return pd.DataFrame()

            # Parse data
            ts = data["Time Series FX (Daily)"]
            df = pd.DataFrame.from_dict(ts, orient="index")
            df.index = pd.to_datetime(df.index)
            df.columns = ["open", "high", "low", "close"]
            df = df.astype(float)
            df.sort_index(inplace=True)

            logger.info(f"Successfully fetched {len(df)} records for {pair}")
            return df

        except requests.RequestException as e:
            logger.error(f"Request error: {e}")
            return pd.DataFrame()

    def get_intraday(self, symbol: str, interval: str = "60min") -> pd.DataFrame:
        """
        Get intraday data

        Args:
            symbol: Trading symbol
            interval: "1min", "5min", "15min", "30min", "60min"

        Returns:
            DataFrame with OHLCV data
        """
        logger.info(f"Fetching intraday data for {symbol}")

        params = {
            "function": "TIME_SERIES_INTRADAY",
            "symbol": symbol,
            "interval": interval,
            "apikey": self.api_key,
        }

        try:
            response = requests.get(self.BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()

            if "Error Message" in data:
                logger.error(f"API Error: {data['Error Message']}")
                return pd.DataFrame()

            key = f"Time Series ({interval})"
            if key not in data:
                logger.warning(f"No data returned for {symbol}")
                return pd.DataFrame()

            ts = data[key]
            df = pd.DataFrame.from_dict(ts, orient="index")
            df.index = pd.to_datetime(df.index)
            df.columns = ["open", "high", "low", "close"]
            df = df.astype(float)
            df.sort_index(inplace=True)

            logger.info(f"Successfully fetched {len(df)} records")
            return df

        except requests.RequestException as e:
            logger.error(f"Request error: {e}")
            return pd.DataFrame()

    def get_quote(self, symbol: str) -> Dict:
        """Get current quote"""
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": symbol,
            "apikey": self.api_key,
        }

        try:
            response = requests.get(self.BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()

            if "Global Quote" in data:
                return data["Global Quote"]
            return {}

        except requests.RequestException as e:
            logger.error(f"Request error: {e}")
            return {}
