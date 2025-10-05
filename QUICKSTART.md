# Quick Start Guide 🚀

## Starting Your Financial Research Tool

**To start the application, run this command in your terminal:**

```bash
cd "/Users/makwinglai/Desktop/Financial research tool"
streamlit run main.py
```

Or simply double-click and run:
```bash
./start_app.sh
```

Then open your browser to the URL shown (typically **http://localhost:8501**)

## What You Can Do Now

### 1️⃣ Explore Market Overview
- Click "🏠 Market Overview" in the sidebar
- View major indices (S&P 500, Dow Jones, NASDAQ)
- See top gainers and losers
- Check sector performance

### 2️⃣ Analyze Stocks
- Click "📈 Stock Dashboard" in the sidebar
- Enter any stock symbol (e.g., AAPL, TSLA, MSFT)
- Select a time period
- Click "Analyze" to see:
  - Current price and statistics
  - Interactive price charts
  - Technical indicators (RSI, MACD, Moving Averages)
  - Performance metrics
  - Company information

### 3️⃣ Export Data
- Click "📥 Data Export" in the sidebar
- Choose what to export:
  - Historical prices for any stock
  - Company fundamentals
  - Multiple stocks comparison
- Download as CSV for Excel or other tools

## Example Stocks to Try

**Tech Giants:**
- AAPL (Apple)
- MSFT (Microsoft)
- GOOGL (Google)
- AMZN (Amazon)
- TSLA (Tesla)

**Financial:**
- JPM (JPMorgan)
- BAC (Bank of America)
- V (Visa)

**Others:**
- WMT (Walmart)
- DIS (Disney)
- NFLX (Netflix)

## Troubleshooting

### App not loading?
1. Make sure you're at: http://localhost:8501
2. Check the terminal for errors
3. Try refreshing the page

### No data showing?
- Check your internet connection
- Try a different stock symbol
- Use the refresh button on the Market Overview page

### Want to restart?
```bash
# Stop the app (Ctrl+C in terminal)
# Then restart:
streamlit run main.py
```

## Next Steps

1. **Explore the Dashboard**: Try different stocks and time periods
2. **Export Data**: Download some CSV files for offline analysis
3. **Check Performance**: Look at technical indicators and metrics
4. **Update Data**: Run `python scripts/update_data.py` to refresh market data

## Need Help?

Check the main README.md for detailed documentation and troubleshooting tips.

---

**Tip**: Use Ctrl+C in the terminal to stop the application when you're done.


