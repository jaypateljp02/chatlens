from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class ParsedMessage(BaseModel):
    timestamp: datetime
    sender: Optional[str]
    content: str
    message_type: str
    is_system: bool

class ChatMetadata(BaseModel):
    filename: str
    total_messages: int
    participants: List[str]
    date_range: Dict[str, Optional[datetime]]
    group_name: Optional[str]

class UploadResponse(BaseModel):
    chat_id: str
    metadata: ChatMetadata
    preview_messages: List[ParsedMessage]

# --- Communication Analytics ---
class CommunicationStats(BaseModel):
    messages_per_participant: Dict[str, int]
    messages_per_hour: Dict[int, int]
    messages_per_day_of_week: Dict[str, int]
    peak_hours: List[int]
    most_active_participant: Optional[str]
    word_frequencies: Dict[str, Dict[str, int]]
    media_counts: Dict[str, int]
    conversation_starters: Dict[str, int]
    avg_message_length: Dict[str, float]

# --- AI Summaries ---
class SummaryRequest(BaseModel):
    mode: str  # "bullet", "story", "timeline", "pending"

class SummaryResponse(BaseModel):
    summary_text: str
    key_takeaways: List[str]
    action_items: List[str]

class AskQuestionRequest(BaseModel):
    question: str

class AskQuestionResponse(BaseModel):
    answer: str
    source_messages: List[str]
    confidence: float

class TopicItem(BaseModel):
    name: str
    count: int
    description: str
    category: str

class TopicResponse(BaseModel):
    topics: List[TopicItem]

# --- Sentiment Analytics ---
class SentimentStats(BaseModel):
    overall_sentiment: Dict[str, int]
    mood_trends: List[Dict[str, Any]]
    stress_per_person: Dict[str, int]
    gratitude_per_person: Dict[str, int]
    conflict_periods: List[Dict[str, Any]]

# --- People Profiles ---
class PersonProfile(BaseModel):
    name: str
    messages_count: int
    word_count: int
    avg_msg_length: float
    engagement_score: int
    sentiment: Dict[str, int]
    top_emojis: List[Dict[str, Any]]
    emoji_count: int
    media_count: int
    peak_hour: int
    conversations_started: int
    communication_style: str

class PeopleProfilesResponse(BaseModel):
    profiles: List[PersonProfile]

# --- Action Items ---
class ActionItem(BaseModel):
    promise: str
    assignee: str
    detected_date: str
    status: str
    completed_by: Optional[str]
    completed_at: Optional[str]
    context: List[str]

class ActionItemsResponse(BaseModel):
    action_items: List[ActionItem]
    total: int
    pending_count: int
    completed_count: int

# --- Timeline ---
class TimelineEvent(BaseModel):
    date: str
    type: str
    title: str
    description: str
    icon: str

class TimelineResponse(BaseModel):
    events: List[TimelineEvent]

# --- Period Comparison ---
class ComparisonRequest(BaseModel):
    period1_start: str
    period1_end: str
    period2_start: str
    period2_end: str

class ComparisonResponse(BaseModel):
    period1: Dict[str, Any]
    period2: Dict[str, Any]
    changes: Dict[str, Any]
