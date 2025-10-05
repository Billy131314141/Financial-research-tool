#!/usr/bin/env python3
"""
Update Bloomberg dashboard to use real news and earnings data
"""
import sys

print("🔧 Updating Bloomberg dashboard to use real data sources...")

# Read the file
with open('app/bloomberg_dashboard.py', 'r') as f:
    content = f.read()

# Add the import at the top (after other imports)
import_to_add = "from src.api.news_fetcher import get_news_fetcher"

if import_to_add not in content:
    # Find the line with "from src.analysis.finbert_sentiment import get_analyzer"
    import_line = "from src.analysis.finbert_sentiment import get_analyzer"
    if import_line in content:
        content = content.replace(
            import_line,
            f"{import_line}\n{import_to_add}"
        )
        print("✅ Added news_fetcher import")
    else:
        print("⚠️  Could not find import location")

# Replace the generate_sample_news function
old_news_func = '''def generate_sample_news(ticker: str, company_name: str) -> list:
    """Generate sample news headlines for sentiment analysis demo"""
    # Sample financial news templates
    return [
        f"{company_name} reports strong quarterly earnings, beating analyst expectations significantly.",
        f"Analysts upgrade {ticker} to buy rating citing robust growth potential.",
        f"{company_name} announces innovative product launch, stock surges in pre-market trading.",
        f"Market volatility impacts {ticker} amid concerns over rising interest rates.",
        f"{company_name} CEO discusses long-term strategy and growth initiatives.",
        f"Industry challenges pose potential headwinds for {ticker} in coming quarters.",
        f"{company_name} expands market share with strategic partnerships and acquisitions.",
        f"Regulatory concerns raise questions about {ticker}'s future profitability.",
        f"{company_name} demonstrates resilience with consistent revenue growth.",
        f"Economic uncertainty leads to cautious outlook for {ticker} this quarter."
    ]'''

new_news_func = '''def generate_sample_news(ticker: str, company_name: str) -> list:
    """Fetch real news headlines (with sample data fallback)"""
    try:
        # Try to fetch real news
        fetcher = get_news_fetcher()
        real_headlines = fetcher.fetch_company_news(ticker, company_name, days_back=7, max_articles=10)
        
        if real_headlines and len(real_headlines) >= 3:
            print(f"✅ Using {len(real_headlines)} real headlines for {ticker}")
            return real_headlines
        else:
            print(f"⚠️  Only found {len(real_headlines)} headlines, using sample data")
    except Exception as e:
        print(f"⚠️  Error fetching news: {e}, using sample data")
    
    # Fallback to sample data
    return [
        f"{company_name} reports strong quarterly earnings, beating analyst expectations significantly.",
        f"Analysts upgrade {ticker} to buy rating citing robust growth potential.",
        f"{company_name} announces innovative product launch, stock surges in pre-market trading.",
        f"Market volatility impacts {ticker} amid concerns over rising interest rates.",
        f"{company_name} CEO discusses long-term strategy and growth initiatives.",
        f"Industry challenges pose potential headwinds for {ticker} in coming quarters.",
        f"{company_name} expands market share with strategic partnerships and acquisitions.",
        f"Regulatory concerns raise questions about {ticker}'s future profitability.",
        f"{company_name} demonstrates resilience with consistent revenue growth.",
        f"Economic uncertainty leads to cautious outlook for {ticker} this quarter."
    ]'''

if old_news_func in content:
    content = content.replace(old_news_func, new_news_func)
    print("✅ Updated generate_sample_news() to use real data")
else:
    print("⚠️  Could not find generate_sample_news function")

# Replace the generate_sample_earnings_call function
old_earnings_func_start = '''def generate_sample_earnings_call(ticker: str, company_name: str) -> str:
    """Generate sample earnings call transcript for sentiment analysis demo"""
    return f"""'''

new_earnings_func = '''def generate_sample_earnings_call(ticker: str, company_name: str) -> str:
    """Fetch real earnings call transcript (with sample data fallback)"""
    try:
        # Try to fetch real transcript
        fetcher = get_news_fetcher()
        real_transcript = fetcher.fetch_earnings_transcript(ticker)
        
        if real_transcript and len(real_transcript) > 500:
            print(f"✅ Using real earnings transcript for {ticker} ({len(real_transcript)} chars)")
            return real_transcript
        else:
            print(f"⚠️  No earnings transcript found for {ticker}, using sample data")
    except Exception as e:
        print(f"⚠️  Error fetching transcript: {e}, using sample data")
    
    # Fallback to sample data
    return f"""'''

if old_earnings_func_start in content:
    content = content.replace(old_earnings_func_start, new_earnings_func)
    print("✅ Updated generate_sample_earnings_call() to use real data")
else:
    print("⚠️  Could not find generate_sample_earnings_call function")

# Write back
with open('app/bloomberg_dashboard.py', 'w') as f:
    f.write(content)

print("\n✅ Bloomberg dashboard updated successfully!")
print("\nThe dashboard will now:")
print("  1. Try to fetch real news from NewsAPI/FMP")
print("  2. Try to fetch real earnings transcripts from FMP")
print("  3. Fall back to sample data if APIs fail")
print("\nRestart your Streamlit app to see the changes!")


