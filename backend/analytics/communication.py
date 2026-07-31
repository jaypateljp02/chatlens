import re
from typing import List, Dict
from collections import Counter
from datetime import timedelta
from models.schemas import ParsedMessage, CommunicationStats

STOP_WORDS = set([
    'the', 'is', 'a', 'an', 'and', 'to', 'in', 'of', 'that', 'it', 'for', 'on', 'with', 'as', 'this', 'was', 'at', 'by', 'but', 'not', 'you', 'i', 'we', 'they', 'he', 'she', 'my', 'me', 'your', 'so', 'if', 'or', 'be', 'are', 'am', 'will', 'all', 'can', 'just', 'like', 'do', 'have',
    'hi', 'ha', 'ko', 'se', 'ki', 'ke', 'me', 'ne', 'hai', 'ho', 'bhi', 'toh', 'kya', 'aur', 'par', 'haan', 'na', 'ye', 'wo', 'jo', 'ab', 'tak', 'liye', 'kuch', 'koi', 'main', 'mera', 'tu', 'tera', 'tha', 'thi', 'the'
])

def calculate_communication_stats(messages: List[ParsedMessage]) -> CommunicationStats:
    msg_per_participant = Counter()
    msg_per_hour = Counter()
    msg_per_day_of_week = Counter()
    
    word_freq_counters: Dict[str, Counter] = {}
    media_counts = Counter()
    conversation_starters = Counter()
    total_chars_per_participant = Counter()
    
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    prev_timestamp = None
    
    for msg in messages:
        if not msg.is_system and msg.sender:
            sender = msg.sender
            msg_per_participant[sender] += 1
            total_chars_per_participant[sender] += len(msg.content)
            
            if sender not in word_freq_counters:
                word_freq_counters[sender] = Counter()
                
            # Check for media
            if msg.message_type != "text" or "<Media omitted>" in msg.content or "omitted" in msg.content.lower():
                media_counts[sender] += 1
            else:
                # Word frequency
                words = re.findall(r'\b\w+\b', msg.content.lower())
                filtered_words = [w for w in words if w not in STOP_WORDS and len(w) > 1]
                word_freq_counters[sender].update(filtered_words)
                
            # Conversation starter (4+ hour gap)
            if prev_timestamp:
                time_diff = msg.timestamp - prev_timestamp
                if time_diff >= timedelta(hours=4):
                    conversation_starters[sender] += 1
            else:
                conversation_starters[sender] += 1  # First message of the chat
                
            prev_timestamp = msg.timestamp
            
        msg_per_hour[msg.timestamp.hour] += 1
        msg_per_day_of_week[days[msg.timestamp.weekday()]] += 1
        
    peak_hours = [hour for hour, count in msg_per_hour.most_common(3)]
    most_active = msg_per_participant.most_common(1)[0][0] if msg_per_participant else None
    
    word_frequencies = {
        sender: dict(counter.most_common(15))
        for sender, counter in word_freq_counters.items()
    }
    
    avg_message_length = {}
    for sender, count in msg_per_participant.items():
        avg_message_length[sender] = total_chars_per_participant[sender] / count if count > 0 else 0.0
    
    return CommunicationStats(
        messages_per_participant=dict(msg_per_participant),
        messages_per_hour=dict(msg_per_hour),
        messages_per_day_of_week=dict(msg_per_day_of_week),
        peak_hours=peak_hours,
        most_active_participant=most_active,
        word_frequencies=word_frequencies,
        media_counts=dict(media_counts),
        conversation_starters=dict(conversation_starters),
        avg_message_length=avg_message_length
    )
