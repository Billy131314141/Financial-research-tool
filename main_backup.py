"""
Financial Research Tool Demo - Main Application
Entry point for the Streamlit application.
"""
import streamlit as st
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.settings import APP_TITLE, APP_ICON, PAGE_LAYOUT
from app import dashboard, market_overview, data_export

# Page configuration
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout=PAGE_LAYOUT,
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #F5F5F5;
        padding: 10px;
        border-radius: 5px;
    }
    h1 {
        color: #212121;
        font-weight: 600;
    }
    h2 {
        color: #212121;
        font-weight: 500;
    }
    h3 {
        color: #424242;
        font-weight: 500;
    }
    .stButton>button {
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("📊 Financial Research Tool")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    ["🏠 Market Overview", "📈 Stock Dashboard", "📥 Data Export", "💼 Portfolio", "⚠️ Watchlist"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.info(
    """
    This tool helps individual investors analyze financial data, 
    track portfolios, and make informed investment decisions.
    
    **Features:**
    - Real-time market overview
    - Stock analysis dashboard
    - Portfolio tracking
    - Data export to CSV
    - Historical analysis
    """
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Demo Version 1.0**")

# Main content area - route to appropriate page
if page == "🏠 Market Overview":
    market_overview.show()
elif page == "📈 Stock Dashboard":
    dashboard.show()
elif page == "📥 Data Export":
    data_export.show()
elif page == "💼 Portfolio":
    st.title("💼 Portfolio Tracker")
    st.info("Portfolio tracking feature coming soon! Use the Stock Dashboard to analyze individual stocks.")
elif page == "⚠️ Watchlist":
    st.title("⚠️ My Watchlist")
    st.info("Watchlist feature coming soon! Use the Stock Dashboard to analyze individual stocks.")


