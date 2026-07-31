"""
Timeline & Period Comparison Engine for ChatLens AI.
Extracts key milestones and compares analytics between two time periods.
"""
from typing import List, Dict, Optional
from collections import Counter, defaultdict
from datetime import datetime

from models.schemas import ParsedMessage

try:
    from nltk.sentiment import SentimentIntensityAnalyzer
    sia = SentimentIntensityAnalyzer()
except Exception:
    sia = None


def extract_timeline(messages: List[ParsedMessage]) -> dict:
    """Extract key milestone events from chat history."""
    events = []
    daily_stats = defaultdict(lambda: {"count": 0, "media": 0, "participants": set()})
    
    for msg in messages:
        if msg.is_system:
            # System messages are often milestones (group created, person added, etc.)
            events.append({
                "date": msg.timestamp.isoformat(),
                "type": "system",
                "title": "Group Event",
                "description": msg.content[:150],
                "icon": "🔔"
            })
            continue
        
        if not msg.sender:
            continue
        
        day_key = msg.timestamp.strftime("%Y-%m-%d")
        daily_stats[day_key]["count"] += 1
        daily_stats[day_key]["participants"].add(msg.sender)
        if msg.message_type == "media":
            daily_stats[day_key]["media"] += 1
    
    # Find peak activity days (top 10% by message count)
    if daily_stats:
        counts = [v["count"] for v in daily_stats.values()]
        threshold = sorted(counts, reverse=True)[max(0, len(counts) // 10)] if counts else 0
        
        for day, stats in sorted(daily_stats.items()):
            if stats["count"] >= threshold and stats["count"] > 5:
                events.append({
                    "date": day + "T12:00:00",
                    "type": "peak_activity",
                    "title": f"Peak Activity Day — {stats['count']} messages",
                    "description": f"{len(stats['participants'])} participants active, {stats['media']} media shared",
                    "icon": "📈"
                })
            
            if stats["media"] >= 5:
                events.append({
                    "date": day + "T12:00:00",
                    "type": "media_burst",
                    "title": f"Media Sharing Burst — {stats['media']} files",
                    "description": f"Heavy media sharing day with {len(stats['participants'])} participants",
                    "icon": "📷"
                })
    
    # Add first and last message milestones
    user_msgs = [m for m in messages if not m.is_system and m.sender]
    if user_msgs:
        events.insert(0, {
            "date": user_msgs[0].timestamp.isoformat(),
            "type": "milestone",
            "title": "Chat Started",
            "description": f"First message by {user_msgs[0].sender}",
            "icon": "🟢"
        })
        events.append({
            "date": user_msgs[-1].timestamp.isoformat(),
            "type": "milestone",
            "title": "Latest Message",
            "description": f"Most recent message by {user_msgs[-1].sender}",
            "icon": "🔵"
        })
    
    # Sort by date
    events.sort(key=lambda e: e["date"])
    
    return {"events": events[:50]}  # Cap at 50 events


def compare_periods(messages: List[ParsedMessage], p1_start: str, p1_end: str, p2_start: str, p2_end: str) -> dict:
    """Compare analytics between two time periods."""
    try:
        p1_s = datetime.fromisoformat(p1_start)
        p1_e = datetime.fromisoformat(p1_end)
        p2_s = datetime.fromisoformat(p2_start)
        p2_e = datetime.fromisoformat(p2_end)
    except ValueError:
        return {"error": "Invalid date format. Use ISO format (YYYY-MM-DD)."}
    
    def get_period_stats(msgs):
        count = len(msgs)
        participants = set()
        sentiment_sum = 0
        for m in msgs:
            if not m.is_system and m.sender:
                participants.add(m.sender)
                if sia:
                    sentiment_sum += sia.polarity_scores(m.content)['compound']
        avg_sentiment = sentiment_sum / count if count > 0 else 0
        return {
            "message_count": count,
            "participant_count": len(participants),
            "participants": list(participants),
            "avg_sentiment": round(avg_sentiment, 3)
        }
    
    p1_msgs = [m for m in messages if p1_s <= m.timestamp <= p1_e]
    p2_msgs = [m for m in messages if p2_s <= m.timestamp <= p2_e]
    
    period1 = get_period_stats(p1_msgs)
    period2 = get_period_stats(p2_msgs)
    
    # Calculate changes
    vol_change = 0
    if period1["message_count"] > 0:
        vol_change = round(((period2["message_count"] - period1["message_count"]) / period1["message_count"]) * 100, 1)
    
    sent_change = round(period2["avg_sentiment"] - period1["avg_sentiment"], 3)
    
    return {
        "period1": {
            "range": f"{p1_start} to {p1_end}",
            **period1
        },
        "period2": {
            "range": f"{p2_start} to {p2_end}",
            **period2
        },
        "changes": {
            "volume_change_percent": vol_change,
            "sentiment_change": sent_change,
            "new_participants": [p for p in period2["participants"] if p not in period1["participants"]]
        }
    }
