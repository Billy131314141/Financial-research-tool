# Financial Research Tool Demo 📊

A comprehensive financial research tool for individual investors to analyze stocks, track portfolios, and make informed investment decisions.

## 🎯 Features

- **📈 Stock Analysis Dashboard**: Detailed analysis with technical indicators, charts, and performance metrics
- **🏠 Market Overview**: At-a-glance view of market indices, top gainers/losers, and sector performance
- **📥 Data Export**: Export historical data and fundamentals to CSV for external analysis
- **💼 Portfolio Tracking**: Track your investments and monitor performance (coming soon)
- **⚠️ Watchlists**: Create and manage custom stock watchlists (coming soon)

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- pip (Python package installer)
- Internet connection for fetching market data

### Installation

1. **Clone or download the repository**

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the setup script**
   ```bash
   python scripts/setup_env.py
   ```
   
   This will:
   - Initialize the SQLite database
   - Create necessary directories
   - Download required NLTK data
   - Optionally fetch initial market data

4. **Launch the application**
   ```bash
   streamlit run main.py
   ```

5. **Open your browser** to the URL displayed (typically `http://localhost:8501`)

## 📁 Project Structure

```
Financial research tool/
├── main.py                 # Main Streamlit application entry point
├── requirements.txt        # Python dependencies
├── README.md              # This file
│
├── app/                   # Streamlit pages
│   ├── dashboard.py       # Stock analysis dashboard
│   ├── market_overview.py # Market overview page
│   └── data_export.py     # Data export functionality
│
├── config/                # Configuration files
│   ├── settings.py        # Application settings
│   └── watchlists.py      # Default watchlists
│
├── src/                   # Core source code
│   ├── api/              # API integration
│   │   └── data_fetcher.py
│   ├── processing/       # Data processing
│   │   ├── data_cleaner.py
│   │   └── feature_engineer.py
│   ├── analysis/         # Analysis modules
│   │   ├── historical_analysis.py
│   │   ├── portfolio_tracker.py
│   │   └── sentiment_analyzer.py
│   ├── components/       # UI components
│   │   ├── chart_generator.py
│   │   └── table_display.py
│   └── utils/           # Utilities
│       └── database.py
│
├── scripts/             # Helper scripts
│   ├── setup_env.py    # Environment setup
│   └── update_data.py  # Data update script
│
└── data/               # Data storage
    ├── raw/           # Raw API data
    ├── processed/     # Processed data
    └── exports/       # Exported CSV files
```

## 📊 Usage Guide

### Market Overview
- View major market indices (S&P 500, Dow Jones, NASDAQ)
- See top gainers and losers
- Analyze sector performance
- Check overall market sentiment

### Stock Dashboard
1. Enter a stock symbol (e.g., AAPL, MSFT, GOOGL)
2. Select time period for analysis
3. Click "Analyze" to load data
4. View:
   - Current price and key statistics
   - Interactive price charts (candlestick or line)
   - Technical indicators (Moving Averages, RSI, MACD)
   - Performance metrics (returns, volatility, Sharpe ratio)
   - Company information

### Data Export
1. Choose export type:
   - Historical Prices
   - Company Fundamentals
   - Multiple Stocks Comparison
2. Configure parameters (ticker, time period, etc.)
3. Click "Generate CSV"
4. Preview the data
5. Click "Download CSV" to save

## 🔧 Configuration

### API Keys
For advanced features (news data), you can set API keys:
- Create a `.env` file in the project root
- Add: `NEWS_API_KEY=your_key_here`

### Default Settings
Edit `config/settings.py` to customize:
- Default stocks and indices
- Chart colors and themes
- Cache settings
- Update frequency

## 📈 Technical Indicators

The tool provides various technical indicators:
- **Moving Averages** (20, 50, 200-day)
- **RSI** (Relative Strength Index)
- **MACD** (Moving Average Convergence Divergence)
- **Bollinger Bands**
- **Volatility** (Daily and Annualized)

## 🔄 Updating Data

To fetch the latest market data:
```bash
python scripts/update_data.py
```

This script can be scheduled to run periodically (e.g., hourly) using cron (Linux/Mac) or Task Scheduler (Windows).

## 📝 Data Sources

- **Stock Data**: Yahoo Finance (via yfinance library)
- **Market Indices**: Yahoo Finance
- **Company Fundamentals**: Yahoo Finance

## ⚠️ Limitations

- Data is delayed (not real-time)
- Free API rate limits apply
- Local deployment only (single user)
- Demo version with basic features

## 🛠️ Troubleshooting

### Issue: Module not found error
**Solution**: Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Issue: No data returned for ticker
**Solution**: 
- Check the ticker symbol is correct
- Verify internet connection
- Try a different ticker
- Check if market is open

### Issue: Charts not displaying
**Solution**:
- Clear browser cache
- Refresh the page
- Check console for errors

## 🔮 Future Enhancements

- [ ] Real-time data integration
- [ ] Advanced portfolio analytics
- [ ] Alert notifications
- [ ] Custom watchlists with persistence
- [ ] Social sentiment analysis
- [ ] Comparison tools
- [ ] Mobile-responsive design
- [ ] Cloud deployment

## 📄 License

This is a demo project for personal use.

## 🤝 Contributing

This is a personal demo project, but suggestions are welcome!

## 📧 Contact

For questions or issues, please refer to the project documentation.

---

**Disclaimer**: This tool is for educational and research purposes only. It does not provide investment advice. Always do your own research and consult with financial professionals before making investment decisions.


