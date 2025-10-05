#!/usr/bin/env python3
import os
from dotenv import load_dotenv

print("\n" + "=" * 70)
print("🔍 MANUAL API TEST - Checking Real Data Access")
print("=" * 70 + "\n")

# Load environment variables from .env file
load_dotenv()

print("Step 1: Checking API Keys...")
print("-" * 70)

news_key = os.getenv('NEWS_API_KEY')
fmp_key = os.getenv('FMP_API_KEY')
polygon_key = os.getenv('POLYGON_API_KEY')

if news_key:
    print(f"✅ NewsAPI Key: {news_key[:25]}...")
else:
    print("❌ NewsAPI Key NOT loaded")

if fmp_key:
    print(f"✅ FMP Key: {fmp_key[:25]}...")
else:
    print("❌ FMP Key NOT loaded")

if polygon_key:
    print(f"✅ Polygon Key: {polygon_key[:25]}...")
else:
    print("❌ Polygon Key NOT loaded")

print("\n" + "=" * 70)
print("Step 2: Testing NewsAPI (fetching real AAPL news)...")
print("=" * 70 + "\n")

try:
    from newsapi import NewsApiClient
    newsapi = NewsApiClient(api_key=news_key)
    
    print("📡 Calling NewsAPI for AAPL news...")
    result = newsapi.get_everything(
        q='AAPL OR "Apple Inc"',
        language='en',
        sort_by='publishedAt',
        page_size=5
    )
    
    if result and result.get('articles'):
        headlines = [a['title'] for a in result['articles']]
        print(f"\n✅ SUCCESS! NewsAPI returned {len(headlines)} real headlines:\n")
        for i, headline in enumerate(headlines, 1):
            print(f"   {i}. {headline}")
    else:
        print("\n⚠️  NewsAPI returned no articles")
        
except Exception as e:
    print(f"\n❌ NewsAPI ERROR: {e}")

print("\n" + "=" * 70)
print("Step 3: Testing FMP API (fetching real AAPL news)...")
print("=" * 70 + "\n")

try:
    import requests
    
    url = 'https://financialmodelingprep.com/api/v3/stock_news'
    params = {
        'tickers': 'AAPL',
        'limit': 5,
        'apikey': fmp_key
    }
    
    print("📡 Calling FMP API for AAPL news...")
    response = requests.get(url, params=params, timeout=10)
    data = response.json()
    
    if data and isinstance(data, list) and len(data) > 0:
        print(f"\n✅ SUCCESS! FMP returned {len(data)} real news items:\n")
        for i, item in enumerate(data[:5], 1):
            print(f"   {i}. {item['title']}")
    else:
        print("\n⚠️  FMP returned unexpected data")
        
except Exception as e:
    print(f"\n❌ FMP API ERROR: {e}")

print("\n" + "=" * 70)
print("Step 4: Testing news_fetcher module...")
print("=" * 70 + "\n")

try:
    import sys
    sys.path.append('.')
    from src.api.news_fetcher import get_news_fetcher
    
    print("📡 Testing news_fetcher.py module...")
    fetcher = get_news_fetcher()
    headlines = fetcher.fetch_company_news('AAPL', 'Apple Inc', days_back=7, max_articles=5)
    
    if headlines:
        print(f"\n✅ SUCCESS! news_fetcher module returned {len(headlines)} headlines:\n")
        for i, h in enumerate(headlines, 1):
            print(f"   {i}. {h}")
    else:
        print("\n⚠️  news_fetcher returned no headlines")
        
except Exception as e:
    print(f"\n❌ news_fetcher ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("✅ TEST COMPLETE!")
print("=" * 70 + "\n")

print("📊 Summary:")
print("   • If you see ✅ SUCCESS messages above, APIs are working!")
print("   • Your app will now fetch real data")
print("\n🚀 Restart your Streamlit app to see real headlines!")
print("   Command: streamlit run main.py\n")
