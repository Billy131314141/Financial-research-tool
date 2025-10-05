"""
FinBERT Sentiment Analysis Module
Uses ProsusAI/finbert for financial text sentiment analysis
"""
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import logging
from typing import List, Dict, Optional
import streamlit as st

logger = logging.getLogger(__name__)


class FinBERTAnalyzer:
    """Financial sentiment analyzer using FinBERT model"""
    
    def __init__(self):
        self.tokenizer = None
        self.model = None
        self.labels = ["positive", "negative", "neutral"]
        
    @st.cache_resource
    def _load_model(_self):
        """Load FinBERT model and tokenizer (cached)"""
        try:
            logger.info("Loading FinBERT model...")
            tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
            model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")
            logger.info("FinBERT model loaded successfully!")
            return tokenizer, model
        except Exception as e:
            logger.error(f"Error loading FinBERT model: {e}")
            return None, None
    
    def ensure_model_loaded(self):
        """Ensure model is loaded before use"""
        if self.tokenizer is None or self.model is None:
            self.tokenizer, self.model = self._load_model()
        return self.tokenizer is not None and self.model is not None
    
    def analyze_financial_sentiment(
        self, 
        text: str, 
        threshold: float = 0.5
    ) -> List[Dict]:
        """
        Analyze sentiment with optional confidence threshold.
        
        Args:
            text: Input text to analyze
            threshold: Minimum confidence threshold (0.0 to 1.0)
            
        Returns:
            List of dicts with label and confidence
        """
        if not self.ensure_model_loaded():
            return []
        
        try:
            # Tokenize input
            inputs = self.tokenizer(
                text, 
                return_tensors="pt", 
                truncation=True, 
                padding=True, 
                max_length=512
            )
            
            # Inference
            with torch.no_grad():
                outputs = self.model(**inputs)
                predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
            
            # Get scores
            scores = predictions[0].tolist()
            
            # Get top label
            top_idx = scores.index(max(scores))
            if scores[top_idx] < threshold:
                return []  # Discard low-confidence predictions
            
            return [{
                "label": self.labels[top_idx],
                "confidence": scores[top_idx],
                "all_scores": {
                    self.labels[i]: scores[i] for i in range(len(self.labels))
                }
            }]
            
        except Exception as e:
            logger.error(f"Error in sentiment analysis: {e}")
            return []
    
    def analyze_multiple_texts(
        self, 
        texts: List[str], 
        threshold: float = 0.5
    ) -> List[Dict]:
        """
        Analyze multiple texts and return results.
        
        Args:
            texts: List of texts to analyze
            threshold: Minimum confidence threshold
            
        Returns:
            List of sentiment results
        """
        results = []
        for text in texts:
            sentiment = self.analyze_financial_sentiment(text, threshold)
            if sentiment:
                results.append({
                    'text': text[:100] + '...' if len(text) > 100 else text,
                    'sentiment': sentiment[0]['label'],
                    'confidence': sentiment[0]['confidence'],
                    'all_scores': sentiment[0]['all_scores']
                })
        return results
    
    def get_aggregate_sentiment(
        self, 
        texts: List[str], 
        threshold: float = 0.5
    ) -> Dict:
        """
        Get aggregate sentiment from multiple texts.
        
        Args:
            texts: List of texts to analyze
            threshold: Minimum confidence threshold
            
        Returns:
            Dict with aggregate sentiment statistics
        """
        results = self.analyze_multiple_texts(texts, threshold)
        
        if not results:
            return {
                'overall_sentiment': 'neutral',
                'confidence': 0.0,
                'positive_count': 0,
                'negative_count': 0,
                'neutral_count': 0,
                'total_analyzed': 0,
                'positive_percentage': 0.0,
                'negative_percentage': 0.0,
                'neutral_percentage': 0.0,
                'detailed_results': []  # ← FIXED: Added this line!
            }
        
        # Count sentiments
        positive_count = sum(1 for r in results if r['sentiment'] == 'positive')
        negative_count = sum(1 for r in results if r['sentiment'] == 'negative')
        neutral_count = sum(1 for r in results if r['sentiment'] == 'neutral')
        total = len(results)
        
        # Calculate percentages
        positive_pct = (positive_count / total) * 100
        negative_pct = (negative_count / total) * 100
        neutral_pct = (neutral_count / total) * 100
        
        # Determine overall sentiment
        if positive_count > negative_count and positive_count > neutral_count:
            overall = 'positive'
        elif negative_count > positive_count and negative_count > neutral_count:
            overall = 'negative'
        else:
            overall = 'neutral'
        
        # Average confidence
        avg_confidence = sum(r['confidence'] for r in results) / total
        
        return {
            'overall_sentiment': overall,
            'confidence': avg_confidence,
            'positive_count': positive_count,
            'negative_count': negative_count,
            'neutral_count': neutral_count,
            'total_analyzed': total,
            'positive_percentage': positive_pct,
            'negative_percentage': negative_pct,
            'neutral_percentage': neutral_pct,
            'detailed_results': results
        }


# Global instance
_analyzer = None

def get_analyzer() -> FinBERTAnalyzer:
    """Get or create global analyzer instance"""
    global _analyzer
    if _analyzer is None:
        _analyzer = FinBERTAnalyzer()
    return _analyzer


# Convenience functions
def analyze_text(text: str, threshold: float = 0.5) -> List[Dict]:
    """Analyze single text for sentiment"""
    analyzer = get_analyzer()
    return analyzer.analyze_financial_sentiment(text, threshold)


def analyze_news_batch(news_items: List[str], threshold: float = 0.5) -> Dict:
    """Analyze batch of news items and return aggregate"""
    analyzer = get_analyzer()
    return analyzer.get_aggregate_sentiment(news_items, threshold)


def analyze_earnings_call(transcript: str, threshold: float = 0.5) -> Dict:
    """
    Analyze earnings call transcript.
    For long transcripts, splits into chunks.
    """
    analyzer = get_analyzer()
    
    # Split transcript into sentences/chunks (max 512 tokens per chunk)
    # Simple split by periods for now
    sentences = [s.strip() for s in transcript.split('.') if s.strip()]
    
    # Analyze chunks
    chunk_size = 5  # Analyze 5 sentences at a time
    chunks = []
    for i in range(0, len(sentences), chunk_size):
        chunk = '. '.join(sentences[i:i+chunk_size]) + '.'
        if chunk.strip():
            chunks.append(chunk)
    
    # Get aggregate sentiment
    return analyzer.get_aggregate_sentiment(chunks, threshold)


if __name__ == "__main__":
    # Test the analyzer
    import json
    
    print("Testing FinBERT Sentiment Analyzer...")
    print("-" * 50)
    
    # Test cases
    test_texts = [
        "Rising interest rates pose risks to our portfolio.",
        "The company reported record quarterly earnings exceeding expectations.",
        "Market conditions remain stable with moderate growth.",
        "Significant losses due to regulatory challenges.",
        "Strong revenue growth and positive outlook for next quarter."
    ]
    
    analyzer = get_analyzer()
    
    print("\nIndividual Analysis:")
    for text in test_texts:
        result = analyzer.analyze_financial_sentiment(text)
        print(f"\nText: {text}")
        print(f"Result: {json.dumps(result, indent=2)}")
    
    print("\n" + "=" * 50)
    print("Aggregate Analysis:")
    aggregate = analyzer.get_aggregate_sentiment(test_texts)
    print(json.dumps(aggregate, indent=2))


