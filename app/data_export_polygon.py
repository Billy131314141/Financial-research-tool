"""
Data Export page - export financial data to CSV files using Polygon.io.
"""
import streamlit as st
import pandas as pd
import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.api.polygon_fetcher import PolygonDataFetcher
from config.settings import CSV_DATE_FORMAT


def show():
    """Display the data export page."""
    st.title("📥 Data Export")
    st.markdown("### Export financial data to CSV files - Powered by Polygon.io")
    
    st.markdown("---")
    
    # Export type selection
    st.subheader("Select Data to Export")
    
    export_type = st.radio(
        "Data Type",
        ["Historical Prices", "Company Information"],
        help="Choose the type of data you want to export"
    )
    
    st.markdown("---")
    
    # Historical Prices Export
    if export_type == "Historical Prices":
        st.subheader("📈 Export Historical Price Data")
        
        col1, col2 = st.columns(2)
        
        with col1:
            ticker = st.text_input(
                "Stock Symbol",
                value="AAPL",
                placeholder="e.g., AAPL, MSFT",
                help="Enter the ticker symbol"
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
        
        if st.button("📥 Generate CSV", type="primary", use_container_width=True):
            try:
                with st.spinner(f"Fetching data for {ticker} from Polygon.io (this takes ~20 seconds due to rate limiting)..."):
                    fetcher = PolygonDataFetcher()
                    df = fetcher.get_historical_data(ticker, days_back=days_back)
                
                if df is not None and not df.empty:
                    # Format date
                    df_export = df.copy()
                    df_export['date'] = pd.to_datetime(df_export['date']).dt.strftime(CSV_DATE_FORMAT)
                    
                    # Show preview
                    st.success(f"✅ Data retrieved successfully! ({len(df_export)} rows)")
                    
                    st.markdown("##### Preview:")
                    st.dataframe(df_export.head(10), use_container_width=True)
                    
                    # Generate filename
                    filename = f"{ticker}_HistoricalPrices_{period_label.replace(' ', '')}_{datetime.now().strftime('%Y%m%d')}.csv"
                    
                    # Convert to CSV
                    csv = df_export.to_csv(index=False)
                    
                    # Download button
                    st.download_button(
                        label="⬇️ Download CSV",
                        data=csv,
                        file_name=filename,
                        mime="text/csv",
                        use_container_width=True
                    )
                    
                    # Show statistics
                    st.markdown("---")
                    st.markdown("##### Data Statistics:")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Total Rows", len(df_export))
                    with col2:
                        st.metric("Start Date", df_export['date'].iloc[0])
                    with col3:
                        st.metric("End Date", df_export['date'].iloc[-1])
                    with col4:
                        st.metric("Columns", len(df_export.columns))
                
                else:
                    st.error(f"❌ No data found for ticker: {ticker}")
                    st.info("Please check the ticker symbol and try again.")
            
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.info("Please check your Polygon.io API key or try again later.")
    
    # Company Information Export
    elif export_type == "Company Information":
        st.subheader("🏢 Export Company Information")
        
        ticker = st.text_input(
            "Stock Symbol",
            value="AAPL",
            placeholder="e.g., AAPL, MSFT",
            help="Enter the ticker symbol"
        ).upper()
        
        if st.button("📥 Generate CSV", type="primary", use_container_width=True):
            try:
                with st.spinner(f"Fetching information for {ticker} from Polygon.io..."):
                    fetcher = PolygonDataFetcher()
                    info = fetcher.get_stock_info(ticker)
                
                if info:
                    # Convert to DataFrame
                    df_export = pd.DataFrame([info]).T
                    df_export.columns = ['Value']
                    df_export.index.name = 'Metric'
                    
                    st.success("✅ Data retrieved successfully!")
                    
                    st.markdown("##### Preview:")
                    st.dataframe(df_export, use_container_width=True)
                    
                    # Generate filename
                    filename = f"{ticker}_CompanyInfo_{datetime.now().strftime('%Y%m%d')}.csv"
                    
                    # Convert to CSV
                    csv = df_export.to_csv()
                    
                    # Download button
                    st.download_button(
                        label="⬇️ Download CSV",
                        data=csv,
                        file_name=filename,
                        mime="text/csv",
                        use_container_width=True
                    )
                
                else:
                    st.error(f"❌ No data found for ticker: {ticker}")
            
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.info("Please check your Polygon.io API key.")
    
    # Information section
    st.markdown("---")
    st.info("""
    **💡 About Polygon.io Data Export:**
    - CSV files can be opened in Excel, Google Sheets, or any data analysis tool
    - Historical price data includes OHLC (Open, High, Low, Close) values
    - Data requests respect rate limits (15-second delays)
    - Data is sourced from Polygon.io's professional-grade API
    - Free tier provides up to 2 years of historical data
    
    **⏱️ Note:** Due to rate limiting (free tier), export may take ~20 seconds per request.
    This ensures we stay within API limits and you get reliable data!
    """)
    
    st.caption("📊 Data powered by Polygon.io")


if __name__ == "__main__":
    show()
