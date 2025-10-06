"""
Simple Earnings Transcript Analysis
Uses API Ninjas endpoint: /v1/earningstranscript
Fixed: Uses session state with query tracking to prevent stale data
"""
import streamlit as st
import requests
import os
import sys
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.analysis.finbert_sentiment import FinBERTAnalyzer

# Bloomberg-style colors
COLORS = {
    'bg_dark': '#0D1117',
    'bg_medium': '#161B22',
    'bg_light': '#21262D',
    'accent_orange': '#FF6B35',
    'accent_blue': '#00D4FF',
    'accent_green': '#00FF87',
    'text_primary': '#E6EDF3',
    'text_secondary': '#8B949E',
    'positive': '#00FF87',
    'negative': '#FF6B6B',
    'neutral': '#FFD93D',
}


def apply_style():
    """Apply custom CSS"""
    st.markdown(f"""
        <style>
        .stApp {{
            background-color: {COLORS['bg_dark']};
            color: {COLORS['text_primary']};
        }}
        
        .transcript-box {{
            background-color: {COLORS['bg_medium']};
            border: 1px solid {COLORS['bg_light']};
            border-radius: 8px;
            padding: 25px;
            margin: 20px 0;
            font-family: 'Courier New', monospace;
            font-size: 0.9rem;
            line-height: 1.8;
            max-height: 600px;
            overflow-y: auto;
        }}
        
        .sentiment-card {{
            background: linear-gradient(135deg, {COLORS['bg_medium']} 0%, {COLORS['bg_light']} 100%);
            border-left: 4px solid {COLORS['accent_blue']};
            padding: 20px;
            margin: 15px 0;
            border-radius: 8px;
        }}
        
        .metric-box {{
            background-color: {COLORS['bg_light']};
            padding: 15px;
            border-radius: 6px;
            text-align: center;
        }}
        </style>
    """, unsafe_allow_html=True)


