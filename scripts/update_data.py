"""
Data update script - fetches and updates financial data.
Run this script periodically to keep data fresh.
"""
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.api.data_fetcher import DataFetcher
from src.utils.database import Database
from config.settings import DEFAULT_STOCKS, DEFAULT_INDICES
from datetime import datetime
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def update_stock_data():
    """Update stock data for default stocks."""
    logger.info("Starting stock data update...")
    
    fetcher = DataFetcher()
    db = Database()
    db.connect()
    cursor = db.conn.cursor()
    
    for ticker in DEFAULT_STOCKS:
        try:
            logger.info(f"Updating {ticker}...")
            
            # Get stock info
            info = fetcher.get_stock_info(ticker)
            if info:
                # Insert or update company
                cursor.execute("""
                    INSERT OR REPLACE INTO Companies 
                    (ticker, company_name, exchange, sector, industry, market_cap, currency, last_updated)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    ticker,
                    info['company_name'],
                    info['exchange'],
                    info['sector'],
                    info['industry'],
                    info['market_cap'],
                    info['currency'],
                    datetime.now()
                ))
            
            # Get historical data (last 30 days)
            hist_data = fetcher.get_historical_data(ticker, period="1mo")
            
            if hist_data is not None and not hist_data.empty:
                # Get company_id
                cursor.execute("SELECT company_id FROM Companies WHERE ticker = ?", (ticker,))
                result = cursor.fetchone()
                
                if result:
                    company_id = result[0]
                    
                    # Insert price data
                    for _, row in hist_data.iterrows():
                        cursor.execute("""
                            INSERT OR REPLACE INTO StockPrices
                            (company_id, timestamp, open, high, low, close, volume, adjusted_close)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """, (
                            company_id,
                            row['date'],
                            row.get('open'),
                            row.get('high'),
                            row.get('low'),
                            row.get('close'),
                            row.get('volume'),
                            row.get('adjusted_close', row.get('close'))
                        ))
            
            db.conn.commit()
            logger.info(f"✓ Updated {ticker}")
        
        except Exception as e:
            logger.error(f"✗ Error updating {ticker}: {e}")
    
    db.close()
    logger.info("Stock data update complete!")


def update_indices_data():
    """Update market indices data."""
    logger.info("Starting indices data update...")
    
    fetcher = DataFetcher()
    db = Database()
    db.connect()
    cursor = db.conn.cursor()
    
    for symbol, name in DEFAULT_INDICES.items():
        try:
            logger.info(f"Updating {name}...")
            
            # Insert or update index
            cursor.execute("""
                INSERT OR REPLACE INTO MarketIndices
                (symbol, index_name, last_updated)
                VALUES (?, ?, ?)
            """, (symbol, name, datetime.now()))
            
            # Get historical data
            hist_data = fetcher.get_historical_data(symbol, period="1mo")
            
            if hist_data is not None and not hist_data.empty:
                # Get index_id
                cursor.execute("SELECT index_id FROM MarketIndices WHERE symbol = ?", (symbol,))
                result = cursor.fetchone()
                
                if result:
                    index_id = result[0]
                    
                    # Insert price data
                    for _, row in hist_data.iterrows():
                        cursor.execute("""
                            INSERT OR REPLACE INTO IndexPrices
                            (index_id, timestamp, open, high, low, close, volume)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                        """, (
                            index_id,
                            row['date'],
                            row.get('open'),
                            row.get('high'),
                            row.get('low'),
                            row.get('close'),
                            row.get('volume', 0)
                        ))
            
            db.conn.commit()
            logger.info(f"✓ Updated {name}")
        
        except Exception as e:
            logger.error(f"✗ Error updating {name}: {e}")
    
    db.close()
    logger.info("Indices data update complete!")


if __name__ == "__main__":
    print("=" * 60)
    print("Financial Research Tool - Data Update")
    print("=" * 60)
    print()
    
    # Update stocks
    update_stock_data()
    print()
    
    # Update indices
    update_indices_data()
    print()
    
    print("=" * 60)
    print("Data update completed!")
    print("=" * 60)


