"""
People Profiles Engine for ChatLens AI.
Generates engagement scores, communication styles, emoji usage, and per-person analytics.
"""
from typing import List, Dict
from collections import defaultdict, Counter
import re

try:
    import emoji
    HAS_EMOJI = True
except ImportError:
    HAS_EMOJI = False

from models.schemas import ParsedMessage


def _extract_emojis(text: str) -> List[str]:
    """Extract emojis from text using the emoji library."""
    if HAS_EMOJI:
        return [c for c in text if emoji.is_emoji(c)]
    # Fallback: basic Unicode emoji range detection
    return re.findall(r'[\U0001f600-\U0001f650\U0001f680-\U0001f6ff\U0001f900-\U0001f9ff\u2600-\u26ff\u2700-\u27bf]', text)


def _detect_communication_style(profile: dict) -> str:
    """Classify communication style based on message patterns."""
    avg_len = profile.get("avg_msg_length", 0)
    emoji_ratio = profile.get("emoji_count", 0) / max(profile.get("messages_count", 1), 1)
    peak_hour = profile.get("peak_hour", 12)
    
    if emoji_ratio > 0.5:
        return "Emoji Enthusiast 😄"
    elif avg_len > 150:
        return "Detailed Reporter 📝"
    elif avg_len < 30:
        return "Concise Communicator ⚡"
    elif peak_hour >= 22 or peak_hour <= 4:
        return "Night Owl 🦉"
    elif peak_hour >= 5 and peak_hour <= 8:
        return "Early Bird 🐦"
    elif profile.get("media_count", 0) > profile.get("messages_count", 1) * 0.3:
        return "Visual Sharer 📷"
    else:
        return "Balanced Communicator 💬"


def calculate_people_profiles(messages: List[ParsedMessage]) -> dict:
    """Generate comprehensive participant profiles."""
    msg_counts = Counter()
    word_counts = defaultdict(int)
    char_counts = defaultdict(int)
    emoji_counts = defaultdict(list)
    hour_counts = defaultdict(lambda: Counter())
    media_counts = Counter()
    starters = Counter()
    
    # Sentiment per person (basic positive/negative count)
    sentiment_counts = defaultdict(lambda: {"positive": 0, "neutral": 0, "negative": 0})
    
    try:
        from nltk.sentiment import SentimentIntensityAnalyzer
        sia = SentimentIntensityAnalyzer()
    except Exception:
        sia = None
    
    prev_time = None
    
    for msg in messages:
        if msg.is_system or not msg.sender:
            continue
        
        sender = msg.sender
        msg_counts[sender] += 1
        word_counts[sender] += len(msg.content.split())
        char_counts[sender] += len(msg.content)
        hour_counts[sender][msg.timestamp.hour] += 1
        
        # Emojis
        emojis = _extract_emojis(msg.content)
        emoji_counts[sender].extend(emojis)
        
        # Media
        if msg.message_type == "media":
            media_counts[sender] += 1
        
        # Conversation starters (4+ hour gap)
        if prev_time and (msg.timestamp - prev_time).total_seconds() > 4 * 3600:
            starters[sender] += 1
        prev_time = msg.timestamp
        
        # Sentiment
        if sia:
            compound = sia.polarity_scores(msg.content)['compound']
            if compound >= 0.05:
                sentiment_counts[sender]["positive"] += 1
            elif compound <= -0.05:
                sentiment_counts[sender]["negative"] += 1
            else:
                sentiment_counts[sender]["neutral"] += 1
    
    total_msgs = sum(msg_counts.values()) or 1
    max_msgs = max(msg_counts.values()) if msg_counts else 1
    
    profiles = []
    for sender in msg_counts:
        count = msg_counts[sender]
        avg_len = char_counts[sender] / count if count > 0 else 0
        peak_hour = hour_counts[sender].most_common(1)[0][0] if hour_counts[sender] else 12
        top_emojis_list = Counter(emoji_counts[sender]).most_common(5)
        
        # Engagement score: weighted combo of volume, conversation starts, and consistency
        volume_score = min((count / max_msgs) * 60, 60)
        starter_score = min(starters.get(sender, 0) * 5, 25)
        consistency_score = min(len(hour_counts[sender]) * 2, 15)
        engagement = round(min(volume_score + starter_score + consistency_score, 100))
        
        profile = {
            "name": sender,
            "messages_count": count,
            "word_count": word_counts[sender],
            "avg_msg_length": round(avg_len, 1),
            "engagement_score": engagement,
            "sentiment": sentiment_counts[sender],
            "top_emojis": [{"emoji": e, "count": c} for e, c in top_emojis_list],
            "emoji_count": len(emoji_counts[sender]),
            "media_count": media_counts.get(sender, 0),
            "peak_hour": peak_hour,
            "conversations_started": starters.get(sender, 0),
            "communication_style": ""
        }
        profile["communication_style"] = _detect_communication_style(profile)
        profiles.append(profile)
    
    # Sort by engagement score
    profiles.sort(key=lambda p: p["engagement_score"], reverse=True)
    
    return {"profiles": profiles}
