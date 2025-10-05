# 📊 Financial Research Tool

> **A Professional Financial Analysis Platform with AI-Powered Sentiment Analysis**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-FF4B4B.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A Bloomberg-inspired financial research platform featuring real-time stock data, AI sentiment analysis of earnings calls, and professional visualizations. Built with Python and Streamlit.

![Financial Research Tool Demo](https://via.placeholder.com/800x400/0D1117/00D4FF?text=Financial+Research+Tool)

---

## ✨ Key Features

### 📈 **Real-Time Market Data**
- Live stock quotes from Polygon.io API
- Historical price data and technical indicators
- Interactive charts with customizable timeframes
- Support for stocks, indices, and cryptocurrencies

### 🤖 **AI Sentiment Analysis**
- **FinBERT** model for financial text analysis
- Earnings call transcript sentiment scoring
- News sentiment analysis
- Segment-by-segment confidence scores

### 📰 **News Integration**
- Real-time financial news from newsdata.io
- Company-specific news filtering
- Sentiment analysis on news articles
- Source tracking and credibility indicators

### 📊 **Bloomberg-Style Dashboard**
- Professional dark theme interface
- Real-time data updates
- Interactive correlation heatmaps
- Network graphs for indicator relationships

### 💼 **Earnings Transcript Analyzer**
- Fetch complete earnings call transcripts (API Ninjas)
- AI-powered sentiment analysis
- Full transcript viewer with highlighting
- Historical quarter comparisons

---

## 🚀 Quick Start

### Prerequisites

```bash
Python 3.8+
pip (Python package manager)
```

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/financial-research-tool.git
cd financial-research-tool
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up API keys**
```bash
# Copy the environment template
cp .env.example .env

# Edit .env and add your API keys
nano .env  # or use your preferred editor
```

4. **Run the application**
```bash
streamlit run main.py
```

5. **Open in browser**
```
http://localhost:8501
```

---

## 🔑 API Keys Required

This project uses several APIs. Get your free keys here:

| API | Purpose | Free Tier | Get Key |
|-----|---------|-----------|---------|
| **Polygon.io** | Stock data | 5 calls/min | [polygon.io](https://polygon.io/) |
| **newsdata.io** | Financial news | 200 calls/day | [newsdata.io](https://newsdata.io/register) |
| **API Ninjas** | Earnings transcripts | 50,000 calls/month | [api-ninjas.com](https://api-ninjas.com/) |
| **FMP** (optional) | Additional data | 250 calls/day | [financialmodelingprep.com](https://financialmodelingprep.com/) |

Add your keys to `.env`:

```bash
POLYGON_API_KEY=your_key_here
NEWS_API_KEY=your_key_here
API_NINJAS_KEY=your_key_here
FMP_API_KEY=your_key_here  # optional
```

---

## 📁 Project Structure

```
financial-research-tool/
├── app/                          # Streamlit pages
│   ├── bloomberg_dashboard.py   # Main Bloomberg-style interface
│   ├── simple_earnings_analysis.py  # Earnings transcript analyzer
│   ├── sentiment_analysis.py    # AI sentiment analysis page
│   ├── news_test_page.py        # News API testing
│   ├── market_overview_polygon.py   # Market overview
│   ├── dashboard_polygon.py     # Stock dashboard
│   └── data_export_polygon.py   # Data export tools
├── src/
│   ├── api/                      # API integrations
│   │   ├── polygon_fetcher.py   # Polygon.io client
│   │   ├── newsdata_fetcher.py  # newsdata.io client
│   │   └── fmp_transcript_fetcher.py  # FMP client
│   ├── analysis/                 # Analysis modules
│   │   └── finbert_sentiment.py # FinBERT sentiment analyzer
│   └── utils/                    # Utility functions
├── config/
│   └── settings.py              # Configuration
├── data/                         # Data storage
├── main.py                       # Application entry point
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

---

## 💡 Usage Examples

### 1. **Analyze Stock Sentiment**

```python
from src.analysis.finbert_sentiment import FinBERTAnalyzer

analyzer = FinBERTAnalyzer()
text = "Revenue grew 25% YoY, exceeding expectations."
result = analyzer.analyze_single(text)
print(result)  # {'sentiment': 'positive', 'confidence': 0.89}
```

### 2. **Fetch Stock Data**

```python
from src.api.polygon_fetcher import PolygonFetcher

fetcher = PolygonFetcher(api_key="your_key")
data = fetcher.get_stock_info("AAPL")
print(data['current_price'])
```

### 3. **Get Earnings Transcript**

Navigate to **📊 Earnings Transcript Analysis** page:
- Enter ticker: `MSFT`
- Select year: `2024`
- Select quarter: `Q2`
- Click **ANALYZE**

---

## 🎨 Features Showcase

### Bloomberg Dashboard
- Professional dark theme
- Real-time price updates
- Technical indicators
- Interactive charts

### AI Sentiment Analysis
- FinBERT model (fine-tuned on financial text)
- Confidence scores
- Segment-level analysis
- Visual sentiment breakdown

### Earnings Transcript Analyzer
- Complete transcript viewing
- AI sentiment scoring
- Historical comparison
- Downloadable reports

---

## 🛠️ Technologies Used

### Core
- **Python 3.8+** - Programming language
- **Streamlit** - Web framework
- **Pandas** - Data manipulation
- **NumPy** - Numerical computing

### Data Sources
- **Polygon.io** - Real-time market data
- **newsdata.io** - Financial news
- **API Ninjas** - Earnings transcripts
- **Financial Modeling Prep** - Additional financial data

### AI/ML
- **FinBERT** - Financial sentiment analysis
- **Transformers** - Hugging Face library
- **PyTorch** - Deep learning framework

### Visualization
- **Plotly** - Interactive charts
- **Matplotlib** - Statistical plotting
- **Seaborn** - Data visualization

---

## 📊 Performance

- **Page Load**: < 2 seconds
- **API Response**: < 1 second (cached)
- **Sentiment Analysis**: ~30 seconds for full transcript
- **Real-time Updates**: Every 5 seconds

---

## 🔒 Security

- ✅ API keys stored in `.env` (not committed)
- ✅ Environment variables for sensitive data
- ✅ `.gitignore` configured for security
- ✅ No hardcoded credentials

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Your Name**
- Portfolio: [your-portfolio.com](https://your-portfolio.com)
- LinkedIn: [linkedin.com/in/yourprofile](https://linkedin.com/in/yourprofile)
- GitHub: [@yourusername](https://github.com/yourusername)

---

## 🙏 Acknowledgments

- **FinBERT** - ProsusAI for the financial sentiment model
- **Streamlit** - For the amazing web framework
- **Polygon.io** - For reliable market data
- **API Ninjas** - For earnings transcript access

---

## 📬 Contact

For questions or collaboration:
- **Email**: your.email@example.com
- **LinkedIn**: [Your Profile](https://linkedin.com/in/yourprofile)

---

<div align="center">

### ⭐ If you found this project helpful, please consider giving it a star!

**Built with ❤️ for financial analysis enthusiasts**

</div>

