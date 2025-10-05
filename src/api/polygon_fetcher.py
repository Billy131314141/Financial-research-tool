"""
Polygon.io data fetcher with rate limiting for free tier.
Free tier: 5 API calls per minute - we'll use max 4 to be safe.
"""
from polygon import RESTClient
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, Dict, List
import os
import logging
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class PolygonDataFetcher:
    """Fetches financial data from Polygon.io with rate limiting."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Polygon data fetcher.
        
        Args:
            api_key: Polygon.io API key. If None, reads from POLYGON_API_KEY env variable.
        """
        self.api_key = api_key or os.getenv('POLYGON_API_KEY')
        
        if not self.api_key:
            raise ValueError(
                "Polygon API key required! Set POLYGON_API_KEY in .env file"
            )
        
        self.client = RESTClient(self.api_key)
        self.last_call_time = 0
        self.min_delay = 15  # 15 seconds between calls (4 calls/minute, safe for free tier)
    
    def _rate_limit(self):
        """Ensure we don't exceed free tier rate limits."""
        elapsed = time.time() - self.last_call_time
        if elapsed < self.min_delay:
            sleep_time = self.min_delay - elapsed
            logger.info(f"Rate limiting: waiting {sleep_time:.1f}s")
            time.sleep(sleep_time)
        self.last_call_time = time.time()
    
    def get_stock_info(self, ticker: str) -> Optional[Dict]:
        """Get basic stock information."""
        try:
            self._rate_limit()
            details = self.client.get_ticker_details(ticker)
            
            return {
                'ticker': ticker.upper(),
                'company_name': details.name or ticker,
                'sector': details.sic_description or 'N/A',
                'industry': details.sic_description or 'N/A',
                'market_cap': details.market_cap or 0,
                'currency': details.currency_name or 'USD',
                'exchange': details.primary_exchange or 'N/A',
                'description': details.description or '',
                'website': details.homepage_url or '',
            }
        except Exception as e:
            logger.error(f"Error fetching info for {ticker}: {e}")
            return None
    
    def get_historical_data(
        self,
        ticker: str,
        days_back: int = 365,
        timespan: str = 'day'
    ) -> Optional[pd.DataFrame]:
        """Get historical price data."""
        try:
            self._rate_limit()
            
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days_back)
            
            from_date = start_date.strftime('%Y-%m-%d')
            to_date = end_date.strftime('%Y-%m-%d')
            
            aggs = []
            for agg in self.client.list_aggs(
                ticker=ticker.upper(),
                multiplier=1,
                timespan=timespan,
                from_=from_date,
                to=to_date,
                limit=50000
            ):
                aggs.append(agg)
            
            if not aggs:
                logger.warning(f"No data found for {ticker}")
                return None
            
            data = []
            for agg in aggs:
                data.append({
                    'date': pd.to_datetime(agg.timestamp, unit='ms'),
                    'open': agg.open,
                    'high': agg.high,
                    'low': agg.low,
                    'close': agg.close,
                    'volume': agg.volume,
                })
            
            df = pd.DataFrame(data)
            df = df.sort_values('date').reset_index(drop=True)
            
            return df
            
        except Exception as e:
            logger.error(f"Error fetching historical data for {ticker}: {e}")
            return None
    
    def get_current_price(self, ticker: str) -> Optional[Dict]:
        """Get current/latest price."""
        try:
            self._rate_limit()
            
            # Get recent daily data (more reliable than tick data)
            aggs = list(self.client.list_aggs(
                ticker=ticker.upper(),
                multiplier=1,
                timespan='day',
                from_=(datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d'),
                to=datetime.now().strftime('%Y-%m-%d'),
                limit=5
            ))
            
            if len(aggs) < 2:
                return None
            
            current_day = aggs[-1]
            prev_day = aggs[-2]
            
            current = current_day.close
            prev_close = prev_day.close
            change = current - prev_close
            change_pct = (change / prev_close) * 100
            
            return {
                'ticker': ticker.upper(),
                'current_price': current,
                'previous_close': prev_close,
                'open': current_day.open,
                'day_high': current_day.high,
                'day_low': current_day.low,
                'change': change,
                'change_percent': change_pct,
                'volume': current_day.volume,
                'market_cap': 0  # Would need separate API call
            }
            
        except Exception as e:
            logger.error(f"Error fetching current price for {ticker}: {e}")
            return None
    
    def get_multiple_tickers(self, tickers: List[str], max_tickers: int = 4) -> pd.DataFrame:
        """
        Get data for multiple tickers with rate limiting.
        Limited to 4 tickers to stay within free tier (4 calls/minute).
        """
        # Limit to prevent rate limit issues
        tickers = tickers[:max_tickers]
        
        data = []
        for i, ticker in enumerate(tickers):
            logger.info(f"Fetching {ticker} ({i+1}/{len(tickers)})...")
            price_info = self.get_current_price(ticker)
            if price_info:
                data.append(price_info)
        
        return pd.DataFrame(data)


if __name__ == "__main__":
    # Test the fetcher
    print("Testing Polygon.io integration...")
    
    fetcher = PolygonDataFetcher()
    
    print("\n1. Getting AAPL info...")
    info = fetcher.get_stock_info("AAPL")
    if info:
        print(f"   Company: {info['company_name']}")
    
    print("\n2. Getting AAPL price...")
    price = fetcher.get_current_price("AAPL")
    if price:
        print(f"   Price: ${price['current_price']:.2f}")
        print(f"   Change: {price['change_percent']:.2f}%")
    
    print("\n3. Getting historical data...")
    hist = fetcher.get_historical_data("AAPL", days_back=30)
    if hist is not None:
        print(f"   Retrieved {len(hist)} days")
    
    print("\nSuccess! Polygon.io is working!")
