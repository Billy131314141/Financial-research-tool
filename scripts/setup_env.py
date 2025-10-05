"""
Environment setup script - initialize the project.
"""
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.database import initialize_database
from config.settings import DEFAULT_STOCKS
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def setup_environment():
    """Setup the project environment."""
    print("=" * 60)
    print("Financial Research Tool - Environment Setup")
    print("=" * 60)
    print()
    
    # Step 1: Initialize database
    print("Step 1: Initializing database...")
    try:
        initialize_database()
        print("✓ Database initialized successfully!")
    except Exception as e:
        print(f"✗ Error initializing database: {e}")
        return False
    
    print()
    
    # Step 2: Create necessary directories
    print("Step 2: Creating necessary directories...")
    directories = [
        "data/raw/stocks",
        "data/raw/fundamentals",
        "data/raw/indices",
        "data/raw/news",
        "data/processed/stocks",
        "data/processed/sentiment",
        "data/cache",
        "data/exports"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created {directory}")
    
    print()
    
    # Step 3: Download NLTK data (for sentiment analysis)
    print("Step 3: Downloading NLTK data for sentiment analysis...")
    try:
        import nltk
        nltk.download('punkt', quiet=True)
        nltk.download('brown', quiet=True)
        print("✓ NLTK data downloaded")
    except Exception as e:
        print(f"⚠ Warning: Could not download NLTK data: {e}")
    
    print()
    
    # Step 4: Fetch initial data (optional)
    print("Step 4: Would you like to fetch initial market data? (This may take a few minutes)")
    response = input("Fetch initial data? (y/n): ").lower()
    
    if response == 'y':
        print("Fetching initial data...")
        try:
            from scripts.update_data import update_stock_data, update_indices_data
            update_indices_data()
            # Fetch data for first 5 stocks only to save time
            print(f"Fetching data for top 5 stocks (out of {len(DEFAULT_STOCKS)})...")
            from config.settings import DEFAULT_STOCKS
            from src.api.data_fetcher import DataFetcher
            fetcher = DataFetcher()
            for ticker in DEFAULT_STOCKS[:5]:
                print(f"  Fetching {ticker}...")
                fetcher.get_historical_data(ticker, period="1y")
            print("✓ Initial data fetched!")
        except Exception as e:
            print(f"⚠ Warning: Could not fetch all initial data: {e}")
    
    print()
    print("=" * 60)
    print("✓ Setup complete!")
    print("=" * 60)
    print()
    print("To run the application, execute:")
    print("  streamlit run main.py")
    print()
    
    return True


if __name__ == "__main__":
    setup_environment()


