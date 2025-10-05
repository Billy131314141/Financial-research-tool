"""
Market Overview page - displays at-a-glance market information.
"""
import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.api.data_fetcher import DataFetcher
from src.components.chart_generator import create_bar_chart, create_line_chart
from src.components.table_display import display_metrics_row, display_stock_table, style_gainers_losers
from config.settings import DEFAULT_INDICES, DEFAULT_STOCKS, COLORS


@st.cache_data(ttl=3600)  # Cache for 1 hour
def fetch_market_data():
    """Fetch all market overview data."""
    fetcher = DataFetcher()
    
    # Get indices data
    indices_list = list(DEFAULT_INDICES.keys())
    indices_data = fetcher.get_market_indices(indices_list)
    
    # Get gainers/losers
    gainers_losers = fetcher.get_top_gainers_losers(DEFAULT_STOCKS)
    
    # Get sector performance
    sector_perf = fetcher.get_sector_performance(DEFAULT_STOCKS)
    
    return indices_data, gainers_losers, sector_perf


def show():
    """Display the market overview page."""
    st.title("🏠 Market Overview")
    st.markdown("### Quick glance at today's market performance")
    
    # Add refresh button
    col1, col2, col3 = st.columns([6, 1, 1])
    with col3:
        if st.button("🔄 Refresh"):
            st.cache_data.clear()
            st.rerun()
    
    st.markdown("---")
    
    try:
        # Fetch data
        with st.spinner("Loading market data..."):
            indices_data, gainers_losers, sector_perf = fetch_market_data()
        
        # Display Major Indices
        st.subheader("📊 Major Market Indices")
        
        if not indices_data.empty:
            # Create metrics for indices
            indices_metrics = {}
            for _, row in indices_data.iterrows():
                symbol = row['ticker']
                name = DEFAULT_INDICES.get(symbol, symbol)
                price = row['current_price']
                change = row['change']
                change_pct = row['change_percent']
                
                indices_metrics[name] = (
                    f"${price:,.2f}",
                    f"{change:+.2f} ({change_pct:+.2f}%)"
                )
            
            display_metrics_row(indices_metrics, num_columns=len(indices_metrics))
            
            # Show mini chart for S&P 500
            st.markdown("---")
            fetcher = DataFetcher()
            sp500_hist = fetcher.get_historical_data("^GSPC", period="1mo", interval="1d")
            
            if sp500_hist is not None and not sp500_hist.empty:
                fig = create_line_chart(
                    sp500_hist,
                    x_column='date',
                    y_column='close',
                    title="S&P 500 - Last 30 Days",
                    color=COLORS['info']
                )
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Unable to load indices data")
        
        st.markdown("---")
        
        # Display Top Gainers and Losers
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Top Gainers")
            gainers = gainers_losers.get('gainers', pd.DataFrame())
            
            if not gainers.empty:
                gainers_display = gainers[['ticker', 'current_price', 'change', 'change_percent']].copy()
                gainers_display.columns = ['Symbol', 'Price', 'Change', 'Change %']
                gainers_display = style_gainers_losers(gainers_display)
                st.dataframe(gainers_display, use_container_width=True, hide_index=True)
            else:
                st.info("No gainers data available")
        
        with col2:
            st.subheader("📉 Top Losers")
            losers = gainers_losers.get('losers', pd.DataFrame())
            
            if not losers.empty:
                losers_display = losers[['ticker', 'current_price', 'change', 'change_percent']].copy()
                losers_display.columns = ['Symbol', 'Price', 'Change', 'Change %']
                losers_display = style_gainers_losers(losers_display)
                st.dataframe(losers_display, use_container_width=True, hide_index=True)
            else:
                st.info("No losers data available")
        
        st.markdown("---")
        
        # Display Sector Performance
        st.subheader("🏭 Sector Performance")
        
        if not sector_perf.empty:
            fig = create_bar_chart(
                sector_perf,
                x_column='sector',
                y_column='avg_change',
                title="Average Change by Sector (%)",
                color_column='avg_change',
                horizontal=True
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Show sector details
            with st.expander("📋 View Sector Details"):
                sector_display = sector_perf.copy()
                sector_display['avg_change'] = sector_display['avg_change'].apply(lambda x: f"{x:.2f}%")
                sector_display.columns = ['Sector', 'Avg Change (%)', 'Stocks Count']
                st.dataframe(sector_display, use_container_width=True, hide_index=True)
        else:
            st.info("Sector performance data not available")
        
        st.markdown("---")
        
        # Market Summary
        st.subheader("📰 Market Summary")
        
        if not indices_data.empty:
            # Calculate overall market sentiment
            avg_change = indices_data['change_percent'].mean()
            
            if avg_change > 0.5:
                sentiment = "🟢 Bullish"
                sentiment_text = "Markets are trending upward today."
            elif avg_change < -0.5:
                sentiment = "🔴 Bearish"
                sentiment_text = "Markets are trending downward today."
            else:
                sentiment = "⚪ Neutral"
                sentiment_text = "Markets are relatively flat today."
            
            col1, col2 = st.columns([1, 3])
            with col1:
                st.metric("Market Sentiment", sentiment)
            with col2:
                st.info(sentiment_text)
        
        # Last updated timestamp
        st.caption(f"Last updated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except Exception as e:
        st.error(f"Error loading market data: {str(e)}")
        st.info("Please try refreshing the page or check your internet connection.")


if __name__ == "__main__":
    show()


