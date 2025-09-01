import requests
import os
from flask import current_app

def analyze_sentiment(text):
    """
    Analyze sentiment of text using Hugging Face API
    """
    api_key = current_app.config.get('HUGGINGFACE_API_KEY')
    
    if not api_key:
        # Fallback to simple sentiment analysis if API key is not available
        return simple_sentiment_analysis(text)
    
    try:
        API_URL = "https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment-latest"
        headers = {"Authorization": f"Bearer {api_key}"}
        
        payload = {"inputs": text}
        response = requests.post(API_URL, headers=headers, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                sentiment_scores = result[0]
                
                # Map sentiment labels to moods
                mood_mapping = {
                    'positive': 'happy',
                    'neutral': 'calm',
                    'negative': 'sad'
                }
                
                # Find the highest scoring sentiment
                best_sentiment = max(sentiment_scores, key=lambda x: x['score'])
                mood = mood_mapping.get(best_sentiment['label'].lower(), 'neutral')
                
                return {
                    'mood': mood,
                    'score': best_sentiment['score'],
                    'raw_result': result
                }
    
    except Exception as e:
        current_app.logger.error(f"Sentiment analysis error: {e}")
    
    # Fallback if API call fails
    return simple_sentiment_analysis(text)

def simple_sentiment_analysis(text):
    """
    Simple fallback sentiment analysis
    """
    positive_words = ['happy', 'joy', 'love', 'great', 'wonderful', 'amazing', 'good']
    negative_words = ['sad', 'angry', 'hate', 'bad', 'terrible', 'awful', 'stress']
    
    text_lower = text.lower()
    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)
    
    if positive_count > negative_count:
        return {'mood': 'happy', 'score': 0.7}
    elif negative_count > positive_count:
        return {'mood': 'sad', 'score': 0.3}
    else:
        return {'mood': 'calm', 'score': 0.5}