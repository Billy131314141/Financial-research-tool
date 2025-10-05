"""
Stock Dashboard page - Using Polygon.io API exclusively.
"""
import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.api.polygon_fetcher import PolygonDataFetcher
from src.processing.feature_engineer import add_all_features
from src.analysis.historical_analysis import calculate_performance_metrics
from src.components.chart_generator import (
    create_candlestick_chart, create_line_chart, 
    create_volume_chart, create_multi_line_chart
)
from src.components.table_display import display_key_stats, display_metrics_row
from config.settings import COLORS


@st.cache_data(ttl=3600)
def fetch_stock_data_polygon(ticker: str, days_back: int = 365):
    """Fetch comprehensive stock data using Polygon.io."""
    fetcher = PolygonDataFetcher()
    
    # Get stock info
    info = fetcher.get_stock_info(ticker)
    
    # Get current price
    price = fetcher.get_current_price(ticker)
    
    # Get historical data
    historical = fetcher.get_historical_data(ticker, days_back=days_back)
    
    return info, price, historical


def show():
    """Display the stock dashboard page."""
    st.title("📈 Stock Analysis Dashboard")
    st.markdown("### Detailed analysis powered by Polygon.io")
    
    # Stock symbol input
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        ticker = st.text_input(
            "Enter Stock Symbol",
            value="AAPL",
            placeholder="e.g., AAPL, MSFT, GOOGL",
            help="Enter a valid stock ticker symbol"
        ).upper()
    
    with col2:
        period_options = {
            "1 Month": 30,
            "3 Months": 90,
            "6 Months": 180,
            "1 Year": 365,
            "2 Years": 730
        }
        period_label = st.selectbox("Time Period", list(period_options.keys()), index=3)
        days_back = period_options[period_label]
    
    with col3:
        analyze_btn = st.button("🔍 Analyze", type="primary", use_container_width=True)
    
    # Only analyze when button is clicked or initial load
    if analyze_btn or 'last_ticker' not in st.session_state:
        st.session_state.last_ticker = ticker
    
    if st.session_state.get('last_ticker'):
        ticker = st.session_state.last_ticker
        
        try:
            with st.spinner(f"Loading data for {ticker} from Polygon.io (this may take ~30 seconds due to rate limiting)..."):
                info, price, historical = fetch_stock_data_polygon(ticker, days_back)
            
            if info is None or price is None:
                st.error(f"Could not find data for ticker: {ticker}")
                st.info("Please check the ticker symbol and try again.")
                return
            
            st.markdown("---")
            
            # Display stock header and key metrics
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"## {info['company_name']} ({ticker})")
                st.markdown(f"**{info['exchange']}** | {info['sector']}")
            
            with col2:
                change_color = "normal" if price['change'] >= 0 else "inverse"
                st.metric(
                    "Current Price",
                    f"${price['current_price']:.2f}",
                    f"{price['change']:+.2f} ({price['change_percent']:+.2f}%)",
                    delta_color=change_color
                )
            
            # Key statistics
            st.markdown("---")
            st.subheader("📊 Key Statistics")
            
            stats = {
                "Open": f"${price['open']:.2f}",
                "Day High": f"${price['day_high']:.2f}",
                "Day Low": f"${price['day_low']:.2f}",
                "Previous Close": f"${price['previous_close']:.2f}",
                "Volume": f"{price['volume']:,}"
            }
            
            display_key_stats(stats, columns=5)
            
            # Historical data analysis
            if historical is not None and not historical.empty:
                st.markdown("---")
                st.subheader("📈 Price Chart")
                
                # Chart type selector
                chart_col1, chart_col2 = st.columns([1, 4])
                
                with chart_col1:
                    chart_type = st.radio(
                        "Chart Type",
                        ["Candlestick", "Line"],
                        help="Select chart visualization type"
                    )
                
                with chart_col2:
                    if chart_type == "Candlestick":
                        fig = create_candlestick_chart(
                            historical,
                            title=f"{ticker} Price - {period_label}"
                        )
                    else:
                        fig = create_line_chart(
                            historical,
                            x_column='date',
                            y_column='close',
                            title=f"{ticker} Price - {period_label}",
                            y_label="Close Price",
                            color=COLORS['info']
                        )
                    
                    st.plotly_chart(fig, use_container_width=True)
                
                # Volume chart
                with st.expander("📊 View Trading Volume"):
                    vol_fig = create_volume_chart(historical, title=f"{ticker} Volume")
                    st.plotly_chart(vol_fig, use_container_width=True)
                
                st.markdown("---")
                
                # Technical indicators
                st.subheader("🔧 Technical Analysis")
                
                # Add technical indicators
                historical_with_features = add_all_features(historical, 'close')
                
                # Display moving averages
                st.markdown("##### Moving Averages")
                
                ma_fig = create_multi_line_chart(
                    historical_with_features,
                    x_column='date',
                    y_columns=['close', 'ma_20', 'ma_50', 'ma_200'],
                    title=f"{ticker} - Price with Moving Averages",
                    y_label="Price"
                )
                st.plotly_chart(ma_fig, use_container_width=True)
                
                # RSI
                with st.expander("📉 Relative Strength Index (RSI)"):
                    if 'rsi' in historical_with_features.columns:
                        rsi_fig = create_line_chart(
                            historical_with_features,
                            x_column='date',
                            y_column='rsi',
                            title=f"{ticker} - RSI (14)",
                            y_label="RSI",
                            color=COLORS['warning']
                        )
                        st.plotly_chart(rsi_fig, use_container_width=True)
                        
                        # RSI interpretation
                        current_rsi = historical_with_features['rsi'].iloc[-1]
                        if current_rsi > 70:
                            st.warning(f"⚠️ RSI: {current_rsi:.2f} - Potentially Overbought")
                        elif current_rsi < 30:
                            st.info(f"ℹ️ RSI: {current_rsi:.2f} - Potentially Oversold")
                        else:
                            st.success(f"✅ RSI: {current_rsi:.2f} - Neutral")
                
                # MACD
                with st.expander("📊 MACD"):
                    if 'macd' in historical_with_features.columns:
                        macd_fig = create_multi_line_chart(
                            historical_with_features,
                            x_column='date',
                            y_columns=['macd', 'macd_signal'],
                            title=f"{ticker} - MACD",
                            y_label="MACD"
                        )
                        st.plotly_chart(macd_fig, use_container_width=True)
                
                st.markdown("---")
                
                # Performance metrics
                st.subheader("📊 Performance Metrics")
                
                metrics = calculate_performance_metrics(historical, 'close')
                
                perf_col1, perf_col2, perf_col3, perf_col4 = st.columns(4)
                
                with perf_col1:
                    st.metric("Total Return", f"{metrics.get('total_return', 0):.2f}%")
                    st.metric("YTD Return", f"{metrics.get('ytd_return', 0):.2f}%")
                
                with perf_col2:
                    st.metric("1Y Return", f"{metrics.get('1y_return', 0):.2f}%")
                    st.metric("Volatility", f"{metrics.get('annualized_volatility', 0):.2f}%")
                
                with perf_col3:
                    st.metric("Max Drawdown", f"{metrics.get('max_drawdown_pct', 0):.2f}%")
                    st.metric("Sharpe Ratio", f"{metrics.get('sharpe_ratio', 0):.2f}")
                
                with perf_col4:
                    st.metric("52W High", f"${metrics.get('high_52week', 0):.2f}")
                    st.metric("52W Low", f"${metrics.get('low_52week', 0):.2f}")
                
                # Company description
                if info.get('description'):
                    st.markdown("---")
                    with st.expander("ℹ️ About " + info['company_name']):
                        st.write(info['description'])
                        if info.get('website'):
                            st.markdown(f"**Website:** {info['website']}")
            
            else:
                st.warning(f"No historical data available for {ticker}")
            
            # Data source info
            st.caption("📊 Data powered by Polygon.io | Cached for 1 hour")
        
        except Exception as e:
            st.error(f"Error loading data: {str(e)}")
            st.info("Please try a different ticker or check your Polygon.io API key.")


if __name__ == "__main__":
    show()
