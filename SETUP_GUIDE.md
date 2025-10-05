# 🚀 Setup Guide for Financial Research Tool

This guide will help you set up the Financial Research Tool on your local machine.

---

## 📋 Prerequisites

Before you begin, ensure you have:

- **Python 3.8 or higher** installed
- **pip** (Python package manager)
- **Git** (for cloning the repository)
- Internet connection for API access

---

## 🔧 Installation Steps

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/financial-research-tool.git
cd financial-research-tool
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install all required packages including:
- Streamlit (web framework)
- Transformers & PyTorch (for FinBERT AI)
- Pandas, NumPy (data processing)
- Plotly (visualizations)
- Requests (API calls)

### Step 4: Set Up API Keys

1. **Copy the environment template:**
```bash
cp .env.example .env
```

2. **Get your API keys:**

| API | Sign Up Link | Free Tier |
|-----|--------------|-----------|
| Polygon.io | https://polygon.io/ | 5 calls/min |
| newsdata.io | https://newsdata.io/register | 200 calls/day |
| API Ninjas | https://api-ninjas.com/ | 50,000 calls/month |

3. **Edit `.env` file:**
```bash
# Open with your preferred editor
nano .env
# or
code .env
```

4. **Add your keys:**
```bash
POLYGON_API_KEY=your_actual_polygon_key_here
NEWS_API_KEY=your_actual_newsdata_key_here
API_NINJAS_KEY=your_actual_api_ninjas_key_here
```

### Step 5: Run the Application

```bash
streamlit run main.py
```

The application will automatically open in your default browser at `http://localhost:8501`

---

## 🎯 First-Time Usage

### Test the Application:

1. **Bloomberg Dashboard**
   - Navigate to "⚡ Bloomberg Terminal" in the sidebar
   - View real-time market data
   - Explore interactive charts

2. **Earnings Transcript Analysis**
   - Go to "📊 Earnings Transcript Analysis"
   - Try the pre-filled example: MSFT, Year 2024, Quarter 2
   - Click "🚀 ANALYZE" to see AI sentiment analysis

3. **News API Test**
   - Navigate to "📰 News API Test"
   - Test your newsdata.io API key
   - View real-time financial news

---

## ⚙️ Configuration

### Customize Settings

Edit `config/settings.py` to customize:
- Default stock tickers
- Refresh intervals
- API timeouts
- Cache durations

Example:
```python
# config/settings.py
DEFAULT_STOCKS = ['AAPL', 'MSFT', 'GOOGL', 'TSLA']
CACHE_DURATION = 3600  # 1 hour
```

---

## 🐛 Troubleshooting

### Common Issues:

**1. ModuleNotFoundError**
```bash
# Solution: Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**2. API Key Invalid**
```bash
# Solution: Check your .env file
cat .env
# Ensure no extra spaces or quotes around keys
```

**3. Port Already in Use**
```bash
# Solution: Use a different port
streamlit run main.py --server.port 8502
```

**4. FinBERT Model Download Slow**
```bash
# First run downloads ~438MB model
# This is normal and only happens once
# Subsequent runs use cached model
```

---

## 📊 Performance Tips

### Optimize Performance:

1. **Use caching effectively**
   - Data is cached for 1 hour by default
   - Reduces API calls and speeds up loading

2. **Close unused browser tabs**
   - Each tab maintains a separate session

3. **Monitor API usage**
   - Check your API dashboards regularly
   - Stay within free tier limits

### API Rate Limits:

| API | Free Limit | Best Practice |
|-----|------------|---------------|
| Polygon.io | 5 calls/min | Cache aggressively |
| newsdata.io | 200 calls/day | Limit news refreshes |
| API Ninjas | 50,000 calls/month | More than enough |

---

## 🔄 Updating the Application

```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Restart the app
streamlit run main.py
```

---

## 🧪 Running Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest tests/

# With coverage
pytest --cov=src tests/
```

---

## 📱 Deployment Options

### Deploy to Streamlit Cloud (Free):

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Add your API keys in "Secrets" section
5. Deploy!

### Deploy to Heroku:

```bash
# Create Procfile
echo "web: streamlit run main.py --server.port $PORT" > Procfile

# Deploy
heroku create your-app-name
git push heroku main
```

---

## 💾 Data Storage

The application stores data in:
- `data/cache/` - Cached API responses
- `data/exports/` - Exported reports
- `.streamlit/` - Streamlit configuration

All data folders are gitignored to keep your repository clean.

---

## 🔐 Security Best Practices

1. **Never commit `.env` file**
   - Already in `.gitignore`
   - Use `.env.example` as template

2. **Rotate API keys regularly**
   - Especially if you share code

3. **Use environment-specific keys**
   - Development vs Production

4. **Monitor API usage**
   - Set up alerts for quota limits

---

## 📚 Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [FinBERT Model](https://huggingface.co/ProsusAI/finbert)
- [Polygon.io API Docs](https://polygon.io/docs/)
- [newsdata.io Docs](https://newsdata.io/documentation)
- [API Ninjas Docs](https://api-ninjas.com/api/earningstranscript)

---

## 🆘 Getting Help

If you encounter issues:

1. Check this guide first
2. Search existing [GitHub Issues](https://github.com/YOUR_USERNAME/financial-research-tool/issues)
3. Create a new issue with:
   - Error message
   - Steps to reproduce
   - Your environment (OS, Python version)

---

## ✅ Verification Checklist

Before using the app, verify:

- [ ] Python 3.8+ installed
- [ ] All dependencies installed successfully
- [ ] `.env` file created with valid API keys
- [ ] Application starts without errors
- [ ] Can load Bloomberg Dashboard
- [ ] Can fetch earnings transcript
- [ ] News API returns data

---

**Ready to go! 🚀**

If everything is set up correctly, you should now have a fully functional Financial Research Tool running on your local machine.

For questions or issues, please open a GitHub issue or contact the maintainer.

