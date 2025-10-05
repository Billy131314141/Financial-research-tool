"""
NewsData Fetcher - Simplified version focusing only on newsdata.io
No FMP endpoints (may not work on free tier)
"""
import requests
import streamlit as st
from datetime import datetime, timedelta
import time


class NewsDataFetcher:
    """Fetcher for newsdata.io API only"""
    
    def __init__(self, news_api_key: str):
        """
        Initialize NewsDataFetcher
        
        Args:
            news_api_key: API key for newsdata.io
        """
        self.news_api_key = news_api_key
        self.newsdata_base_url = 'https://newsdata.io/api/1/news'
        
    def _rate_limit_wait(self, wait_time: float = 0.2):
        """Wait between API calls to avoid rate limits"""
        time.sleep(wait_time)
    
    @st.cache_data(ttl=3600)
    def get_news(_self, ticker: str, company_name: str = None, days_back: int = 7, max_results: int = 10):
        """
        Fetch news from newsdata.io
        
        Args:
            ticker: Stock ticker symbol
            company_name: Optional company name for better search results
            days_back: Number of days to look back (not always supported)
            max_results: Maximum number of results to return
            
        Returns:
            List of news articles or empty list on error
        """
        try:
            # Build search query
            query = ticker
            if company_name:
                query = f"{ticker} OR {company_name}"
            
            params = {
                'apikey': _self.news_api_key,
                'q': query,
                'language': 'en',
                'category': 'business'
            }
            
            response = requests.get(_self.newsdata_base_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('status') == 'success':
                    results = data.get('results', [])
                    
                    # Format news articles
                    news_list = []
                    for article in results[:max_results]:
                        news_list.append({
                            'title': article.get('title', 'No title'),
                            'description': article.get('description', 'No description'),
                            'url': article.get('link', ''),
                            'source': article.get('source_id', 'Unknown'),
                            'published_at': article.get('pubDate', str(datetime.now())),
                            'content': article.get('content', article.get('description', '')),
                        })
                    
                    return news_list
                else:
                    print(f"newsdata.io API error: {data}")
                    return []
            else:
                print(f"newsdata.io HTTP error: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"Error fetching news: {e}")
            return []
    
    def get_sample_news(self, ticker: str = "AAPL", count: int = 5):
        """
        Get sample news data for testing (fallback when API fails)
        
        Args:
            ticker: Stock ticker
            count: Number of sample articles
            
        Returns:
            List of sample news articles
        """
        sample_news = []
        for i in range(count):
            sample_news.append({
                'title': f'{ticker} Sample News Article {i+1}',
                'description': f'This is a sample news article about {ticker}. In production, this would contain real financial news.',
                'url': 'https://example.com',
                'source': 'Sample Source',
                'published_at': str(datetime.now() - timedelta(days=i)),
                'content': f'Sample content for {ticker} news article {i+1}. This is placeholder text that would normally contain the full article content.',
            })
        return sample_news
