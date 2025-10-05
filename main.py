"""
Financial Research Tool - Professional Edition
Entry point for the Streamlit application.
"""
import streamlit as st
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.settings import APP_TITLE, APP_ICON, PAGE_LAYOUT
from app import market_overview_polygon, dashboard_polygon, data_export_polygon, bloomberg_dashboard, sentiment_analysis, news_test_page, simple_earnings_analysis

# Page configuration
st.set_page_config(
    page_title="Professional Financial Terminal",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar navigation
st.sidebar.markdown("""
    <div style='text-align: center; padding: 20px 0;'>
        <h1 style='margin: 0; background: linear-gradient(90deg, #FF6B35 0%, #00D4FF 100%);
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                   font-size: 1.5rem;'>
            ⚡ FINANCIAL TERMINAL
        </h1>
        <p style='font-size: 0.7rem; color: #8B949E; margin: 5px 0;'>Professional Edition v3.3</p>
    </div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "⚡ Bloomberg Terminal",
        "📊 Earnings Transcript Analysis",
        "🤖 AI Sentiment Analysis",
        "📰 News API Test",
        "🏠 Market Overview",
        "📈 Stock Dashboard",
        "📥 Data Export"
    ]
)

st.sidebar.markdown("---")

# Theme selector
st.sidebar.markdown("### ⚙️ SETTINGS")
ui_style = st.sidebar.selectbox(
    "UI Theme",
    ["Bloomberg Dark", "Standard Light"],
    help="Choose your preferred interface style"
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 FEATURES")
st.sidebar.success(
    """
    **✨ NEW: Earnings Transcript Analysis!**
    
    - View complete earnings transcripts
    - AI sentiment analysis with FinBERT
    - Segment-by-segment breakdown
    - Real-time FMP integration
    
    **Other Features:**
    - News API testing
    - AI Sentiment Analysis
    - Bloomberg-style Terminal
    - Professional visualizations
    - Real-time stock data
    
    **Powered by:** FMP, Polygon.io, newsdata.io, FinBERT
    """
)

st.sidebar.markdown("---")
st.sidebar.caption("**Version 4.0** • Earnings Analysis Edition")
st.sidebar.caption("© 2025 Financial Research Tool")

# Main content area - route to appropriate page
if page == "⚡ Bloomberg Terminal":
    bloomberg_dashboard.show()
elif page == "📊 Earnings Transcript Analysis":
    simple_earnings_analysis.show()
elif page == "🤖 AI Sentiment Analysis":
    sentiment_analysis.show()
elif page == "📰 News API Test":
    news_test_page.show()
elif page == "🏠 Market Overview":
    market_overview_polygon.show()
elif page == "📈 Stock Dashboard":
    dashboard_polygon.show()
elif page == "📥 Data Export":
    data_export_polygon.show()
