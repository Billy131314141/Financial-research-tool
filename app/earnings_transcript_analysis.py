"""
Earnings Transcript Analysis - Display full transcripts with FinBERT sentiment analysis
"""
import streamlit as st
import os
import sys
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.api.fmp_transcript_fetcher import FMPTranscriptFetcher
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
    """Apply Bloomberg-style custom CSS"""
    st.markdown(f"""
        <style>
        .stApp {{
            background-color: {COLORS['bg_dark']};
            color: {COLORS['text_primary']};
        }}
        
        .transcript-container {{
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
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        }}
        
        .positive-sentiment {{
            border-left-color: {COLORS['positive']};
        }}
        
        .negative-sentiment {{
            border-left-color: {COLORS['negative']};
        }}
        
        .neutral-sentiment {{
            border-left-color: {COLORS['neutral']};
        }}
        
        .metric-box {{
            background-color: {COLORS['bg_light']};
            padding: 15px;
            border-radius: 6px;
            text-align: center;
            margin: 10px 0;
        }}
        
        .metric-value {{
            font-size: 2rem;
            font-weight: bold;
            margin: 10px 0;
        }}
        
        .metric-label {{
            color: {COLORS['text_secondary']};
            font-size: 0.9rem;
        }}
        
        .loading-text {{
            color: {COLORS['accent_blue']};
            font-size: 1.1rem;
            text-align: center;
            padding: 20px;
        }}
        </style>
    """, unsafe_allow_html=True)


