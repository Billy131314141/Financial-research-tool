"""
Configuration settings for the Financial Research Tool.
"""
import os

# Database Configuration
DATABASE_PATH = "data/financial_research.db"

# API Configuration
# Note: For production, use environment variables for API keys
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")  # Get from https://newsapi.org

# Default Stocks/Indices for Demo
# Reduced to 8 stocks to avoid Yahoo Finance API rate limiting
DEFAULT_STOCKS = [
    "AAPL", "MSFT", "GOOGL", "AMZN",
    "TSLA", "NVDA", "JPM", "V"
]

DEFAULT_INDICES = {
    "^GSPC": "S&P 500",
    "^DJI": "Dow Jones Industrial Average",
    "^IXIC": "NASDAQ Composite"
}

# Major Sectors
SECTORS = [
    "Technology",
    "Healthcare",
    "Financial Services",
    "Consumer Cyclical",
    "Industrials",
    "Communication Services",
    "Consumer Defensive",
    "Energy",
    "Utilities",
    "Real Estate",
    "Basic Materials"
]

# Data Update Configuration
UPDATE_FREQUENCY_HOURS = 1  # How often to update market data
HISTORICAL_DATA_YEARS = 10  # Years of historical data to fetch

# Chart Configuration
DEFAULT_CHART_HEIGHT = 500
DEFAULT_CHART_TEMPLATE = "plotly_white"

# Date Ranges for Analysis
DATE_RANGES = {
    "1D": 1,
    "5D": 5,
    "1M": 30,
    "3M": 90,
    "6M": 180,
    "YTD": "ytd",
    "1Y": 365,
    "5Y": 1825,
    "10Y": 3650,
    "MAX": "max"
}

# Application Settings
APP_TITLE = "Financial Research Tool Demo"
APP_ICON = "📊"
PAGE_LAYOUT = "wide"

# CSV Export Settings
CSV_EXPORT_PATH = "data/exports/"
CSV_DATE_FORMAT = "%Y-%m-%d"

# Cache Settings
CACHE_TTL = 3600  # Cache time-to-live in seconds (1 hour)

# Alert Types
ALERT_TYPES = [
    "PRICE_ABOVE",
    "PRICE_BELOW",
    "VOLUME_SPIKE",
    "PERCENT_CHANGE"
]

# Color Scheme (from styling guidelines)
COLORS = {
    "positive": "#4CAF50",  # Green
    "negative": "#F44336",  # Red
    "info": "#2196F3",      # Blue
    "warning": "#FFC107",   # Amber
    "text_dark": "#212121",
    "text_body": "#424242",
    "text_subtle": "#757575",
    "background": "#FFFFFF",
    "background_secondary": "#F5F5F5",
    "border": "#E0E0E0"
}


