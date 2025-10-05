"""
Data Export page - export financial data to CSV files.
"""
import streamlit as st
import pandas as pd
import sys
import os
from datetime import datetime, timedelta

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.api.data_fetcher import DataFetcher
from config.settings import CSV_EXPORT_PATH, CSV_DATE_FORMAT


def show():
    """Display the data export page."""
    st.title("📥 Data Export")
    st.markdown("### Export financial data to CSV files for external analysis")
    
    st.markdown("---")
    
    # Export type selection
    st.subheader("Select Data to Export")
    
    export_type = st.radio(
        "Data Type",
        ["Historical Prices", "Company Fundamentals", "Multiple Stocks Comparison"],
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
                "1 Month": "1mo",
                "3 Months": "3mo",
                "6 Months": "6mo",
                "1 Year": "1y",
                "2 Years": "2y",
                "5 Years": "5y",
                "10 Years": "10y",
                "Max": "max"
            }
            period_label = st.selectbox("Time Period", list(period_options.keys()), index=3)
            period = period_options[period_label]
        
        # Additional options
        include_adjusted = st.checkbox("Include Adjusted Close", value=True)
        include_volume = st.checkbox("Include Volume", value=True)
        
        if st.button("📥 Generate CSV", type="primary", use_container_width=True):
            try:
                with st.spinner(f"Fetching data for {ticker}..."):
                    fetcher = DataFetcher()
                    df = fetcher.get_historical_data(ticker, period=period)
                
                if df is not None and not df.empty:
                    # Filter columns based on selection
                    columns_to_keep = ['date', 'open', 'high', 'low', 'close']
                    
                    if include_adjusted and 'adjusted_close' in df.columns:
                        columns_to_keep.append('adjusted_close')
                    
                    if include_volume and 'volume' in df.columns:
                        columns_to_keep.append('volume')
                    
                    # Filter and clean
                    df_export = df[[col for col in columns_to_keep if col in df.columns]].copy()
                    
                    # Format date
                    if 'date' in df_export.columns:
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
                        st.metric("Start Date", df_export['date'].iloc[0] if 'date' in df_export.columns else "N/A")
                    with col3:
                        st.metric("End Date", df_export['date'].iloc[-1] if 'date' in df_export.columns else "N/A")
                    with col4:
                        st.metric("Columns", len(df_export.columns))
                
                else:
                    st.error(f"❌ No data found for ticker: {ticker}")
                    st.info("Please check the ticker symbol and try again.")
            
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.info("Please try again or check your internet connection.")
    
    # Company Fundamentals Export
    elif export_type == "Company Fundamentals":
        st.subheader("🏢 Export Company Fundamental Data")
        
        ticker = st.text_input(
            "Stock Symbol",
            value="AAPL",
            placeholder="e.g., AAPL, MSFT",
            help="Enter the ticker symbol"
        ).upper()
        
        if st.button("📥 Generate CSV", type="primary", use_container_width=True):
            try:
                with st.spinner(f"Fetching fundamentals for {ticker}..."):
                    fetcher = DataFetcher()
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
                    filename = f"{ticker}_Fundamentals_{datetime.now().strftime('%Y%m%d')}.csv"
                    
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
    
    # Multiple Stocks Comparison
    elif export_type == "Multiple Stocks Comparison":
        st.subheader("📊 Export Multiple Stocks for Comparison")
        
        tickers_input = st.text_area(
            "Stock Symbols (comma-separated)",
            value="AAPL, MSFT, GOOGL",
            placeholder="e.g., AAPL, MSFT, GOOGL, AMZN",
            help="Enter multiple ticker symbols separated by commas"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            period_options = {
                "1 Month": "1mo",
                "3 Months": "3mo",
                "6 Months": "6mo",
                "1 Year": "1y",
                "2 Years": "2y",
                "5 Years": "5y"
            }
            period_label = st.selectbox("Time Period", list(period_options.keys()), index=3)
            period = period_options[period_label]
        
        with col2:
            data_point = st.selectbox(
                "Data Point",
                ["Close", "Adjusted Close", "Volume"],
                help="Which data point to compare"
            )
        
        if st.button("📥 Generate CSV", type="primary", use_container_width=True):
            try:
                # Parse tickers
                tickers = [t.strip().upper() for t in tickers_input.split(',') if t.strip()]
                
                if not tickers:
                    st.warning("Please enter at least one ticker symbol")
                    return
                
                with st.spinner(f"Fetching data for {len(tickers)} stocks..."):
                    fetcher = DataFetcher()
                    
                    # Fetch data for all tickers
                    all_data = {}
                    for ticker in tickers:
                        df = fetcher.get_historical_data(ticker, period=period)
                        if df is not None and not df.empty:
                            column_map = {
                                "Close": "close",
                                "Adjusted Close": "adjusted_close",
                                "Volume": "volume"
                            }
                            col = column_map.get(data_point, "close")
                            
                            if col in df.columns:
                                all_data[ticker] = df[['date', col]].copy()
                                all_data[ticker].columns = ['date', ticker]
                    
                    if not all_data:
                        st.error("❌ No data found for the provided tickers")
                        return
                    
                    # Merge all dataframes
                    df_export = all_data[list(all_data.keys())[0]]
                    for ticker in list(all_data.keys())[1:]:
                        df_export = df_export.merge(all_data[ticker], on='date', how='outer')
                    
                    # Sort by date
                    df_export = df_export.sort_values('date')
                    
                    # Format date
                    df_export['date'] = pd.to_datetime(df_export['date']).dt.strftime(CSV_DATE_FORMAT)
                    
                    st.success(f"✅ Data retrieved for {len(all_data)} stocks! ({len(df_export)} rows)")
                    
                    st.markdown("##### Preview:")
                    st.dataframe(df_export.head(10), use_container_width=True)
                    
                    # Generate filename
                    filename = f"Comparison_{period_label.replace(' ', '')}_{datetime.now().strftime('%Y%m%d')}.csv"
                    
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
            
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    # Information section
    st.markdown("---")
    st.info("""
    **💡 Tips:**
    - CSV files can be opened in Excel, Google Sheets, or any data analysis tool
    - Historical price data includes OHLC (Open, High, Low, Close) values
    - Adjusted close accounts for stock splits and dividends
    - Data is sourced from Yahoo Finance via yfinance
    """)


if __name__ == "__main__":
    show()