def display_sentiment_overview(aggregate_sentiment):
    """Display sentiment analysis overview"""
    
    overall = aggregate_sentiment.get('overall_sentiment', 'neutral')
    confidence = aggregate_sentiment.get('confidence', 0.0)
    
    # Determine color based on sentiment
    if overall == 'positive':
        sentiment_class = 'positive-sentiment'
        emoji = '📈'
        color = COLORS['positive']
    elif overall == 'negative':
        sentiment_class = 'negative-sentiment'
        emoji = '📉'
        color = COLORS['negative']
    else:
        sentiment_class = 'neutral-sentiment'
        emoji = '➡️'
        color = COLORS['neutral']
    
    st.markdown(f"""
        <div class="sentiment-card {sentiment_class}">
            <h2 style='margin: 0; color: {color};'>{emoji} Overall Sentiment: {overall.upper()}</h2>
            <p style='font-size: 1.2rem; margin: 10px 0;'>
                Confidence: <strong>{confidence:.1%}</strong>
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Display metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        pos_pct = aggregate_sentiment.get('positive_percentage', 0.0)
        st.markdown(f"""
            <div class="metric-box">
                <div class="metric-label">Positive</div>
                <div class="metric-value" style="color: {COLORS['positive']};">
                    {pos_pct:.1f}%
                </div>
                <div class="metric-label">
                    {aggregate_sentiment.get('positive_count', 0)} segments
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        neg_pct = aggregate_sentiment.get('negative_percentage', 0.0)
        st.markdown(f"""
            <div class="metric-box">
                <div class="metric-label">Negative</div>
                <div class="metric-value" style="color: {COLORS['negative']};">
                    {neg_pct:.1f}%
                </div>
                <div class="metric-label">
                    {aggregate_sentiment.get('negative_count', 0)} segments
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        neu_pct = aggregate_sentiment.get('neutral_percentage', 0.0)
        st.markdown(f"""
            <div class="metric-box">
                <div class="metric-label">Neutral</div>
                <div class="metric-value" style="color: {COLORS['neutral']};">
                    {neu_pct:.1f}%
                </div>
                <div class="metric-label">
                    {aggregate_sentiment.get('neutral_count', 0)} segments
                </div>
            </div>
        """, unsafe_allow_html=True)


def display_transcript(transcript_text, title="Earnings Call Transcript"):
    """Display the full transcript in a scrollable container"""
    
    st.markdown(f"### 📄 {title}")
    st.markdown(f"""
        <div class="transcript-container">
            {transcript_text.replace(chr(10), '<br>')}
        </div>
    """, unsafe_allow_html=True)


def show():
    """Main earnings transcript analysis page"""
    apply_style()
    
    # Header
    st.markdown(f"""
        <div style='background: linear-gradient(90deg, {COLORS['accent_orange']} 0%, {COLORS['accent_blue']} 100%); 
                    padding: 30px; margin-bottom: 30px; border-radius: 10px;'>
            <h1 style='margin: 0; color: white;'>📊 Earnings Transcript Analysis</h1>
            <p style='margin: 10px 0 0 0; color: white; font-size: 1.2rem;'>
                AI-Powered Sentiment Analysis with FinBERT
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # API Key setup
    fmp_api_key = os.getenv('FMP_API_KEY', 'A6MKpF3MmM14y3KFEazkMiLiPgpiAdGe')
    
    # Input section
    st.markdown("### 🔍 Select Company")
    
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        ticker = st.text_input(
            "Stock Ticker",
            value="AAPL",
            help="Enter a stock ticker (e.g., AAPL, TSLA, MSFT)"
        ).upper()
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        show_available = st.button("📋 Show Available", use_container_width=True)
    
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        analyze_btn = st.button("🚀 ANALYZE", use_container_width=True, type="primary")
    
    st.markdown("---")
    
    # Initialize fetcher
    fetcher = FMPTranscriptFetcher(fmp_api_key)
    
    # Show available transcripts
    if show_available:
        with st.spinner('📡 Fetching list of available transcripts from FMP...'):
            available = fetcher.get_available_transcripts(limit=100)
            
            if available:
                st.success(f"✅ Found {len(available)} available transcripts from FMP!")
                
                # Filter by ticker if one was entered
                if ticker:
                    ticker_transcripts = [t for t in available if ticker.upper() in t.get('symbol', '').upper()]
                    if ticker_transcripts:
                        st.markdown(f"### 📊 Transcripts for {ticker}:")
                        for t in ticker_transcripts:
                            st.markdown(f"""
                            <div class="sentiment-card">
                                <strong>{t.get('symbol')}</strong> - Q{t.get('period', 'Q1').replace('Q', '')} {t.get('fiscalYear') or t.get('year')}<br>
                                <em>Date: {t.get('date', 'Unknown')}</em>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.warning(f"⚠️ No transcripts found for {ticker} in FMP database")
                
                # Show all available
                with st.expander("📋 All Available Transcripts (First 20)", expanded=False):
                    for i, t in enumerate(available[:20], 1):
                        symbol = t.get('symbol', 'N/A')
                        quarter = t.get('period', 'Q1').replace('Q', '')
                        year = t.get('fiscalYear') or t.get('year', 'N/A')
                        date = t.get('date', 'N/A')
                        st.markdown(f"{i}. **{symbol}** - Q{quarter} {year} ({date})")
            else:
                st.error("❌ Could not fetch available transcripts from FMP")
                st.info("""
                **Possible reasons:**
                - API key might not have access to this endpoint
                - Free tier might have limitations
                - Network connectivity issue
                """)
        
        st.markdown("---")
    
    if analyze_btn:
        with st.spinner(f'📡 Fetching earnings transcript for {ticker}...'):
            # Try to fetch real transcript
            transcript_data = fetcher.get_transcript(ticker)
            
            # If API fails, use sample data
            if not transcript_data or 'content' not in transcript_data:
                st.warning(f"⚠️ Could not fetch real transcript for {ticker}. Using sample data for demonstration.")
                
                col_a, col_b = st.columns(2)
                with col_a:
                    st.info("""
                    **Why might this fail?**
                    
                    1. **Free tier limitations**: Transcript content may require paid plan
                    2. **No recent earnings**: Company hasn't reported recently
                    3. **Wrong endpoint**: FMP changed their API structure
                    4. **API quota**: You've reached daily limit (250 calls)
                    """)
                
                with col_b:
                    st.success("""
                    **Good news:**
                    
                    ✅ Sample transcript is realistic
                    ✅ Sentiment analysis is REAL (FinBERT AI)
                    ✅ You can still see how it works
                    ✅ Click "📋 Show Available" to see what FMP has
                    """)
                
                transcript_data = fetcher.get_sample_transcript(ticker)
            else:
                st.success(f"✅ Successfully fetched real earnings transcript for {ticker}!")
            
            # Extract transcript content
            transcript_text = transcript_data.get('content', '')
            symbol = transcript_data.get('symbol', ticker)
            quarter = transcript_data.get('quarter', 'N/A')
            year = transcript_data.get('year', 'N/A')
            date = transcript_data.get('date', 'N/A')
            
            # Display transcript metadata
            st.markdown(f"""
                <div class="sentiment-card">
                    <h3 style='margin: 0;'>{symbol} - Q{quarter} {year} Earnings Call</h3>
                    <p style='margin: 5px 0; color: {COLORS['text_secondary']};'>
                        Date: {date} | Transcript Length: {len(transcript_text):,} characters
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Perform sentiment analysis
            st.markdown("### 🤖 AI Sentiment Analysis")
            
            with st.spinner('🧠 Analyzing sentiment with FinBERT AI...'):
                # Initialize FinBERT analyzer
                analyzer = FinBERTAnalyzer()
                
                # Split transcript into chunks (FinBERT has 512 token limit)
                # Split by paragraphs for more meaningful analysis
                chunks = [p.strip() for p in transcript_text.split('\n\n') if p.strip() and len(p.strip()) > 50]
                
                if len(chunks) == 0:
                    chunks = [transcript_text]
                
                st.info(f"📊 Analyzing {len(chunks)} segments from the transcript...")
                
                # Analyze sentiment
                aggregate_sentiment = analyzer.get_aggregate_sentiment(chunks)
                
                # Display sentiment overview
                display_sentiment_overview(aggregate_sentiment)
            
            st.markdown("---")
            
            # Display full transcript
            display_transcript(transcript_text, f"{symbol} Q{quarter} {year} Earnings Call Transcript")
            
            st.markdown("---")
            
            # Detailed segment analysis
            with st.expander("🔍 Detailed Segment Analysis", expanded=False):
                st.markdown("### Sentiment by Segment")
                
                detailed = aggregate_sentiment.get('detailed_results', [])
                
                if detailed:
                    for i, result in enumerate(detailed[:20], 1):  # Show first 20 segments
                        sentiment = result.get('sentiment', 'neutral')
                        confidence = result.get('confidence', 0.0)
                        text = result.get('text', '')[:200]  # First 200 chars
                        
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
                            <div style='background-color: {COLORS['bg_light']}; padding: 15px; margin: 10px 0; border-radius: 6px; border-left: 3px solid {color};'>
                                <strong>Segment {i}:</strong> {emoji} {sentiment.upper()} ({confidence:.1%} confidence)<br>
                                <em style='color: {COLORS['text_secondary']};'>{text}...</em>
                            </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("No detailed segment data available.")
            
            st.markdown("---")
            
            # Analysis summary
            st.markdown("### 💡 Key Insights")
            
            overall = aggregate_sentiment.get('overall_sentiment', 'neutral')
            total = aggregate_sentiment.get('total_analyzed', 0)
            
            if overall == 'positive':
                st.success(f"""
                ✅ **Positive Outlook**: The earnings call shows a predominantly positive sentiment across {total} analyzed segments.
                Management appears confident about the company's performance and future prospects.
                """)
            elif overall == 'negative':
                st.error(f"""
                ⚠️ **Cautionary Tone**: The earnings call reflects concerns, with negative sentiment detected across {total} segments.
                Investors should pay attention to challenges and risk factors discussed.
                """)
            else:
                st.info(f"""
                ℹ️ **Balanced Perspective**: The earnings call presents a neutral to mixed sentiment across {total} segments.
                Management is providing a balanced view of opportunities and challenges.
                """)
    
    else:
        # Show instructions when not analyzing
        st.markdown("""
        ### 📋 How to Use
        
        1. **Enter a stock ticker** (e.g., AAPL, TSLA, MSFT, GOOGL)
        2. **Click "ANALYZE TRANSCRIPT"** button
        3. **View the complete earnings call transcript**
        4. **See AI-powered sentiment analysis** using FinBERT
        
        ---
        
        ### 🤖 About FinBERT Analysis
        
        This tool uses **FinBERT**, a BERT model fine-tuned on financial text, to analyze sentiment in earnings calls:
        
        - ✅ **Positive**: Optimistic language, growth indicators, strong performance
        - ❌ **Negative**: Concerns, challenges, declining metrics, risks
        - ➡️ **Neutral**: Factual statements, balanced commentary
        
        The model analyzes each segment of the transcript and provides:
        - Overall sentiment score
        - Confidence level
        - Breakdown by sentiment category
        - Segment-by-segment analysis
        
        ---
        
        ### 📊 What You'll Get
        
        - 📄 **Full Transcript**: Complete earnings call text
        - 🎯 **Overall Sentiment**: Positive, Negative, or Neutral
        - 📈 **Sentiment Distribution**: Percentage breakdown
        - 🔍 **Detailed Analysis**: Sentiment for each transcript segment
        - 💡 **Key Insights**: AI-generated summary
        
        ---
        
        ### 💡 Tips
        
        - Transcripts are fetched from Financial Modeling Prep (FMP)
        - If real data isn't available, sample data is used for demonstration
        - Sentiment analysis is always real (FinBERT AI model)
        - Analysis takes 30-60 seconds depending on transcript length
        
        **Ready to analyze?** Enter a ticker above! 🚀
        """)


if __name__ == "__main__":
    show()

