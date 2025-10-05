"""
Market Overview page - Using Polygon.io API (No rate limit issues!)
"""
import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.api.polygon_fetcher import PolygonDataFetcher
from src.components.chart_generator import create_bar_chart, create_line_chart
from src.components.table_display import display_metrics_row, style_gainers_losers
from config.settings import DEFAULT_STOCKS, COLORS


@st.cache_data(ttl=3600)  # Cache for 1 hour
def fetch_market_data_polygon():
    """Fetch market data using Polygon.io - limited to 4 stocks for free tier."""
    fetcher = PolygonDataFetcher()
    
    # Limit to 4 stocks max for free tier (4 API calls)
    stocks_to_fetch = DEFAULT_STOCKS[:4]  
    
    # Get stock data with rate limiting built in
    stock_data = fetcher.get_multiple_tickers(stocks_to_fetch, max_tickers=4)
    
    return stock_data


def show():
    """Display the market overview page."""
    st.title("🏠 Market Overview (Polygon.io)")
    st.markdown("### Quick glance at today's market performance")
    st.info("📊 Using Polygon.io API - Free tier (4 stocks shown)")
    
    # Add refresh button
    col1, col2 = st.columns([8, 1])
    with col2:
        if st.button("🔄 Refresh"):
            st.cache_data.clear()
            st.rerun()
    
    st.markdown("---")
    
    try:
        # Fetch data
        with st.spinner("Loading market data (respecting rate limits)..."):
            stock_data = fetch_market_data_polygon()
        
        if not stock_data.empty:
            st.subheader("📈 Top Stocks")
            
            # Display stock metrics
            stock_metrics = {}
            for _, row in stock_data.iterrows():
                ticker = row['ticker']
                price = row['current_price']
                change = row['change']
                change_pct = row['change_percent']
                
                stock_metrics[ticker] = (
                    f"${price:,.2f}",
                    f"{change:+.2f} ({change_pct:+.2f}%)"
                )
            
            display_metrics_row(stock_metrics, num_columns=min(len(stock_metrics), 4))
            
            st.markdown("---")
            
            # Show detailed table
            st.subheader("📋 Stock Details")
            
            display_df = stock_data.copy()
            display_df['current_price'] = display_df['current_price'].apply(lambda x: f"${x:.2f}")
            display_df['change'] = display_df['change'].apply(lambda x: f"${x:+.2f}")
            display_df['change_percent'] = display_df['change_percent'].apply(lambda x: f"{x:+.2f}%")
            display_df['volume'] = display_df['volume'].apply(lambda x: f"{x:,}")
            
            # Select columns to display
            cols_to_show = ['ticker', 'current_price', 'change', 'change_percent', 'volume']
            display_df = display_df[cols_to_show]
            display_df.columns = ['Symbol', 'Price', 'Change ($)', 'Change (%)', 'Volume']
            
            st.dataframe(display_df, use_container_width=True, hide_index=True)
            
            st.markdown("---")
            
            # Market sentiment based on average change
            avg_change = stock_data['change_percent'].mean()
            
            col1, col2 = st.columns([1, 3])
            
            with col1:
                if avg_change > 0.5:
                    sentiment = "🟢 Bullish"
                elif avg_change < -0.5:
                    sentiment = "🔴 Bearish"
                else:
                    sentiment = "⚪ Neutral"
                
                st.metric("Market Sentiment", sentiment)
            
            with col2:
                if avg_change > 0.5:
                    st.success(f"📈 Markets are trending upward! Average change: +{avg_change:.2f}%")
                elif avg_change < -0.5:
                    st.error(f"📉 Markets are trending downward. Average change: {avg_change:.2f}%")
                else:
                    st.info(f"⚖️ Markets are relatively flat. Average change: {avg_change:.2f}%")
            
            # Show rate limit info
            st.markdown("---")
            st.caption(f"💡 Free tier limits: Showing 4 stocks | Data cached for 1 hour | Last updated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
        else:
            st.warning("No data available. Please check your Polygon.io API key.")
            st.info("Make sure your API key is set in the .env file: POLYGON_API_KEY=your_key_here")
    
    except Exception as e:
        st.error(f"Error loading market data: {str(e)}")
        st.info("""
        **Troubleshooting:**
        - Check that your Polygon.io API key is valid
        - Free tier allows 5 API calls per minute
        - Data is cached for 1 hour to minimize API calls
        - Try refreshing in a few moments
        """)


if __name__ == "__main__":
    show()
