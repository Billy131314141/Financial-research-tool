"""
News Test Page - Test newsdata.io API only
Simple page to verify news API is working
"""
import streamlit as st
import requests
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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
        .news-card {{
            background-color: {COLORS['bg_medium']};
            border-left: 4px solid {COLORS['accent_blue']};
            padding: 15px;
            margin: 10px 0;
            border-radius: 4px;
        }}
        </style>
    """, unsafe_allow_html=True)


def test_newsdata_io_api(ticker, company_name, api_key):
    """Test newsdata.io API directly"""
    
    st.markdown("### 📰 Testing newsdata.io API")
    
    if not api_key or len(api_key) < 10:
        st.error("❌ Please enter your newsdata.io API key")
        return
    
    st.caption(f"Using API Key: {api_key[:20]}...")
    
    try:
        # Call newsdata.io API
        url = 'https://newsdata.io/api/1/news'
        params = {
            'apikey': api_key,
            'q': f'{ticker} OR {company_name}',
            'language': 'en',
            'category': 'business'
        }
        
        st.info(f"📡 Calling newsdata.io API...")
        st.code(f"GET {url}?q={ticker} OR {company_name}&category=business")
        
        response = requests.get(url, params=params, timeout=10)
        
        st.markdown(f"**Status Code:** {response.status_code}")
        
        data = response.json()
        
        # Check response
        if response.status_code == 200 and data.get('status') == 'success':
            results = data.get('results', [])
            total = data.get('totalResults', 0)
            
            st.success(f"✅ SUCCESS! API is working!")
            st.markdown(f"**Total Results Available:** {total}")
            st.markdown(f"**Results Returned:** {len(results)}")
            
            if results:
                st.markdown("---")
                st.markdown("#### 📰 News Headlines:")
                
                for i, article in enumerate(results, 1):
                    title = article.get('title', 'No title')
                    source = article.get('source_id', 'Unknown')
                    pub_date = article.get('pubDate', 'Unknown')[:10]
                    description = article.get('description', 'No description')
                    link = article.get('link', '#')
                    
                    st.markdown(f"""
                    <div class="news-card">
                        <h4>{i}. {title}</h4>
                        <p><strong>Source:</strong> {source} | <strong>Date:</strong> {pub_date}</p>
                        <p><em>{description[:200]}...</em></p>
                        <p><a href="{link}" target="_blank">Read more →</a></p>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("---")
                st.success("✅ Your newsdata.io API is working! You can now integrate this into your app.")
            else:
                st.warning("⚠️ API worked but returned no results for this search")
                
        else:
            st.error("❌ API Error")
            st.json(data)
            
            if data.get('status') == 'error':
                error_code = data.get('results', {}).get('code', 'unknown')
                error_message = data.get('results', {}).get('message', 'Unknown error')
                
                st.markdown(f"""
                **Error Code:** {error_code}  
                **Message:** {error_message}
                
                **Common Issues:**
                - `apiKeyInvalid`: Your API key is invalid
                - `apiKeyMissing`: No API key provided
                - `rateLimitExceeded`: Too many requests
                """)
                
    except Exception as e:
        st.error(f"❌ Request Error: {e}")
        st.code(str(e))


def show():
    """Main news test page"""
    apply_style()
    
    # Header
    st.markdown(f"""
        <div style='background: linear-gradient(90deg, {COLORS['accent_orange']} 0%, {COLORS['accent_blue']} 100%); 
                    padding: 25px; margin-bottom: 30px; border-radius: 8px;'>
            <h1 style='margin: 0; color: white;'>📰 News API Test</h1>
            <p style='margin: 10px 0 0 0; color: white; font-size: 1.1rem;'>
                Test newsdata.io API - Verify it's working
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🔑 Enter Your API Key")
    st.info("""
    **Don't have an API key?** Get one free at: https://newsdata.io/register
    
    **This test will:**
    - Check if your API key is valid
    - Show real news headlines
    - Verify the API is working
    """)
    
    # API Key input - loads from .env or Streamlit Secrets
    api_key = st.text_input(
        "newsdata.io API Key",
        value=os.getenv('NEWS_API_KEY', ''),
        type="password",
        help="Enter your newsdata.io API key (or set NEWS_API_KEY in .env)"
    )
    
    st.markdown("---")
    
    # Stock input
    col1, col2, col3 = st.columns([3, 2, 1])
    with col1:
        ticker = st.text_input("Stock Ticker", value="AAPL").upper()
    with col2:
        company_name = st.text_input("Company Name", value="Apple")
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        test_btn = st.button("🔍 TEST API", use_container_width=True)
    
    st.markdown("---")
    
    if test_btn:
        test_newsdata_io_api(ticker, company_name, api_key)
    else:
        st.markdown("""
        ### 📋 Instructions:
        
        1. **Enter your newsdata.io API key** above
        2. **Enter a stock ticker** (e.g., AAPL, TSLA, MSFT)
        3. **Click TEST API** button
        4. **Check if you see news headlines**
        
        #### ✅ If successful:
        - You'll see "✅ SUCCESS!" message
        - News headlines will be displayed
        - Your API is ready to integrate
        
        #### ❌ If failed:
        - You'll see error message
        - Check API key is correct
        - Verify internet connection
        """)


if __name__ == "__main__":
    show()
