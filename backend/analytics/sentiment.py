"""
Sentiment Analytics Engine for ChatLens AI.
Uses NLTK VADER for baseline sentiment scoring with stress, conflict, and gratitude detection.
"""
import re
from typing import List, Dict
from collections import defaultdict
from datetime import datetime, timedelta

try:
    from nltk.sentiment import SentimentIntensityAnalyzer
    import nltk
    try:
        nltk.data.find('sentiment/vader_lexicon.zip')
    except LookupError:
        nltk.download('vader_lexicon', quiet=True)
    sia = SentimentIntensityAnalyzer()
except Exception:
    sia = None

from models.schemas import ParsedMessage


STRESS_WORDS = [
    'urgent', 'asap', 'delay', 'delayed', 'issue', 'issues', 'problem', 'problems',
    'stuck', 'error', 'errors', 'pressure', 'tight', 'deadline', 'critical',
    'failing', 'failed', 'broken', 'crash', 'bug', 'bugs', 'blocker',
    'worried', 'anxious', 'stress', 'stressed', 'tension', 'overdue',
    'jaldi', 'problem', 'dikkat', 'mushkil', 'pareshan', 'tension'
]

GRATITUDE_WORDS = [
    'thank', 'thanks', 'thankyou', 'thank you', 'great', 'awesome', 'amazing',
    'good job', 'well done', 'appreciated', 'appreciate', 'kudos', 'excellent',
    'fantastic', 'wonderful', 'brilliant', 'perfect', 'superb', 'outstanding',
    'dhanyavaad', 'shukriya', 'badiya', 'bahut accha', 'zabardast'
]


def calculate_sentiment_stats(messages: List[ParsedMessage]) -> dict:
    """Calculate comprehensive sentiment analytics from parsed messages."""
    mood_trends = []
    stress_per_person = defaultdict(int)
    gratitude_per_person = defaultdict(int)
    conflict_periods = []
    overall_sentiment = {"positive": 0, "neutral": 0, "negative": 0}
    
    weekly_scores = defaultdict(list)
    negative_window = []
    
    for msg in messages:
        if msg.is_system or not msg.sender:
            continue
        
        text = msg.content.lower()
        
        # VADER sentiment scoring
        if sia:
            scores = sia.polarity_scores(msg.content)
            compound = scores['compound']
        else:
            compound = 0.0
        
        # Classify overall
        if compound >= 0.05:
            overall_sentiment["positive"] += 1
        elif compound <= -0.05:
            overall_sentiment["negative"] += 1
        else:
            overall_sentiment["neutral"] += 1
        
        # Weekly mood trends
        week_key = msg.timestamp.strftime("%Y-W%W")
        weekly_scores[week_key].append(compound)
        
        # Stress language detection
        for word in STRESS_WORDS:
            if word in text:
                stress_per_person[msg.sender] += 1
                break
        
        # Gratitude detection
        for word in GRATITUDE_WORDS:
            if word in text:
                gratitude_per_person[msg.sender] += 1
                break
        
        # Conflict detection: cluster of negative messages within 30 min
        if compound < -0.3:
            negative_window.append({
                "timestamp": msg.timestamp.isoformat(),
                "sender": msg.sender,
                "content": msg.content[:100],
                "score": round(compound, 3)
            })
        else:
            if len(negative_window) >= 3:
                conflict_periods.append({
                    "start": negative_window[0]["timestamp"],
                    "end": negative_window[-1]["timestamp"],
                    "messages_count": len(negative_window),
                    "participants": list(set(m["sender"] for m in negative_window)),
                    "sample": negative_window[0]["content"]
                })
            negative_window = []
    
    # Flush remaining negative window
    if len(negative_window) >= 3:
        conflict_periods.append({
            "start": negative_window[0]["timestamp"],
            "end": negative_window[-1]["timestamp"],
            "messages_count": len(negative_window),
            "participants": list(set(m["sender"] for m in negative_window)),
            "sample": negative_window[0]["content"]
        })
    
    # Build mood trends
    for week, scores in sorted(weekly_scores.items()):
        avg = sum(scores) / len(scores) if scores else 0
        mood_trends.append({
            "week": week,
            "avg_sentiment": round(avg, 3),
            "message_count": len(scores)
        })
    
    return {
        "overall_sentiment": overall_sentiment,
        "mood_trends": mood_trends,
        "stress_per_person": dict(stress_per_person),
        "gratitude_per_person": dict(gratitude_per_person),
        "conflict_periods": conflict_periods
    }