@st.cache_data(ttl=3600)
def fetch_transcript(ticker: str, year: int, quarter: int, api_key: str):
    """
    Fetch earnings transcript from API Ninjas
    Endpoint: https://api.api-ninjas.com/v1/earningstranscript
    """
    try:
        url = "https://api.api-ninjas.com/v1/earningstranscript"
        params = {
            'ticker': ticker.upper(),
            'year': year,
            'quarter': quarter
        }
        
        # API Ninjas uses X-Api-Key header
        headers = {
            'X-Api-Key': api_key
        }
        
        # Debug info (only show key length for security)
        with st.expander("🔍 Debug Information", expanded=False):
            st.code(f"""
API Endpoint: {url}
Parameters: ticker={params['ticker']}, year={params['year']}, quarter={params['quarter']}
API Key Length: {len(api_key) if api_key else 0} characters
API Key Format: {'Valid' if api_key and len(api_key) > 10 else 'Invalid - too short'}
Full URL: {url}?ticker={params['ticker']}&year={params['year']}&quarter={params['quarter']}
            """)
        
        response = requests.get(url, params=params, headers=headers, timeout=20)
        
        # Log response for debugging
        st.caption(f"📡 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            # API Ninjas returns the transcript directly
            if data and isinstance(data, dict):
                return data
            elif data and isinstance(data, list) and len(data) > 0:
                return data[0]
            else:
                st.warning("⚠️ API returned 200 but no data found")
                st.json(data)
                return None
        elif response.status_code == 401:
            st.error("❌ **Authentication Error (401): Invalid API Key**")
            st.info("""
            **How to fix:**
            1. Check your API Ninjas dashboard: https://api-ninjas.com/profile
            2. Verify your API key is active
            3. For Hugging Face deployment, check Settings → Repository secrets
            4. Ensure the key is named exactly: `API_NINJAS_KEY`
            5. No quotes or extra spaces in the secret value
            
            **Current key status:**
            - Key is present: {bool_status}
            - Key length: {key_len} characters
            """.format(
                bool_status="✅ Yes" if api_key else "❌ No",
                key_len=len(api_key) if api_key else 0
            ))
            with st.expander("Show full error response"):
                st.code(response.text)
            return None
        elif response.status_code == 404:
            st.error(f"❌ **Not Found (404): Transcript not available**")
            st.info(f"""
            The API returned 404 for {ticker} Q{quarter} {year}.
            
            This usually means:
            - No earnings transcript exists for this combination
            - Company hasn't reported earnings yet
            - Try a different quarter or year
            
            **Suggestions:**
            - Try major tech companies: MSFT, AAPL, GOOGL, TSLA
            - Try recent quarters: Q1-Q4 2024, Q1-Q4 2023
            - Some companies report on different schedules
            """)
            with st.expander("Show API response"):
                st.code(response.text)
            return None
        elif response.status_code == 429:
            st.error("❌ **Rate Limit Exceeded (429)**")
            st.info("""
            You've hit the API rate limit.
            
            **API Ninjas Free Tier:**
            - 50,000 requests per month
            - ~1,600 requests per day
            
            Wait a few minutes and try again.
            """)
            return None
        else:
            st.error(f"❌ **API Error ({response.status_code})**")
            st.code(response.text)
            with st.expander("Full error details"):
                st.json({
                    "status_code": response.status_code,
                    "url": url,
                    "params": params,
                    "response": response.text
                })
            return None
            
    except requests.exceptions.Timeout:
        st.error("❌ **Request Timeout**")
        st.info("The API request took too long. Try again or check your internet connection.")
        return None
    except requests.exceptions.ConnectionError:
        st.error("❌ **Connection Error**")
        st.info("Could not connect to API Ninjas. Check your internet connection.")
        return None
    except Exception as e:
        st.error(f"❌ **Unexpected Error:** {type(e).__name__}")
        st.code(str(e))
        with st.expander("Full error traceback"):
            import traceback
            st.code(traceback.format_exc())
        return None


def display_sentiment(aggregate_sentiment):
    """Display sentiment overview"""
    overall = aggregate_sentiment.get('overall_sentiment', 'neutral')
    confidence = aggregate_sentiment.get('confidence', 0.0)
    
    if overall == 'positive':
        emoji = '📈'
        color = COLORS['positive']
    elif overall == 'negative':
        emoji = '📉'
        color = COLORS['negative']
    else:
        emoji = '➡️'
        color = COLORS['neutral']
    
    st.markdown(f"""
        <div class="sentiment-card" style="border-left-color: {color};">
            <h2 style='margin: 0; color: {color};'>{emoji} Overall Sentiment: {overall.upper()}</h2>
            <p style='font-size: 1.2rem; margin: 10px 0;'>
                Confidence: <strong>{confidence:.1%}</strong>
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
            <div class="metric-box">
                <div style="color: {COLORS['text_secondary']};">Positive</div>
                <div style="font-size: 2rem; font-weight: bold; color: {COLORS['positive']}; margin: 10px 0;">
                    {aggregate_sentiment.get('positive_percentage', 0.0):.1f}%
                </div>
                <div style="color: {COLORS['text_secondary']};">
                    {aggregate_sentiment.get('positive_count', 0)} segments
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="metric-box">
                <div style="color: {COLORS['text_secondary']};">Negative</div>
                <div style="font-size: 2rem; font-weight: bold; color: {COLORS['negative']}; margin: 10px 0;">
                    {aggregate_sentiment.get('negative_percentage', 0.0):.1f}%
                </div>
                <div style="color: {COLORS['text_secondary']};">
                    {aggregate_sentiment.get('negative_count', 0)} segments
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="metric-box">
                <div style="color: {COLORS['text_secondary']};">Neutral</div>
                <div style="font-size: 2rem; font-weight: bold; color: {COLORS['neutral']}; margin: 10px 0;">
                    {aggregate_sentiment.get('neutral_percentage', 0.0):.1f}%
                </div>
                <div style="color: {COLORS['text_secondary']};">
                    {aggregate_sentiment.get('neutral_count', 0)} segments
                </div>
            </div>
        """, unsafe_allow_html=True)


def show():
    """Main page"""
    apply_style()
    
    # Initialize session state for persisting data across reruns
    if 'transcript_result' not in st.session_state:
        st.session_state.transcript_result = None
    if 'transcript_query' not in st.session_state:
        st.session_state.transcript_query = None
    
    # Header
    st.markdown(f"""
        <div style='background: linear-gradient(90deg, {COLORS['accent_orange']} 0%, {COLORS['accent_blue']} 100%); 
                    padding: 30px; margin-bottom: 30px; border-radius: 10px;'>
            <h1 style='margin: 0; color: white;'>📊 Earnings Transcript Analyzer</h1>
            <p style='margin: 10px 0 0 0; color: white; font-size: 1.2rem;'>
                Powered by API Ninjas + FinBERT AI
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # API Key - loads from .env or Streamlit Secrets
    api_key = os.getenv('API_NINJAS_KEY')
    
    if not api_key:
        st.error("⚠️ API_NINJAS_KEY not found! Please add it to your .env file or Streamlit Secrets.")
        st.stop()
    
    # Input form
    st.markdown("### 🔍 Select Earnings Call")
    
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    
    with col1:
        ticker = st.text_input(
            "Stock Ticker",
            value="MSFT",
            help="Enter stock symbol (e.g., MSFT, AAPL, GOOGL)",
            key="ticker_input"
        ).upper()
    
    with col2:
        year = st.number_input(
            "Year",
            min_value=2015,
            max_value=2025,
            value=2024,
            step=1,
            key="year_input"
        )
    
    with col3:
        quarter = st.selectbox(
            "Quarter",
            options=[1, 2, 3, 4],
            index=1,  # Q2 (index 1 = value 2)
            key="quarter_input"
        )
    
    # Create unique query identifier for current inputs
    current_query = f"{ticker}_{year}_{quarter}"
    
    # Check if inputs changed - if so, clear old data
    if st.session_state.transcript_query != current_query:
        if st.session_state.transcript_result is not None:
            # Clear old data when inputs change
            st.session_state.transcript_result = None
            st.info("💡 Inputs changed. Click ANALYZE to fetch new data.")
    
    with col4:
        st.markdown("<br>", unsafe_allow_html=True)
        analyze_btn = st.button("🚀 ANALYZE", use_container_width=True, type="primary")
    
    # Show endpoint
    st.caption(f"🌐 API Ninjas: `https://api.api-ninjas.com/v1/earningstranscript?ticker={ticker}&year={year}&quarter={quarter}`")
    
    st.markdown("---")
    
    # When button is clicked, fetch and store data in session state
    if analyze_btn:
        with st.spinner(f'📡 Fetching {ticker} Q{quarter} {year} earnings transcript...'):
            transcript_data = fetch_transcript(ticker, year, quarter, api_key)
            
            if not transcript_data:
                st.error("❌ Could not fetch transcript from API Ninjas")
                st.info("""
                **Possible reasons:**
                - Transcript not available for this company/quarter
                - Year/quarter combination doesn't exist yet
                - API key issue or rate limit
                - Company hasn't reported earnings yet
                
                **Try:**
                - Different quarter (Q1, Q2, Q3, Q4)
                - Previous year (2023, 2022, 2021)
                - Major companies: MSFT, AAPL, GOOGL, TSLA, NVDA
                
                **Example that works:** MSFT, Year: 2024, Quarter: 2
                """)
                st.session_state.transcript_result = None
                st.session_state.transcript_query = None
            else:
                # Extract data (API Ninjas format)
                content = (transcript_data.get('transcript') or 
                          transcript_data.get('content') or 
                          transcript_data.get('text') or '')
                
                if not content:
                    st.error("❌ Transcript returned but has no content")
                    st.json(transcript_data)
                    st.session_state.transcript_result = None
                    st.session_state.transcript_query = None
                else:
                    symbol = transcript_data.get('ticker', transcript_data.get('symbol', ticker))
                    qtr = transcript_data.get('quarter', quarter)
                    yr = transcript_data.get('year', year)
                    date = transcript_data.get('date', f'Q{qtr} {yr}')
                    
                    # Success! Store in session state with query tracking
                    st.success(f"✅ Successfully fetched {symbol} Q{qtr} {yr} earnings transcript!")
                    
                    st.session_state.transcript_result = {
                        'content': content,
                        'symbol': symbol,
                        'qtr': qtr,
                        'yr': yr,
                        'date': date,
                        'sentiment': None  # Will be computed below
                    }
                    # Track what query this data is for
                    st.session_state.transcript_query = current_query
    
    # Display data if it exists AND matches current inputs
    if st.session_state.transcript_result and st.session_state.transcript_query == current_query:
        data = st.session_state.transcript_result
        content = data['content']
        symbol = data['symbol']
        qtr = data['qtr']
        yr = data['yr']
        date = data['date']
        
        # Show metadata
        st.markdown(f"""
            <div class="sentiment-card">
                <h3 style='margin: 0;'>{symbol} - Q{qtr} {yr} Earnings Call</h3>
                <p style='margin: 5px 0; color: {COLORS['text_secondary']};'>
                    Date: {date} | Length: {len(content):,} characters | Words: ~{len(content.split()):,}
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Sentiment Analysis (compute once and cache in session state)
        if data['sentiment'] is None:
            st.markdown("### 🤖 AI Sentiment Analysis")
            
            with st.spinner('🧠 Analyzing with FinBERT...'):
                analyzer = FinBERTAnalyzer()
                
                # Split into chunks
                chunks = [p.strip() for p in content.split('\n\n') if p.strip() and len(p.strip()) > 50]
                if len(chunks) == 0:
                    chunks = [content[i:i+500] for i in range(0, len(content), 500)]
                
                st.info(f"📊 Analyzing {len(chunks)} segments...")
                
                # Analyze and store in session state
                aggregate_sentiment = analyzer.get_aggregate_sentiment(chunks)
                st.session_state.transcript_result['sentiment'] = aggregate_sentiment
        else:
            # Use cached sentiment from session state
            st.markdown("### 🤖 AI Sentiment Analysis")
            aggregate_sentiment = data['sentiment']
        
        # Display sentiment
        display_sentiment(aggregate_sentiment)
        
        st.markdown("---")
        
        # Full transcript
        st.markdown("### 📄 Complete Transcript")
        st.markdown(f"""
            <div class="transcript-box">
                {content.replace(chr(10), '<br>')}
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Detailed segments
        with st.expander("🔍 Detailed Segment Analysis", expanded=False):
            detailed = aggregate_sentiment.get('detailed_results', [])
            
            if detailed:
                for i, result in enumerate(detailed[:20], 1):
                    sentiment = result.get('sentiment', 'neutral')
                    confidence = result.get('confidence', 0.0)
                    text = result.get('text', '')[:200]
                    
                    if sentiment == 'positive':
                        emoji = '📈'
                        color = COLORS['positive']
                    elif sentiment == 'negative':
                        emoji = '📉'
                        color = COLORS['negative']
                    else:
                        emoji = '➡️'
                        color = COLORS['neutral']
                    
                    st.markdown(f"""
                        <div style='background-color: {COLORS['bg_light']}; padding: 15px; margin: 10px 0; 
                                    border-radius: 6px; border-left: 3px solid {color};'>
                            <strong>Segment {i}:</strong> {emoji} {sentiment.upper()} ({confidence:.1%} confidence)<br>
                            <em style='color: {COLORS['text_secondary']};'>{text}...</em>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No detailed analysis available.")
    
    else:
        # Show instructions when no data is loaded
        st.markdown("""
        ### 📋 How to Use
        
        1. **Enter stock ticker** (e.g., AAPL, TSLA, MSFT)
        2. **Select year** (2015-2025)
        3. **Select quarter** (Q1, Q2, Q3, Q4)
        4. **Click ANALYZE** to fetch transcript and analyze sentiment
        
        ---
        
        ### 📊 What You'll Get
        
        - 📄 **Full earnings call transcript**
        - 🤖 **AI sentiment analysis** (FinBERT)
        - 📈 **Sentiment breakdown** (Positive/Negative/Neutral)
        - 🔍 **Segment-by-segment analysis**
        
        ---
        
        ### 💡 Tips
        
        - **Major tech companies** usually have transcripts (MSFT, AAPL, GOOGL, META, TSLA)
        - **Recent quarters** are more likely to be available (2022-2024)
        - **Q1 = Jan-Mar, Q2 = Apr-Jun, Q3 = Jul-Sep, Q4 = Oct-Dec**
        - **API Ninjas** provides reliable earnings transcripts
        
        ---
        
        ### 🎯 Try These
        
        Popular earnings calls:
        - **MSFT** Q2 2024 (Azure cloud growth) ⭐ Recommended!
        - **AAPL** Q3 2024 (iPhone sales results)
        - **TSLA** Q4 2023 (Tesla annual results)
        - **GOOGL** Q2 2024 (AI developments)
        - **NVDA** Q1 2024 (GPU demand)
        
        **Ready? Enter a ticker above!** 🚀
        """)


if __name__ == "__main__":
    show()
