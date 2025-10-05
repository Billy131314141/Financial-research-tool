"""
Data fetcher module for retrieving financial data from various APIs.
Primarily uses yfinance for stock and market data.
"""
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, List, Dict
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataFetcher:
    """Handles fetching financial data from external APIs."""
    
    def __init__(self):
        """Initialize the data fetcher."""
        pass
    
    def get_stock_info(self, ticker: str) -> Optional[Dict]:
        """
        Fetch basic information about a stock.
        
        Args:
            ticker: Stock ticker symbol (e.g., 'AAPL')
            
        Returns:
            Dictionary with stock information or None if error
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            return {
                'ticker': ticker,
                'company_name': info.get('longName', ticker),
                'sector': info.get('sector', 'N/A'),
                'industry': info.get('industry', 'N/A'),
                'market_cap': info.get('marketCap', 0),
                'currency': info.get('currency', 'USD'),
                'exchange': info.get('exchange', 'N/A'),
                'description': info.get('longBusinessSummary', ''),
                'website': info.get('website', ''),
                'pe_ratio': info.get('trailingPE', None),
                'dividend_yield': info.get('dividendYield', None),
                'fifty_two_week_high': info.get('fiftyTwoWeekHigh', None),
                'fifty_two_week_low': info.get('fiftyTwoWeekLow', None)
            }
        except Exception as e:
            logger.error(f"Error fetching info for {ticker}: {e}")
            return None
    
    def get_historical_data(
        self, 
        ticker: str, 
        period: str = "1y", 
        interval: str = "1d"
    ) -> Optional[pd.DataFrame]:
        """
        Fetch historical price data for a stock.
        
        Args:
            ticker: Stock ticker symbol
            period: Data period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
            interval: Data interval (1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo)
            
        Returns:
            DataFrame with historical price data or None if error
        """
        try:
            stock = yf.Ticker(ticker)
            df = stock.history(period=period, interval=interval)
            
            if df.empty:
                logger.warning(f"No historical data found for {ticker}")
                return None
                
            # Reset index to make Date a column
            df.reset_index(inplace=True)
            
            # Rename columns to match database schema
            df.columns = [col.lower().replace(' ', '_') for col in df.columns]
            
            return df
        except Exception as e:
            logger.error(f"Error fetching historical data for {ticker}: {e}")
            return None
    
    def get_current_price(self, ticker: str) -> Optional[Dict]:
        """
        Get current/latest price information for a stock.
        
        Args:
            ticker: Stock ticker symbol
            
        Returns:
            Dictionary with current price info or None if error
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            return {
                'ticker': ticker,
                'current_price': info.get('currentPrice', info.get('regularMarketPrice', 0)),
                'previous_close': info.get('previousClose', 0),
                'open': info.get('open', 0),
                'day_high': info.get('dayHigh', 0),
                'day_low': info.get('dayLow', 0),
                'volume': info.get('volume', 0),
                'market_cap': info.get('marketCap', 0),
                'change': info.get('regularMarketChange', 0),
                'change_percent': info.get('regularMarketChangePercent', 0)
            }
        except Exception as e:
            logger.error(f"Error fetching current price for {ticker}: {e}")
            return None
    
    def get_multiple_tickers(self, tickers: List[str]) -> pd.DataFrame:
        """
        Fetch current data for multiple tickers at once.
        
        Args:
            tickers: List of ticker symbols
            
        Returns:
            DataFrame with data for all tickers
        """
        try:
            data = []
            for ticker in tickers:
                price_info = self.get_current_price(ticker)
                if price_info:
                    data.append(price_info)
            
            return pd.DataFrame(data)
        except Exception as e:
            logger.error(f"Error fetching multiple tickers: {e}")
            return pd.DataFrame()
    
    def get_market_indices(self, indices: List[str]) -> pd.DataFrame:
        """
        Fetch data for major market indices.
        
        Args:
            indices: List of index symbols (e.g., ['^GSPC', '^DJI'])
            
        Returns:
            DataFrame with index data
        """
        return self.get_multiple_tickers(indices)
    
    def get_top_gainers_losers(self, tickers: List[str]) -> Dict[str, pd.DataFrame]:
        """
        Identify top gainers and losers from a list of tickers.
        
        Args:
            tickers: List of ticker symbols to analyze
            
        Returns:
            Dictionary with 'gainers' and 'losers' DataFrames
        """
        try:
            df = self.get_multiple_tickers(tickers)
            
            if df.empty:
                return {'gainers': pd.DataFrame(), 'losers': pd.DataFrame()}
            
            # Sort by change percent
            df_sorted = df.sort_values('change_percent', ascending=False)
            
            # Get top 5 gainers and losers
            gainers = df_sorted.head(5)
            losers = df_sorted.tail(5).sort_values('change_percent')
            
            return {
                'gainers': gainers,
                'losers': losers
            }
        except Exception as e:
            logger.error(f"Error identifying gainers/losers: {e}")
            return {'gainers': pd.DataFrame(), 'losers': pd.DataFrame()}
    
    def get_sector_performance(self, tickers: List[str]) -> pd.DataFrame:
        """
        Calculate sector performance based on provided tickers.
        
        Args:
            tickers: List of ticker symbols
            
        Returns:
            DataFrame with sector performance summary
        """
        try:
            sector_data = []
            
            for ticker in tickers:
                info = self.get_stock_info(ticker)
                price = self.get_current_price(ticker)
                
                if info and price:
                    sector_data.append({
                        'ticker': ticker,
                        'sector': info['sector'],
                        'change_percent': price['change_percent']
                    })
            
            df = pd.DataFrame(sector_data)
            
            if df.empty:
                return df
            
            # Calculate average performance by sector
            sector_performance = df.groupby('sector')['change_percent'].agg([
                ('avg_change', 'mean'),
                ('count', 'count')
            ]).reset_index()
            
            sector_performance = sector_performance.sort_values('avg_change', ascending=False)
            
            return sector_performance
        except Exception as e:
            logger.error(f"Error calculating sector performance: {e}")
            return pd.DataFrame()
    
    def download_historical_bulk(
        self, 
        tickers: List[str], 
        period: str = "10y"
    ) -> Dict[str, pd.DataFrame]:
        """
        Download historical data for multiple tickers (bulk operation).
        
        Args:
            tickers: List of ticker symbols
            period: Data period to fetch
            
        Returns:
            Dictionary mapping tickers to their historical DataFrames
        """
        results = {}
        
        for ticker in tickers:
            logger.info(f"Downloading historical data for {ticker}...")
            df = self.get_historical_data(ticker, period=period)
            if df is not None:
                results[ticker] = df
        
        logger.info(f"Downloaded data for {len(results)}/{len(tickers)} tickers")
        return results


if __name__ == "__main__":
    # Test the data fetcher
    fetcher = DataFetcher()
    
    # Test single stock
    print("Testing AAPL data fetch...")
    info = fetcher.get_stock_info("AAPL")
    print(f"Company: {info['company_name']}")
    
    price = fetcher.get_current_price("AAPL")
    print(f"Current Price: ${price['current_price']:.2f}")
    
    # Test historical data
    hist = fetcher.get_historical_data("AAPL", period="1mo")
    print(f"\nHistorical data shape: {hist.shape}")
    print(hist.head())


