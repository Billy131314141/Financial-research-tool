"""
Data Test Page - Check if APIs are fetching real data
Tests newsdata.io and FMP APIs
"""
import streamlit as st
import requests
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bloomberg-style colors
COLORS = {
    'bg_dark': '#0D1117',
    'bg_medium': '#161B22',
    'accent_orange': '#FF6B35',
    'accent_blue': '#00D4FF',
    'text_primary': '#E6EDF3',
}

def apply_style():
    st.markdown(f"""
        <style>
        .stApp {{
            background-color: {COLORS['bg_dark']};
            color: {COLORS['text_primary']};
        }}
        .data-card {{
            background-color: {COLORS['bg_medium']};
            border-left: 4px solid {COLORS['accent_blue']};
            padding: 15px;
            margin: 10px 0;
            border-radius: 4px;
        }}
        .earnings-card {{
            background-color: {COLORS['bg_medium']};
            border-left: 4px solid {COLORS['accent_orange']};
            padding: 20px;
            margin: 10px 0;
            border-radius: 4px;
        }}
        </style>
    """, unsafe_allow_html=True)


def test_newsdata_io(ticker, company_name):
    """Test newsdata.io API"""
    api_key = os.getenv('NEWS_API_KEY')
    
    st.markdown("### 📰 Testing newsdata.io API")
    st.caption(f"API Key: {api_key[:25]}..." if api_key else "No API key found")
    
    if not api_key:
        st.error("❌ NEWS_API_KEY not found in .env file")
        return
    
    try:
        # newsdata.io API endpoint
        url = 'https://newsdata.io/api/1/news'
        params = {
            'apikey': api_key,
            'q': f'{ticker} OR {company_name}',
            'language': 'en',
            'category': 'business'
        }
        
        st.info(f"📡 Calling newsdata.io for {ticker}...")
        st.code(f"GET {url}?q={ticker}")
        
        response = requests.get(url, params=params, timeout=10)
        st.markdown(f"**Status Code:** {response.status_code}")
        
        data = response.json()
        
        # Check response
        if response.status_code == 200 and data.get('status') == 'success':
            results = data.get('results', [])
            st.success(f"✅ SUCCESS! newsdata.io returned {len(results)} articles")
            st.markdown(f"**Total Results:** {data.get('totalResults', 0)}")
            
            if results:
                st.markdown("---")
                st.markdown("#### 📰 News Headlines:")
                
                for i, article in enumerate(results, 1):
                    st.markdown(f"""
                    <div class="data-card">
                        <h4>{i}. {article.get('title', 'No title')}</h4>
                        <p><strong>Source:</strong> {article.get('source_id', 'Unknown')} | 
                           <strong>Published:</strong> {article.get('pubDate', 'Unknown')[:10]}</p>
                        <p><em>{article.get('description', 'No description')[:200]}...</em></p>
                        <p><a href="{article.get('link', '#')}" target="_blank">Read more →</a></p>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ API returned an error or no results")
            st.json(data)
            
    except Exception as e:
        st.error(f"❌ newsdata.io Error: {e}")
        st.code(str(e))


def test_fmp_profile(ticker):
    """Test FMP Company Profile API (usually available on free tier)"""
    api_key = os.getenv('FMP_API_KEY')
    
    st.markdown("### 📊 Testing FMP Company Profile API")
    st.caption(f"API Key: {api_key[:25]}..." if api_key else "No API key found")
    
    if not api_key:
        st.error("❌ FMP_API_KEY not found in .env file")
        return
    
    try:
        url = f'https://financialmodelingprep.com/api/v3/profile/{ticker}'
        params = {'apikey': api_key}
        
        st.info(f"📡 Calling FMP Profile API for {ticker}...")
        st.code(f"GET {url}")
        
        response = requests.get(url, params=params, timeout=10)
        st.markdown(f"**Status Code:** {response.status_code}")
        
        data = response.json()
        
        if isinstance(data, dict) and 'Error Message' in data:
            st.error(f"❌ FMP API Error:")
            st.json(data)
        elif isinstance(data, list) and len(data) > 0:
            profile = data[0]
            st.success(f"✅ SUCCESS! Got company profile")
            
            st.markdown("---")
            st.markdown("#### 📊 Company Information:")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Company:** {profile.get('companyName', 'N/A')}")
                st.markdown(f"**Sector:** {profile.get('sector', 'N/A')}")
                st.markdown(f"**Industry:** {profile.get('industry', 'N/A')}")
                st.markdown(f"**Exchange:** {profile.get('exchange', 'N/A')}")
            with col2:
                st.markdown(f"**Market Cap:** ${profile.get('mktCap', 0):,.0f}")
                st.markdown(f"**Price:** ${profile.get('price', 0):.2f}")
                st.markdown(f"**Website:** {profile.get('website', 'N/A')}")
                st.markdown(f"**CEO:** {profile.get('ceo', 'N/A')}")
            
            st.markdown("**Description:**")
            st.info(profile.get('description', 'No description available'))
        else:
            st.warning("⚠️ Unexpected response")
            st.json(data)
            
    except Exception as e:
        st.error(f"❌ FMP Profile Error: {e}")


def test_fmp_quote(ticker):
    """Test FMP Quote API (real-time stock data)"""
    api_key = os.getenv('FMP_API_KEY')
    
    st.markdown("### 💹 Testing FMP Quote API")
    
    try:
        url = f'https://financialmodelingprep.com/api/v3/quote/{ticker}'
        params = {'apikey': api_key}
        
        st.info(f"📡 Calling FMP Quote API for {ticker}...")
        
        response = requests.get(url, params=params, timeout=10)
        st.markdown(f"**Status Code:** {response.status_code}")
        
        data = response.json()
        
        if isinstance(data, dict) and 'Error Message' in data:
            st.error(f"❌ FMP API Error:")
            st.json(data)
        elif isinstance(data, list) and len(data) > 0:
            quote = data[0]
            st.success(f"✅ SUCCESS! Got real-time quote")
            
            st.markdown("---")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Price", f"${quote.get('price', 0):.2f}")
            with col2:
                change = quote.get('change', 0)
                st.metric("Change", f"${change:.2f}", f"{quote.get('changesPercentage', 0):.2f}%")
            with col3:
                st.metric("Day High", f"${quote.get('dayHigh', 0):.2f}")
            with col4:
                st.metric("Day Low", f"${quote.get('dayLow', 0):.2f}")
            
            st.markdown("**Additional Info:**")
            st.json(quote)
        else:
            st.warning("⚠️ Unexpected response")
            st.json(data)
            
    except Exception as e:
        st.error(f"❌ FMP Quote Error: {e}")


def test_fmp_income_statement(ticker):
    """Test FMP Income Statement API"""
    api_key = os.getenv('FMP_API_KEY')
    
    st.markdown("### 📊 Testing FMP Income Statement API")
    
    try:
        url = f'https://financialmodelingprep.com/api/v3/income-statement/{ticker}'
        params = {'apikey': api_key, 'limit': 1}
        
        st.info(f"📡 Calling FMP Income Statement API for {ticker}...")
        
        response = requests.get(url, params=params, timeout=10)
        st.markdown(f"**Status Code:** {response.status_code}")
        
        data = response.json()
        
        if isinstance(data, dict) and 'Error Message' in data:
            st.warning("⚠️ Income Statement not available on free tier")
            st.json(data)
        elif isinstance(data, list) and len(data) > 0:
            statement = data[0]
            st.success(f"✅ SUCCESS! Got income statement")
            
            st.markdown(f"**Fiscal Year:** {statement.get('calendarYear', 'N/A')}")
            st.markdown(f"**Period:** {statement.get('period', 'N/A')}")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Revenue", f"${statement.get('revenue', 0)/1e9:.2f}B")
            with col2:
                st.metric("Net Income", f"${statement.get('netIncome', 0)/1e9:.2f}B")
            with col3:
                st.metric("EPS", f"${statement.get('eps', 0):.2f}")
        else:
            st.warning("⚠️ No data available")
            st.json(data)
            
    except Exception as e:
        st.error(f"❌ FMP Income Statement Error: {e}")


def show():
    """Main data test page"""
    apply_style()
    
    # Header
    st.markdown(f"""
        <div style='background: linear-gradient(90deg, {COLORS['accent_orange']} 0%, {COLORS['accent_blue']} 100%); 
                    padding: 25px; margin-bottom: 30px; border-radius: 8px;'>
            <h1 style='margin: 0; color: white;'>🔍 API Data Test Page</h1>
            <p style='margin: 10px 0 0 0; color: white; font-size: 1.1rem;'>
                Test newsdata.io and FMP APIs - See what data is available
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Input section
    col1, col2, col3 = st.columns([3, 2, 1])
    with col1:
        ticker = st.text_input("Stock Ticker", value="AAPL").upper()
    with col2:
        company_name = st.text_input("Company Name", value="Apple Inc")
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        test_btn = st.button("🔍 TEST APIs", use_container_width=True)
    
    if test_btn or 'test_run' not in st.session_state:
        st.session_state.test_run = True
    
    if st.session_state.get('test_run'):
        st.markdown("---")
        
        # API Keys Status
        st.markdown("### 🔑 API Keys Status")
        col1, col2 = st.columns(2)
        
        with col1:
            news_key = os.getenv('NEWS_API_KEY')
            if news_key:
                st.success(f"✅ newsdata.io Key: {news_key[:20]}...")
            else:
                st.error("❌ NEWS_API_KEY not found")
        
        with col2:
            fmp_key = os.getenv('FMP_API_KEY')
            if fmp_key:
                st.success(f"✅ FMP Key: {fmp_key[:20]}...")
            else:
                st.error("❌ FMP_API_KEY not found")
        
        st.markdown("---")
        
        # Test each API
        tabs = st.tabs([
            "📰 newsdata.io Test", 
            "📊 FMP Profile", 
            "💹 FMP Quote",
            "📊 FMP Financials"
        ])
        
        with tabs[0]:
            test_newsdata_io(ticker, company_name)
        
        with tabs[1]:
            test_fmp_profile(ticker)
        
        with tabs[2]:
            test_fmp_quote(ticker)
        
        with tabs[3]:
            test_fmp_income_statement(ticker)
        
        st.markdown("---")
        
        # Summary
        st.markdown("### 📊 Summary")
        st.info("""
        **What this page tests:**
        - newsdata.io: Financial news articles (your news source)
        - FMP Profile: Company information
        - FMP Quote: Real-time stock prices
        - FMP Financials: Income statements (may require paid plan)
        
        **If you see ✅ SUCCESS:**
        - API is working and returning data
        - This data can be integrated into your app
        
        **If you see ❌ ERROR:**
        - Check error message for details
        - Some endpoints require paid FMP plans
        - Free tier has limits: 250 calls/day
        """)


if __name__ == "__main__":
    show()
