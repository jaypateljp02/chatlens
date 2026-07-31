"""
Action Items Engine for ChatLens AI.
Detects promise patterns, assignment statements, and tracks completion status.
"""
import re
from typing import List, Set
from collections import defaultdict
from models.schemas import ParsedMessage

completed_actions_store: Set[str] = set()

PROMISE_PATTERNS = [
    r'\bi\'?ll\b.*\b(send|do|handle|check|complete|finish|share|update|fix|prepare|call|arrange)\b',
    r'\bwill\b.*\b(send|do|handle|check|complete|finish|share|update|fix|prepare|call|arrange)\b',
    r'\b(assigned to|assigning|please do|please send|please check|please handle|please complete)\b',
    r'\b(by friday|by monday|by tomorrow|by today|by end of day|by eod|by tonight|by evening)\b',
    r'\b(let\'?s complete|let\'?s finish|let\'?s do|need to complete|need to finish)\b',
    r'\b(kal tak|aaj tak|bhej dena|kar dena|de dena|kar lena|bhej do|check karo)\b',
    r'\b(todo|to-do|action item|follow up|follow-up|pending)\b',
]

COMPLETION_PATTERNS = [
    r'\b(done|completed|finished|sent|shared|handled|fixed|resolved|delivered)\b',
    r'\b(ho gaya|kar diya|bhej diya|de diya|complete ho gaya|fix ho gaya)\b',
    r'\b(yes done|all done|task done|work done)\b',
]

def mark_promise_completed(promise_text: str):
    """Mark a promise as completed in persistent memory."""
    if promise_text:
        completed_actions_store.add(promise_text.strip())

def detect_action_items(messages: List[ParsedMessage]) -> dict:
    """Detect promises, assignments, and track their completion status."""
    action_items = []
    
    compiled_promises = [re.compile(p, re.IGNORECASE) for p in PROMISE_PATTERNS]
    compiled_completions = [re.compile(p, re.IGNORECASE) for p in COMPLETION_PATTERNS]
    
    for i, msg in enumerate(messages):
        if msg.is_system or not msg.sender:
            continue
        
        text = msg.content
        is_promise = False
        
        for pattern in compiled_promises:
            if pattern.search(text):
                is_promise = True
                break
        
        if not is_promise:
            continue
        
        # Check if manually marked complete or subsequent messages (next 50) confirm completion
        status = "pending"
        completed_by = None
        completed_at = None

        text_snippet = text[:200]
        if text_snippet.strip() in completed_actions_store or any(p in completed_actions_store for p in [text.strip(), text_snippet.strip()]):
            status = "completed"
            completed_by = "User Verified"
            completed_at = msg.timestamp.isoformat()
        else:
            lookahead = messages[i+1:i+51]
            for future_msg in lookahead:
                if future_msg.is_system:
                    continue
                for comp_pattern in compiled_completions:
                    if comp_pattern.search(future_msg.content):
                        status = "completed"
                        completed_by = future_msg.sender
                        completed_at = future_msg.timestamp.isoformat()
                        break
                if status == "completed":
                    break
        
        action_items.append({
            "promise": text_snippet,
            "assignee": msg.sender,
            "detected_date": msg.timestamp.isoformat(),
            "status": status,
            "completed_by": completed_by,
            "completed_at": completed_at,
            "context": messages[max(0, i-1):i+2]
        })
    
    # Serialize context messages
    for item in action_items:
        item["context"] = [
            f"[{m.timestamp.strftime('%Y-%m-%d %H:%M')}] {m.sender}: {m.content[:100]}"
            for m in item["context"] if not m.is_system and m.sender
        ]
    
    pending_count = sum(1 for a in action_items if a["status"] == "pending")
    completed_count = sum(1 for a in action_items if a["status"] == "completed")
    
    return {
        "action_items": action_items,
        "total": len(action_items),
        "pending_count": pending_count,
        "completed_count": completed_count
    }
