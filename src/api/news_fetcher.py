"""
Real News and Earnings Call Data Fetcher
Integrates NewsAPI and Financial Modeling Prep (FMP) APIs
"""
import os
import requests
from newsapi import NewsApiClient
from datetime import datetime, timedelta
from typing import List, Optional, Dict
import logging
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class NewsDataFetcher:
    """Fetches financial news and earnings call transcripts from multiple sources."""
    
    def __init__(self):
        """Initialize with API keys from environment variables."""
        self.news_api_key = os.getenv('NEWS_API_KEY')
        self.fmp_api_key = os.getenv('FMP_API_KEY')
        
        # Initialize NewsAPI client
        self.newsapi_client = None
        if self.news_api_key:
            try:
                self.newsapi_client = NewsApiClient(api_key=self.news_api_key)
                logger.info("NewsAPI client initialized")
            except Exception as e:
                logger.error(f"Failed to initialize NewsAPI: {e}")
        
        # Rate limiting
        self.last_news_call = 0
        self.last_fmp_call = 0
        self.news_call_interval = 1  # 1 second between calls
        self.fmp_call_interval = 0.5  # 0.5 seconds between calls
    
    def _rate_limit_wait(self, api_type: str = 'news'):
        """Ensure API calls respect rate limits."""
        if api_type == 'news':
            elapsed = time.time() - self.last_news_call
            if elapsed < self.news_call_interval:
                time.sleep(self.news_call_interval - elapsed)
            self.last_news_call = time.time()
        elif api_type == 'fmp':
            elapsed = time.time() - self.last_fmp_call
            if elapsed < self.fmp_call_interval:
                time.sleep(self.fmp_call_interval - elapsed)
            self.last_fmp_call = time.time()
    
    def fetch_news_from_newsapi(
        self, 
        ticker: str, 
        company_name: str, 
        days_back: int = 7
    ) -> List[str]:
        """
        Fetch news headlines from NewsAPI.
        
        Args:
            ticker: Stock ticker symbol
            company_name: Company name for search
            days_back: How many days back to search
            
        Returns:
            List of news headlines
        """
        if not self.newsapi_client or not self.news_api_key:
            logger.warning("NewsAPI not configured")
            return []
        
        try:
            self._rate_limit_wait('news')
            
            # Calculate date range
            from_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
            
            # Search for company news
            articles = self.newsapi_client.get_everything(
                q=f'"{ticker}" OR "{company_name}"',
                language='en',
                from_param=from_date,
                sort_by='publishedAt',
                page_size=10
            )
            
            if articles and articles.get('articles'):
                headlines = [article['title'] for article in articles['articles']]
                logger.info(f"Fetched {len(headlines)} headlines from NewsAPI for {ticker}")
                return headlines
            
        except Exception as e:
            logger.error(f"NewsAPI fetch error for {ticker}: {e}")
        
        return []
    
    def fetch_news_from_fmp(self, ticker: str, days_back: int = 7) -> List[str]:
        """
        Fetch news from Financial Modeling Prep API.
        
        Args:
            ticker: Stock ticker symbol
            days_back: How many days back to search
            
        Returns:
            List of news headlines
        """
        if not self.fmp_api_key:
            logger.warning("FMP API not configured")
            return []
        
        try:
            self._rate_limit_wait('fmp')
            
            # FMP stock news endpoint
            url = f'https://financialmodelingprep.com/api/v3/stock_news'
            params = {
                'tickers': ticker,
                'limit': 10,
                'apikey': self.fmp_api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data and isinstance(data, list):
                # Filter by date
                cutoff_date = datetime.now() - timedelta(days=days_back)
                headlines = []
                
                for article in data:
                    pub_date = datetime.strptime(article['publishedDate'][:10], '%Y-%m-%d')
                    if pub_date >= cutoff_date:
                        headlines.append(article['title'])
                
                logger.info(f"Fetched {len(headlines)} headlines from FMP for {ticker}")
                return headlines
            
        except Exception as e:
            logger.error(f"FMP news fetch error for {ticker}: {e}")
        
        return []
    
    def fetch_earnings_transcript(self, ticker: str, quarter: Optional[int] = None, 
                                  year: Optional[int] = None) -> Optional[str]:
        """
        Fetch earnings call transcript from FMP.
        
        Args:
            ticker: Stock ticker symbol
            quarter: Specific quarter (1-4), if None gets latest
            year: Specific year, if None gets latest
            
        Returns:
            Earnings call transcript text, or None if not found
        """
        if not self.fmp_api_key:
            logger.warning("FMP API not configured for transcripts")
            return None
        
        try:
            self._rate_limit_wait('fmp')
            
            # FMP earnings call transcript endpoint
            url = f'https://financialmodelingprep.com/api/v3/earning_call_transcript/{ticker}'
            params = {'apikey': self.fmp_api_key}
            
            if quarter and year:
                params['quarter'] = quarter
                params['year'] = year
            
            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            
            if data and isinstance(data, list) and len(data) > 0:
                # Get the most recent transcript
                transcript = data[0].get('content', '')
                if transcript:
                    logger.info(f"Fetched earnings transcript for {ticker} (Q{data[0].get('quarter', '?')} {data[0].get('year', '?')})")
                    return transcript
            
        except Exception as e:
            logger.error(f"FMP transcript fetch error for {ticker}: {e}")
        
        return None
    
    def fetch_company_news(
        self, 
        ticker: str, 
        company_name: str, 
        days_back: int = 7,
        max_articles: int = 10
    ) -> List[str]:
        """
        Fetch news from all available sources with fallback.
        
        Args:
            ticker: Stock ticker symbol
            company_name: Company name
            days_back: Days to look back
            max_articles: Maximum number of articles to return
            
        Returns:
            List of news headlines
        """
        all_headlines = []
        
        # Try NewsAPI first (better quality for general news)
        newsapi_headlines = self.fetch_news_from_newsapi(ticker, company_name, days_back)
        all_headlines.extend(newsapi_headlines)
        
        # If we don't have enough, try FMP
        if len(all_headlines) < 5:
            fmp_headlines = self.fetch_news_from_fmp(ticker, days_back)
            all_headlines.extend(fmp_headlines)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_headlines = []
        for headline in all_headlines:
            if headline.lower() not in seen:
                seen.add(headline.lower())
                unique_headlines.append(headline)
        
        # Return up to max_articles
        result = unique_headlines[:max_articles]
        
        if result:
            logger.info(f"Fetched total {len(result)} unique headlines for {ticker}")
        else:
            logger.warning(f"No headlines found for {ticker}, may need to use sample data")
        
        return result


# Global instance
_fetcher = None

def get_news_fetcher() -> NewsDataFetcher:
    """Get or create global news fetcher instance."""
    global _fetcher
    if _fetcher is None:
        _fetcher = NewsDataFetcher()
    return _fetcher


# Convenience functions
def fetch_news(ticker: str, company_name: str, days_back: int = 7) -> List[str]:
    """Fetch news headlines for a company."""
    fetcher = get_news_fetcher()
    return fetcher.fetch_company_news(ticker, company_name, days_back)


def fetch_earnings_transcript(ticker: str) -> Optional[str]:
    """Fetch latest earnings call transcript."""
    fetcher = get_news_fetcher()
    return fetcher.fetch_earnings_transcript(ticker)


if __name__ == "__main__":
    # Test the fetcher
    import json
    
    print("=" * 70)
    print("Testing News Data Fetcher")
    print("=" * 70)
    print()
    
    # Test with AAPL
    ticker = "AAPL"
    company = "Apple Inc"
    
    print(f"Fetching news for {ticker} ({company})...")
    headlines = fetch_news(ticker, company, days_back=7)
    
    if headlines:
        print(f"\n✅ Found {len(headlines)} headlines:")
        for i, headline in enumerate(headlines, 1):
            print(f"{i}. {headline}")
    else:
        print("❌ No headlines found")
    
    print("\n" + "=" * 70)
    print(f"Fetching earnings transcript for {ticker}...")
    transcript = fetch_earnings_transcript(ticker)
    
    if transcript:
        print(f"✅ Found transcript ({len(transcript)} characters)")
        print(f"Preview: {transcript[:200]}...")
    else:
        print("❌ No transcript found")
    
    print("\n" + "=" * 70)
    print("Test complete!")


