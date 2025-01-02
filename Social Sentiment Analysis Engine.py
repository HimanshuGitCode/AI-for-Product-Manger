from typing import Dict, List
import pandas as pd
from textblob import TextBlob

class SentimentAnalyzer:
    def __init__(self, competitors: List[str]):
        self.competitors = competitors
        self.sentiment_data = {}
    
    def analyze_social_mentions(self, platform_data: Dict):
        """
        Analyze social media mentions and sentiment
        platform_data: Dict with competitor mentions from various platforms
        """
        for competitor in self.competitors:
            mentions = platform_data.get(competitor, [])
            
            if not mentions:
                continue
            
            sentiment_scores = []
            topics = []
            
            for mention in mentions:
                # Calculate sentiment
                sentiment = TextBlob(mention['text'])
                sentiment_scores.append(sentiment.sentiment.polarity)
                
                # Analyze with GPT for topic extraction
                topics.extend(self._extract_topics(mention['text']))
            
            self.sentiment_data[competitor] = {
                'average_sentiment': sum(sentiment_scores) / len(sentiment_scores),
                'mention_count': len(mentions),
                'trending_topics': self._get_trending_topics(topics),
                'timestamp': datetime.now().isoformat()
            }
    
    def _extract_topics(self, text: str) -> List[str]:
        """Extract key topics from text using GPT"""
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Extract key topics from this text."},
                {"role": "user", "content": text}
            ]
        )
        return response.choices[0].message.content.split(',')
    
    def _get_trending_topics(self, topics: List[str]) -> Dict[str, int]:
        """Identify trending topics from all mentions"""
        from collections import Counter
        return dict(Counter(topics).most_common(5))
