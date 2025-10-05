"""
Bloomberg-style Professional Dashboard with Sentiment Analysis and Indicator Relationships
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.api.polygon_fetcher import PolygonDataFetcher
from src.processing.feature_engineer import add_all_features
from src.analysis.historical_analysis import calculate_performance_metrics
from src.analysis.finbert_sentiment import get_analyzer


# Bloomberg-style color scheme
BLOOMBERG_COLORS = {
    'bg_dark': '#0D1117',
    'bg_medium': '#161B22',
    'bg_light': '#21262D',
    'accent_orange': '#FF6B35',
    'accent_blue': '#00D4FF',
    'accent_green': '#00FF88',
    'text_primary': '#E6EDF3',
    'text_secondary': '#8B949E',
    'border': '#30363D'
}


def apply_bloomberg_style():
    """Apply Bloomberg-inspired dark theme CSS"""
    st.markdown(f"""
        <style>
        /* Main background */
        .stApp {{
            background-color: {BLOOMBERG_COLORS['bg_dark']};
            color: {BLOOMBERG_COLORS['text_primary']};
        }}
        
        /* Sidebar */
        [data-testid="stSidebar"] {{
            background-color: {BLOOMBERG_COLORS['bg_medium']};
            border-right: 1px solid {BLOOMBERG_COLORS['border']};
        }}
        
        /* Headers */
        h1, h2, h3 {{
            color: {BLOOMBERG_COLORS['text_primary']} !important;
            font-family: 'Helvetica Neue', sans-serif;
            font-weight: 600;
        }}
        
        /* Metrics */
        [data-testid="stMetricValue"] {{
            color: {BLOOMBERG_COLORS['accent_blue']};
            font-size: 2rem;
            font-weight: 700;
        }}
        
        [data-testid="stMetricLabel"] {{
            color: {BLOOMBERG_COLORS['text_secondary']};
            font-size: 0.875rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        
        [data-testid="stMetricDelta"] {{
            font-size: 1rem;
        }}
        
        /* Cards/Containers */
        .element-container {{
            background-color: {BLOOMBERG_COLORS['bg_medium']};
            border-radius: 4px;
        }}
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {{
            background-color: {BLOOMBERG_COLORS['bg_medium']};
            border-bottom: 2px solid {BLOOMBERG_COLORS['accent_orange']};
        }}
        
        .stTabs [data-baseweb="tab"] {{
            color: {BLOOMBERG_COLORS['text_secondary']};
            font-weight: 600;
            padding: 12px 24px;
            border-radius: 0;
        }}
        
        .stTabs [aria-selected="true"] {{
            background-color: {BLOOMBERG_COLORS['bg_light']};
            color: {BLOOMBERG_COLORS['accent_orange']};
            border-bottom: 3px solid {BLOOMBERG_COLORS['accent_orange']};
        }}
        
        /* Input fields */
        .stTextInput input {{
            background-color: {BLOOMBERG_COLORS['bg_light']};
            color: {BLOOMBERG_COLORS['text_primary']};
            border: 1px solid {BLOOMBERG_COLORS['border']};
            border-radius: 2px;
            font-family: 'Monaco', 'Courier New', monospace;
            font-size: 1rem;
        }}
        
        /* Buttons */
        .stButton button {{
            background-color: {BLOOMBERG_COLORS['accent_orange']};
            color: white;
            border: none;
            border-radius: 2px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            transition: all 0.3s;
        }}
        
        .stButton button:hover {{
            background-color: #FF8C5C;
            box-shadow: 0 4px 12px rgba(255, 107, 53, 0.4);
        }}
        
        /* Dataframes */
        .dataframe {{
            background-color: {BLOOMBERG_COLORS['bg_medium']};
            color: {BLOOMBERG_COLORS['text_primary']};
            border: 1px solid {BLOOMBERG_COLORS['border']};
        }}
        
        .dataframe th {{
            background-color: {BLOOMBERG_COLORS['bg_light']};
            color: {BLOOMBERG_COLORS['accent_blue']};
            font-weight: 700;
            text-transform: uppercase;
            font-size: 0.75rem;
            letter-spacing: 0.05em;
        }}
        
        /* Plotly charts */
        .js-plotly-plot {{
            background-color: {BLOOMBERG_COLORS['bg_medium']};
        }}
        
        /* Sentiment badges */
        .sentiment-positive {{
            background-color: {BLOOMBERG_COLORS['accent_green']};
            color: {BLOOMBERG_COLORS['bg_dark']};
            padding: 4px 12px;
            border-radius: 12px;
            font-weight: 700;
            display: inline-block;
        }}
        
        .sentiment-negative {{
            background-color: #FF4444;
            color: white;
            padding: 4px 12px;
            border-radius: 12px;
            font-weight: 700;
            display: inline-block;
        }}
        
        .sentiment-neutral {{
            background-color: {BLOOMBERG_COLORS['text_secondary']};
            color: white;
            padding: 4px 12px;
            border-radius: 12px;
            font-weight: 700;
            display: inline-block;
        }}
        
        /* Info boxes */
        .stAlert {{
            background-color: {BLOOMBERG_COLORS['bg_light']};
            border-left: 4px solid {BLOOMBERG_COLORS['accent_blue']};
            color: {BLOOMBERG_COLORS['text_primary']};
        }}
        </style>
    """, unsafe_allow_html=True)


@st.cache_data(ttl=3600)
def fetch_stock_data(ticker: str, days_back: int = 365):
    """Fetch stock data"""
    fetcher = PolygonDataFetcher()
    info = fetcher.get_stock_info(ticker)
    price = fetcher.get_current_price(ticker)
    historical = fetcher.get_historical_data(ticker, days_back=days_back)
    return info, price, historical


def create_indicator_correlation_heatmap(historical_df):
    """Create interactive indicator correlation heatmap"""
    # Add all technical indicators
    df_indicators = add_all_features(historical_df, 'close')
    
    # Select key indicators
    indicators = [
        'close', 'volume', 'ma_20', 'ma_50', 'ma_200',
        'rsi', 'macd', 'volatility_annualized',
        'bb_upper', 'bb_lower'
    ]
    
    # Calculate correlation matrix
    available_indicators = [col for col in indicators if col in df_indicators.columns]
    corr_matrix = df_indicators[available_indicators].corr()
    
    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale='RdBu',
        zmid=0,
        text=np.round(corr_matrix.values, 2),
        texttemplate='%{text}',
        textfont={"size": 10},
        colorbar=dict(title="Correlation")
    ))
    
    fig.update_layout(
        title="Indicator Correlation Matrix",
        paper_bgcolor=BLOOMBERG_COLORS['bg_medium'],
        plot_bgcolor=BLOOMBERG_COLORS['bg_medium'],
        font=dict(color=BLOOMBERG_COLORS['text_primary']),
        height=600
    )
    
    return fig


def create_indicator_network_graph(historical_df, threshold=0.5):
    """Create network graph showing strong correlations between indicators"""
    df_indicators = add_all_features(historical_df, 'close')
    
    indicators = [
        'close', 'volume', 'ma_20', 'ma_50', 'ma_200',
        'rsi', 'macd', 'volatility_annualized'
    ]
    
    available_indicators = [col for col in indicators if col in df_indicators.columns]
    corr_matrix = df_indicators[available_indicators].corr()
    
    # Create edges for correlations above threshold
    edges = []
    edge_weights = []
    
    for i in range(len(corr_matrix)):
        for j in range(i+1, len(corr_matrix)):
            corr_val = abs(corr_matrix.iloc[i, j])
            if corr_val > threshold:
                edges.append((corr_matrix.index[i], corr_matrix.columns[j]))
                edge_weights.append(corr_val)
    
    if not edges:
        return None
    
    # Create network visualization using plotly
    import networkx as nx
    
    G = nx.Graph()
    G.add_edges_from(edges)
    pos = nx.spring_layout(G, k=2, iterations=50)
    
    # Create edge traces
    edge_trace = []
    for edge, weight in zip(edges, edge_weights):
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace.append(go.Scatter(
            x=[x0, x1, None],
            y=[y0, y1, None],
            mode='lines',
            line=dict(width=weight*3, color=BLOOMBERG_COLORS['accent_blue']),
            hoverinfo='none',
            showlegend=False
        ))
    
    # Create node trace
    node_x = []
    node_y = []
    node_text = []
    
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(node)
    
    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode='markers+text',
        text=node_text,
        textposition="top center",
        marker=dict(
            size=20,
            color=BLOOMBERG_COLORS['accent_orange'],
            line=dict(width=2, color=BLOOMBERG_COLORS['text_primary'])
        ),
        textfont=dict(color=BLOOMBERG_COLORS['text_primary'], size=12),
        hoverinfo='text'
    )
    
    # Create figure
    fig = go.Figure(data=edge_trace + [node_trace])
    
    fig.update_layout(
        title=f"Indicator Relationship Network (|correlation| > {threshold})",
        showlegend=False,
        paper_bgcolor=BLOOMBERG_COLORS['bg_medium'],
        plot_bgcolor=BLOOMBERG_COLORS['bg_medium'],
        font=dict(color=BLOOMBERG_COLORS['text_primary']),
        hovermode='closest',
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        height=600
    )
    
    return fig


def generate_sample_news(ticker: str, company_name: str) -> list:
    """Generate sample news headlines for sentiment analysis demo"""
    # Sample financial news templates
    return [
        f"{company_name} reports strong quarterly earnings, beating analyst expectations significantly.",
        f"Analysts upgrade {ticker} to buy rating citing robust growth potential.",
        f"{company_name} announces innovative product launch, stock surges in pre-market trading.",
        f"Market volatility impacts {ticker} amid concerns over rising interest rates.",
        f"{company_name} CEO discusses long-term strategy and growth initiatives.",
        f"Industry challenges pose potential headwinds for {ticker} in coming quarters.",
        f"{company_name} expands market share with strategic partnerships and acquisitions.",
        f"Regulatory concerns raise questions about {ticker}'s future profitability.",
        f"{company_name} demonstrates resilience with consistent revenue growth.",
        f"Economic uncertainty leads to cautious outlook for {ticker} this quarter."
    ]


def generate_sample_earnings_call(ticker: str, company_name: str) -> str:
    """Generate sample earnings call transcript for sentiment analysis demo"""
    return f"""
    Good afternoon and welcome to {company_name}'s quarterly earnings call.
    
    We are pleased to report strong financial performance this quarter. Revenue increased 
    significantly, exceeding our initial guidance and analyst expectations. Our innovative 
    product lineup continues to gain market traction, driving robust demand.
    
    Operating margins improved due to operational efficiencies and cost management initiatives.
    We successfully navigated supply chain challenges and maintained strong customer relationships.
    
    However, we remain cautious about macroeconomic headwinds including rising interest rates
    and potential regulatory changes. Competition in our sector remains intense, requiring
    continued investment in innovation and market differentiation.
    
    Looking ahead, we are optimistic about growth opportunities in emerging markets and new
    product categories. Our strategic investments in technology and talent position us well
    for sustainable long-term growth despite near-term uncertainties.
    
    We maintain our commitment to shareholder value through disciplined capital allocation
    and operational excellence.
    """


@st.cache_data(ttl=3600)
def analyze_sentiment_cached(ticker: str, company_name: str):
    """Cached sentiment analysis for ticker"""
    analyzer = get_analyzer()
    
    # Generate sample data
    news_items = generate_sample_news(ticker, company_name)
    earnings_text = generate_sample_earnings_call(ticker, company_name)
    
    # Analyze news
    news_results = analyzer.analyze_multiple_texts(news_items, threshold=0.5)
    news_aggregate = analyzer.get_aggregate_sentiment(news_items, threshold=0.5)
    
    # Analyze earnings call (split into chunks)
    sentences = [s.strip() + '.' for s in earnings_text.split('.') if s.strip()]
    earnings_aggregate = analyzer.get_aggregate_sentiment(sentences, threshold=0.5)
    
    return news_results, news_aggregate, earnings_aggregate, sentences


def show_sentiment_tab(ticker: str, company_name: str):
    """Display sentiment analysis tabs with real FinBERT analysis"""
    st.markdown("### 📊 Sentiment Analysis Dashboard")
    st.caption("🤖 Powered by FinBERT - AI sentiment analysis for financial text")
    
    # Load model status
    with st.spinner("Loading FinBERT model..."):
        try:
            news_results, news_aggregate, earnings_aggregate, earnings_sentences = \
                analyze_sentiment_cached(ticker, company_name)
            model_loaded = True
        except Exception as e:
            st.error(f"Error loading sentiment model: {e}")
            model_loaded = False
            return
    
    if model_loaded:
        st.success("✅ FinBERT Model Loaded - Analyzing real-time sentiment!")
    
    sentiment_tabs = st.tabs([
        "📞 Earnings Call Sentiment",
        "📰 News Sentiment",
        "📈 Sentiment Trends"
    ])
    
    # Earnings Call Sentiment Tab
    with sentiment_tabs[0]:
        st.markdown("#### Recent Earnings Call Sentiment")
        st.caption(f"Analyzing sample earnings call for {company_name}")
        
        # Overall metrics
        col1, col2, col3 = st.columns(3)
        
        overall_sentiment = earnings_aggregate['overall_sentiment']
        confidence = earnings_aggregate['confidence']
        
        with col1:
            st.metric("Overall Sentiment", overall_sentiment.upper(), 
                     f"{confidence*100:.1f}% confidence")
            if overall_sentiment == 'positive':
                st.markdown('<div class="sentiment-positive">BULLISH</div>', unsafe_allow_html=True)
            elif overall_sentiment == 'negative':
                st.markdown('<div class="sentiment-negative">BEARISH</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="sentiment-neutral">NEUTRAL</div>', unsafe_allow_html=True)
        
        with col2:
            st.metric("Positive Statements", f"{earnings_aggregate['positive_percentage']:.1f}%")
        with col3:
            st.metric("Negative Statements", f"{earnings_aggregate['negative_percentage']:.1f}%")
        
        # Sentiment breakdown
        st.markdown("##### Sentiment Distribution:")
        sentiment_df = pd.DataFrame({
            'Category': ['Positive', 'Neutral', 'Negative'],
            'Count': [
                earnings_aggregate['positive_count'],
                earnings_aggregate['neutral_count'],
                earnings_aggregate['negative_count']
            ],
            'Percentage': [
                f"{earnings_aggregate['positive_percentage']:.1f}%",
                f"{earnings_aggregate['neutral_percentage']:.1f}%",
                f"{earnings_aggregate['negative_percentage']:.1f}%"
            ]
        })
        st.dataframe(sentiment_df, use_container_width=True, hide_index=True)
        
        # Detailed results
        with st.expander("📋 View Detailed Analysis"):
            for result in earnings_aggregate['detailed_results'][:10]:  # Show first 10
                sentiment_emoji = {
                    'positive': '🟢',
                    'negative': '🔴',
                    'neutral': '⚪'
                }
                st.markdown(f"{sentiment_emoji[result['sentiment']]} **{result['sentiment'].upper()}** "
                           f"({result['confidence']*100:.1f}% confidence)")
                st.caption(f"*\"{result['text']}\"*")
                st.markdown("---")
    
    # News Sentiment Tab
    with sentiment_tabs[1]:
        st.markdown("#### News Sentiment Analysis")
        st.caption(f"Analyzing sample financial news for {company_name}")
        
        # Aggregate metrics
        col1, col2, col3, col4 = st.columns(4)
        
        overall_news_sentiment = news_aggregate['overall_sentiment']
        
        with col1:
            st.metric("Overall Sentiment", overall_news_sentiment.upper())
        with col2:
            st.metric("News Analyzed", news_aggregate['total_analyzed'])
        with col3:
            st.metric("Positive %", f"{news_aggregate['positive_percentage']:.1f}%")
        with col4:
            st.metric("Confidence", f"{news_aggregate['confidence']*100:.1f}%")
        
        # News items with sentiment
        st.markdown("##### Recent News Analysis:")
        news_display = []
        
        for i, result in enumerate(news_results):
            sentiment_icon = {
                'positive': '🟢 Positive',
                'negative': '🔴 Negative',
                'neutral': '⚪ Neutral'
            }
            
            # Generate realistic time
            hours_ago = i * 3 + 2
            if hours_ago < 24:
                time_str = f"{hours_ago}h ago"
            else:
                time_str = f"{hours_ago // 24}d ago"
            
            news_display.append({
                'Time': time_str,
                'Headline': result['text'],
                'Sentiment': sentiment_icon[result['sentiment']],
                'Confidence': f"{result['confidence']*100:.1f}%",
                'Score': result['confidence']
            })
        
        news_df = pd.DataFrame(news_display)
        st.dataframe(news_df, use_container_width=True, hide_index=True)
        
        # Sentiment distribution chart
        st.markdown("##### Sentiment Distribution:")
        fig = go.Figure(data=[go.Pie(
            labels=['Positive', 'Neutral', 'Negative'],
            values=[
                news_aggregate['positive_count'],
                news_aggregate['neutral_count'],
                news_aggregate['negative_count']
            ],
            marker=dict(colors=[BLOOMBERG_COLORS['accent_green'], 
                               BLOOMBERG_COLORS['text_secondary'],
                               '#FF4444']),
            hole=0.4
        )])
        
        fig.update_layout(
            paper_bgcolor=BLOOMBERG_COLORS['bg_medium'],
            plot_bgcolor=BLOOMBERG_COLORS['bg_medium'],
            font=dict(color=BLOOMBERG_COLORS['text_primary']),
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Sentiment Trends Tab
    with sentiment_tabs[2]:
        st.markdown("#### Sentiment Trend Analysis")
        st.caption("Simulated 30-day sentiment trend based on analysis patterns")
        
        # Generate trend based on current sentiment
        dates = pd.date_range(end=pd.Timestamp.now(), periods=30, freq='D')
        
        # Base trend on overall sentiment
        base_score = 0.5
        if overall_news_sentiment == 'positive':
            base_score = 0.7
        elif overall_news_sentiment == 'negative':
            base_score = 0.3
        
        # Generate realistic trend
        sentiment_scores = np.cumsum(np.random.randn(30) * 0.03) + base_score
        sentiment_scores = np.clip(sentiment_scores, 0.2, 0.9)
        
        # Smooth the trend
        window = 3
        sentiment_scores = pd.Series(sentiment_scores).rolling(window=window, center=True).mean().fillna(method='bfill').fillna(method='ffill').values
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dates,
            y=sentiment_scores,
            mode='lines+markers',
            name='Sentiment Score',
            line=dict(color=BLOOMBERG_COLORS['accent_blue'], width=3),
            fill='tozeroy',
            fillcolor=f'rgba(0, 212, 255, 0.1)',
            marker=dict(size=6)
        ))
        
        # Add reference lines
        fig.add_hline(y=0.6, line_dash="dash", line_color=BLOOMBERG_COLORS['accent_green'], 
                     annotation_text="Positive Threshold")
        fig.add_hline(y=0.4, line_dash="dash", line_color="red", 
                     annotation_text="Negative Threshold")
        
        fig.update_layout(
            title="30-Day Sentiment Trend (Simulated)",
            xaxis_title="Date",
            yaxis_title="Sentiment Score",
            paper_bgcolor=BLOOMBERG_COLORS['bg_medium'],
            plot_bgcolor=BLOOMBERG_COLORS['bg_medium'],
            font=dict(color=BLOOMBERG_COLORS['text_primary']),
            height=400,
            yaxis=dict(range=[0, 1])
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Trend statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Current Score", f"{sentiment_scores[-1]:.2f}")
        with col2:
            st.metric("30-Day Average", f"{np.mean(sentiment_scores):.2f}")
        with col3:
            trend = sentiment_scores[-1] - sentiment_scores[0]
            st.metric("Trend", f"{trend:+.2f}", f"{'Improving' if trend > 0 else 'Declining'}")


def show():
    """Main Bloomberg-style dashboard"""
    apply_bloomberg_style()
    
    # Header with Bloomberg-style branding
    st.markdown(f"""
        <div style='background: linear-gradient(90deg, {BLOOMBERG_COLORS['accent_orange']} 0%, {BLOOMBERG_COLORS['accent_blue']} 100%); 
                    padding: 20px; margin-bottom: 30px; border-radius: 4px;'>
            <h1 style='margin: 0; color: white;'>⚡ BLOOMBERG-STYLE TERMINAL</h1>
            <p style='margin: 5px 0 0 0; color: rgba(255,255,255,0.9); font-size: 0.9rem;'>
                Professional Financial Analysis Platform
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Stock input
    col1, col2, col3 = st.columns([3, 2, 1])
    with col1:
        ticker = st.text_input(
            "TICKER",
            value="AAPL",
            help="Enter stock symbol"
        ).upper()
    with col2:
        period_options = {"1M": 30, "3M": 90, "6M": 180, "1Y": 365, "2Y": 730}
        period = st.selectbox("PERIOD", list(period_options.keys()), index=3)
        days_back = period_options[period]
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        analyze = st.button("ANALYZE", use_container_width=True)
    
    if analyze or 'bloomberg_ticker' not in st.session_state:
        st.session_state.bloomberg_ticker = ticker
    
    ticker = st.session_state.bloomberg_ticker
    
    try:
        with st.spinner(f"⚡ Loading {ticker} data from Polygon.io..."):
            info, price, historical = fetch_stock_data(ticker, days_back)
        
        if info and price and historical is not None:
            # Price header
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.metric(
                    "PRICE",
                    f"${price['current_price']:.2f}",
                    f"{price['change']:+.2f} ({price['change_percent']:+.2f}%)"
                )
            with col2:
                st.metric("OPEN", f"${price['open']:.2f}")
            with col3:
                st.metric("HIGH", f"${price['day_high']:.2f}")
            with col4:
                st.metric("LOW", f"${price['day_low']:.2f}")
            with col5:
                st.metric("VOLUME", f"{price['volume']:,.0f}")
            
            st.markdown("---")
            
            # Main tabs
            tabs = st.tabs([
                "📊 OVERVIEW",
                "🎯 INDICATORS",
                "🔗 RELATIONSHIPS",
                "💬 SENTIMENT",
                "📈 TECHNICALS"
            ])
            
            # Overview Tab
            with tabs[0]:
                st.markdown(f"### {info['company_name']}")
                st.caption(f"{info['sector']} | {info['exchange']}")
                
                # Price chart
                from src.components.chart_generator import create_candlestick_chart
                fig = create_candlestick_chart(historical, title=f"{ticker} Price Chart")
                fig.update_layout(
                    paper_bgcolor=BLOOMBERG_COLORS['bg_medium'],
                    plot_bgcolor=BLOOMBERG_COLORS['bg_dark'],
                    font=dict(color=BLOOMBERG_COLORS['text_primary'])
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Indicators Tab
            with tabs[1]:
                metrics = calculate_performance_metrics(historical, 'close')
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("RETURN (TOTAL)", f"{metrics.get('total_return', 0):.2f}%")
                    st.metric("RETURN (YTD)", f"{metrics.get('ytd_return', 0):.2f}%")
                with col2:
                    st.metric("VOLATILITY", f"{metrics.get('annualized_volatility', 0):.2f}%")
                    st.metric("SHARPE RATIO", f"{metrics.get('sharpe_ratio', 0):.2f}")
                with col3:
                    st.metric("MAX DRAWDOWN", f"{metrics.get('max_drawdown_pct', 0):.2f}%")
                    st.metric("52W HIGH", f"${metrics.get('high_52week', 0):.2f}")
                with col4:
                    st.metric("52W LOW", f"${metrics.get('low_52week', 0):.2f}")
                    st.metric("CURRENT", f"${metrics.get('current_price', 0):.2f}")
            
            # Relationships Tab
            with tabs[2]:
                st.markdown("### Indicator Correlation Analysis")
                st.caption("Understanding how different technical indicators relate to each other")
                
                viz_type = st.radio("Visualization Type:", ["Heatmap", "Network Graph"], horizontal=True)
                
                if viz_type == "Heatmap":
                    fig = create_indicator_correlation_heatmap(historical)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    threshold = st.slider("Correlation Threshold", 0.0, 1.0, 0.5, 0.05)
                    fig = create_indicator_network_graph(historical, threshold)
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.warning(f"No strong correlations found above {threshold}")
            
            # Sentiment Tab
            with tabs[3]:
                show_sentiment_tab(ticker, info.get('company_name', ticker))
            
            # Technicals Tab
            with tabs[4]:
                st.markdown("### Technical Analysis")
                df_tech = add_all_features(historical, 'close')
                
                # RSI
                st.markdown("#### RSI (Relative Strength Index)")
                current_rsi = df_tech['rsi'].iloc[-1]
                
                fig_rsi = go.Figure()
                fig_rsi.add_trace(go.Scatter(
                    x=df_tech['date'],
                    y=df_tech['rsi'],
                    mode='lines',
                    name='RSI',
                    line=dict(color=BLOOMBERG_COLORS['accent_blue'], width=2)
                ))
                fig_rsi.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Overbought")
                fig_rsi.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="Oversold")
                
                fig_rsi.update_layout(
                    paper_bgcolor=BLOOMBERG_COLORS['bg_medium'],
                    plot_bgcolor=BLOOMBERG_COLORS['bg_dark'],
                    font=dict(color=BLOOMBERG_COLORS['text_primary']),
                    height=300
                )
                st.plotly_chart(fig_rsi, use_container_width=True)
                
                if current_rsi > 70:
                    st.markdown(f'<div class="sentiment-negative">OVERBOUGHT: RSI = {current_rsi:.1f}</div>', unsafe_allow_html=True)
                elif current_rsi < 30:
                    st.markdown(f'<div class="sentiment-positive">OVERSOLD: RSI = {current_rsi:.1f}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="sentiment-neutral">NEUTRAL: RSI = {current_rsi:.1f}</div>', unsafe_allow_html=True)
        
        else:
            st.error(f"⚠️ Could not load data for {ticker}")
    
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")


if __name__ == "__main__":
    show()
