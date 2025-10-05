"""
Basic sentiment analysis for financial news.
"""
from textblob import TextBlob
from typing import List, Dict
import pandas as pd


def analyze_sentiment(text: str) -> Dict:
    """
    Analyze sentiment of a text using TextBlob.
    
    Args:
        text: Text to analyze
        
    Returns:
        Dictionary with sentiment scores
    """
    if not text:
        return {
            'polarity': 0.0,
            'subjectivity': 0.0,
            'sentiment': 'neutral'
        }
    
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity  # -1 to 1
    subjectivity = blob.sentiment.subjectivity  # 0 to 1
    
    # Classify sentiment
    if polarity > 0.1:
        sentiment = 'positive'
    elif polarity < -0.1:
        sentiment = 'negative'
    else:
        sentiment = 'neutral'
    
    return {
        'polarity': polarity,
        'subjectivity': subjectivity,
        'sentiment': sentiment
    }


def analyze_news_batch(news_list: List[Dict]) -> pd.DataFrame:
    """
    Analyze sentiment for a batch of news articles.
    
    Args:
        news_list: List of dictionaries with 'title' and optional 'description'
        
    Returns:
        DataFrame with news and sentiment scores
    """
    results = []
    
    for news in news_list:
        title = news.get('title', '')
        description = news.get('description', '')
        
        # Combine title and description
        text = f"{title}. {description}"
        
        sentiment = analyze_sentiment(text)
        
        results.append({
            'title': title,
            'description': description,
            'polarity': sentiment['polarity'],
            'subjectivity': sentiment['subjectivity'],
            'sentiment': sentiment['sentiment'],
            'source': news.get('source', ''),
            'url': news.get('url', ''),
            'publish_date': news.get('publishedAt', '')
        })
    
    return pd.DataFrame(results)


def calculate_aggregate_sentiment(df: pd.DataFrame) -> Dict:
    """
    Calculate aggregate sentiment from multiple news articles.
    
    Args:
        df: DataFrame with sentiment data
        
    Returns:
        Dictionary with aggregate metrics
    """
    if df.empty or 'polarity' not in df.columns:
        return {
            'avg_polarity': 0.0,
            'sentiment_score': 0.0,
            'positive_count': 0,
            'negative_count': 0,
            'neutral_count': 0,
            'overall_sentiment': 'neutral'
        }
    
    avg_polarity = df['polarity'].mean()
    
    # Count sentiment categories
    sentiment_counts = df['sentiment'].value_counts().to_dict()
    
    # Determine overall sentiment
    if avg_polarity > 0.1:
        overall = 'positive'
    elif avg_polarity < -0.1:
        overall = 'negative'
    else:
        overall = 'neutral'
    
    return {
        'avg_polarity': avg_polarity,
        'sentiment_score': avg_polarity * 100,  # Scale to -100 to 100
        'positive_count': sentiment_counts.get('positive', 0),
        'negative_count': sentiment_counts.get('negative', 0),
        'neutral_count': sentiment_counts.get('neutral', 0),
        'overall_sentiment': overall
    }


def get_sentiment_indicator(polarity: float) -> str:
    """
    Get a simple sentiment indicator emoji/text.
    
    Args:
        polarity: Sentiment polarity score
        
    Returns:
        Sentiment indicator string
    """
    if polarity > 0.3:
        return "🟢 Very Positive"
    elif polarity > 0.1:
        return "🟢 Positive"
    elif polarity < -0.3:
        return "🔴 Very Negative"
    elif polarity < -0.1:
        return "🔴 Negative"
    else:
        return "⚪ Neutral"


