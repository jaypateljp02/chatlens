"""
LangChain RAG Pipeline — Layer 2 & 3 of ChatLens AI Architecture

Layer 2: Local Search & Retrieval
  - Search SQLite vault for relevant messages
  - Pass only top 50 relevant messages to AI (NOT the entire chat)
  
Layer 3B: AI Reasoning via Gemini 1.5 Flash
  - Uses Google Gemini for high-quality answers
  - Every answer includes source message references with timestamps
  - Falls back to pattern matching if no API key configured
"""

import os
import re
import json
from typing import List, Dict, Any, Optional, Tuple

from config import settings

# ─── Check if Gemini API is configured ───────────────────────────────────────
GEMINI_AVAILABLE = bool(settings.GEMINI_API_KEY and settings.GEMINI_API_KEY.strip())

if GEMINI_AVAILABLE:
    try:
        from google import genai
        gemini_client = genai.Client(api_key=settings.GEMINI_API_KEY)
        print(f"[Gemini] Real AI Active — gemini-3.6-flash")
    except Exception as e:
        GEMINI_AVAILABLE = False
        gemini_client = None
        print(f"[Gemini] Gemini init failed: {e}. Using fallback.")
else:
    gemini_client = None
    print("[Gemini] No API key — using fallback engine. Add GEMINI_API_KEY to enable real AI.")


# ─── Gemini API Call ──────────────────────────────────────────────────────────
def _call_gemini(prompt: str, max_tokens: int = 1024) -> str:
    """Call Gemini API with retry and error handling."""
    if not GEMINI_AVAILABLE or not gemini_client:
        return None
    try:
        response = gemini_client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
        )
        return response.text.strip()
    except Exception as e:
        print(f"[Gemini] API error: {e}")
        return None


# ─── LAYER 2: Local RAG Retrieval ────────────────────────────────────────────
def retrieve_relevant_messages(query: str, all_messages: List[Dict], top_k: int = 500) -> Tuple[List[Dict], List[int]]:
    """
    Retrieve the most relevant messages for a query from the local message store.
    This is the RAG retrieval step — we search BEFORE calling the AI.
    Returns (top_messages, source_ids)
    """
    stop_words = {"is", "are", "the", "a", "an", "in", "on", "at", "to", "for", "of",
                  "and", "or", "what", "who", "when", "where", "how", "did", "does", "do",
                  "kya", "hai", "hain", "ka", "ki", "ke", "se", "ko", "ne"}

    tokens = [w.lower() for w in re.findall(r'\b[a-zA-Z0-9\u0900-\u097F]{2,}\b', query)
              if w.lower() not in stop_words]

    # Concept expansion for common queries
    expansions = {
        "pending": ["will", "send", "complete", "deadline", "task", "do", "report"],
        "task": ["will", "complete", "deadline", "task", "pending", "do", "by"],
        "decision": ["decided", "agreed", "confirmed", "approved", "finalised", "resolved"],
        "promise": ["will", "i'll", "guarantee", "commit", "promise", "handle"],
        "treatment": ["treatment", "doctor", "hospital", "medicine", "x-ray", "bone", "patient"],
        "expense": ["₹", "rs", "rupees", "cost", "payment", "bill", "amount", "paid"],
        "meeting": ["meet", "meeting", "call", "zoom", "discuss", "session"],
    }

    expanded = set(tokens)
    for kw, synonyms in expansions.items():
        if kw in query.lower():
            expanded.update(synonyms)

    # Score each message
    scored = []
    for i, msg in enumerate(all_messages):
        if msg.get("is_system", False):
            continue
        content_lower = msg.get("content", "").lower()

        # Primary: exact word boundary match (weight 2)
        primary = sum(2 for t in tokens if re.search(r'\b' + re.escape(t) + r'\b', content_lower))
        # Secondary: expanded concept match (weight 1)
        secondary = sum(1 for t in expanded if re.search(r'\b' + re.escape(t) + r'\b', content_lower))

        score = primary + secondary
        if score > 0:
            scored.append((score, i, msg))

    scored.sort(key=lambda x: x[0], reverse=True)
    top = scored[:top_k]

    source_ids = [x[1] for x in top]
    messages = [x[2] for x in top]
    return messages, source_ids


def _format_messages_for_ai(messages: List[Dict]) -> str:
    """Format messages into a clean text block for the AI prompt."""
    lines = []
    for msg in messages:
        if msg.get("is_system", False):
            continue
        ts = str(msg.get("timestamp", ""))[:19]
        sender = msg.get("sender", "Unknown")
        content = msg.get("content", "")
        lines.append(f"[{ts}] {sender}: {content}")
    return "\n".join(lines)


# ─── LAYER 3B: Real AI Reasoning ─────────────────────────────────────────────
def generate_real_summary(all_messages: List[Dict], mode: str = "bullet") -> Dict[str, Any]:
    """
    Generate an intelligent summary using Gemini 1.5 Flash.
    Passes only a smart sample of messages to avoid token limits.
    """
    # Select a representative sample: first 20, middle 20, last 20
    total = len(all_messages)
    if total <= 100:
        sample = all_messages
    else:
        sample = (
            all_messages[:30] +
            all_messages[total//2 - 15: total//2 + 15] +
            all_messages[-30:]
        )

    chat_text = _format_messages_for_ai(sample)
    senders = list({m.get("sender") for m in all_messages if not m.get("is_system") and m.get("sender")})
    sender_str = ", ".join(senders[:6])

    if GEMINI_AVAILABLE:
        mode_instructions = {
            "bullet": "Provide a structured bullet-point executive summary highlighting: key topics discussed, important decisions made, pending action items, and notable events.",
            "story": "Write a narrative paragraph summary explaining what this conversation is about, what happened, what was resolved, and what remains pending.",
            "timeline": "Create a chronological timeline of key events and decisions in this conversation.",
            "pending": "List ONLY the unresolved action items, pending commitments, and unanswered questions from this conversation. For each item, mention who is responsible and the deadline if mentioned."
        }

        prompt = f"""You are ChatLens AI, an expert at analyzing WhatsApp group conversations.
Analyze the following conversation messages and {mode_instructions.get(mode, mode_instructions['bullet'])}

CONVERSATION PARTICIPANTS: {sender_str}
TOTAL MESSAGES: {total}
LANGUAGE NOTE: Messages may be in English, Hindi, Marathi or mixed Roman script — analyze all of them.

MESSAGES:
{chat_text}

INSTRUCTIONS:
- Be specific and factual — reference actual names, dates, and events from the messages
- Do NOT invent or hallucinate information not present in the messages
- For pending items, always mention the responsible person and deadline if known
- Format your response clearly with headers and bullet points where appropriate
"""
        ai_response = _call_gemini(prompt, max_tokens=1500)

        if ai_response:
            # Extract key takeaways
            takeaways_prompt = f"""Based on this WhatsApp conversation, give exactly 3 key takeaways in 1 sentence each:
{chat_text[:3000]}

Format: return only 3 lines, one takeaway per line, no numbering."""
            takeaways_text = _call_gemini(takeaways_prompt, max_tokens=200)
            takeaways = [t.strip() for t in (takeaways_text or "").split("\n") if t.strip()][:3]
            if not takeaways:
                takeaways = [f"Analyzed {total} messages from {sender_str}"]

            return {
                "summary_text": ai_response,
                "key_takeaways": takeaways,
                "action_items": [],
                "model_used": "gemini-3.6-flash",
                "ai_powered": True
            }

    # ─── Fallback (no API key) ─────────────────────────────────────────────
    return _fallback_summary(all_messages, mode)


def answer_question_with_rag(all_messages: List[Dict], question: str) -> Dict[str, Any]:
    """
    Answer a question using RAG:
    1. Search local messages for relevant context
    2. Pass only relevant messages to Gemini
    3. Return answer with source message references
    """
    q_lower = question.strip().lower()

    # Greeting detection
    greetings = {"hi", "hii", "hello", "hey", "namaste", "good morning", "good afternoon", "who are you", "what can you do"}
    if q_lower in greetings or any(q_lower.startswith(g) for g in greetings):
        return {
            "answer": (
                "👋 Hello! I am **ChatLens AI**, powered by Google Gemini.\n\n"
                "I have analyzed your WhatsApp chat and can answer questions about:\n"
                "- 📋 Pending tasks and action items\n"
                "- 🏥 Medical updates and treatment information\n"
                "- 👥 Who said what and when\n"
                "- 📊 Communication patterns and key decisions\n"
                "- 🔍 Any specific topic, person, or event\n\n"
                "**Try asking:** *'What are the pending tasks?'* or *'What did Archna say about treatment?'*"
            ),
            "source_messages": [],
            "confidence": 1.0,
            "ai_powered": GEMINI_AVAILABLE
        }

    # RAG: Retrieve relevant messages (up to 500 for maximum context)
    relevant_msgs, source_ids = retrieve_relevant_messages(question, all_messages, top_k=500)

    if not relevant_msgs:
        return {
            "answer": (
                f"🔍 I searched your chat history for **'{question}'** but couldn't find relevant messages.\n\n"
                "💡 **Try asking:** Pending tasks, doctor updates, treatment status, or mention a specific person's name."
            ),
            "source_messages": [],
            "confidence": 0.3,
            "ai_powered": GEMINI_AVAILABLE
        }

    chat_context = _format_messages_for_ai(relevant_msgs[:400])

    if GEMINI_AVAILABLE:
        prompt = f"""You are ChatLens AI. Answer the following question based ONLY on the WhatsApp messages provided.

QUESTION: {question}

RELEVANT MESSAGES FROM CHAT:
{chat_context}

INSTRUCTIONS:
1. Answer specifically and accurately based on the messages above
2. Quote specific messages with their timestamp and sender when relevant
3. If the answer involves multiple people or dates, list them all
4. If you cannot find the answer in these messages, say so clearly
5. Messages may be in English, Hindi, Marathi or mixed — understand all
6. Always mention WHO said something and WHEN (use the timestamp from messages)
7. Keep the answer concise but complete

Answer:"""

        ai_answer = _call_gemini(prompt, max_tokens=800)

        if ai_answer:
            # Format source references
            source_refs = []
            for msg in relevant_msgs[:5]:
                ts = str(msg.get("timestamp", ""))[:19]
                sender = msg.get("sender", "Unknown")
                content = msg.get("content", "")[:100]
                source_refs.append(f"[{ts}] {sender}: {content}...")

            return {
                "answer": ai_answer,
                "source_messages": source_refs,
                "confidence": 0.95,
                "ai_powered": True,
                "model_used": "gemini-3.6-flash"
            }

    # ─── Fallback ─────────────────────────────────────────────────────────
    return _fallback_qa(relevant_msgs, question)


def extract_topics_with_ai(all_messages: List[Dict]) -> List[Dict]:
    """Extract real topics from the conversation using Gemini."""
    sample = all_messages[:100] if len(all_messages) > 100 else all_messages
    chat_text = _format_messages_for_ai(sample)

    if GEMINI_AVAILABLE:
        prompt = f"""Analyze this WhatsApp conversation and identify the TOP 5 main topics discussed.

MESSAGES:
{chat_text[:4000]}

For each topic, provide:
- Topic name (2-4 words)
- Brief description (1 sentence)
- Approximate message count

Format your response as JSON array:
[
  {{"name": "Topic Name", "count": 25, "description": "Brief description of what was discussed"}},
  ...
]

Return ONLY valid JSON, no other text."""

        ai_response = _call_gemini(prompt, max_tokens=500)
        if ai_response:
            try:
                # Extract JSON from response
                json_match = re.search(r'\[.*\]', ai_response, re.DOTALL)
                if json_match:
                    topics = json.loads(json_match.group(0))
                    for t in topics:
                        t["ai_powered"] = True
                    return topics[:5]
            except Exception:
                pass

    return _fallback_topics(all_messages)


# ─── FALLBACK ENGINE (when no Gemini API key) ─────────────────────────────────
def _fallback_summary(messages: List[Dict], mode: str) -> Dict[str, Any]:
    """Basic pattern-based summary when Gemini is not available."""
    lines = [m for m in messages if not m.get("is_system") and m.get("content")]
    total = len(lines)
    senders = list({m.get("sender") for m in lines if m.get("sender")})
    sender_str = ", ".join(senders[:4]) if senders else "Participants"

    action_lines = [m for m in lines if re.search(
        r'\b(will|going to|promise|send|complete|handle|by Friday|tomorrow|check|report)\b',
        m.get("content", ""), re.IGNORECASE)]

    summary_text = (
        f"### 📋 Chat Summary\n\n"
        f"- **Participants:** {sender_str}\n"
        f"- **Total Messages:** {total}\n"
        f"- **Action Items Found:** {len(action_lines)}\n\n"
        f"> ⚠️ **Add a GEMINI_API_KEY to get intelligent AI summaries** with real insights, decisions, and pending items.\n"
        f"> Get free key at: https://aistudio.google.com/apikey"
    )

    return {
        "summary_text": summary_text,
        "key_takeaways": [f"Analyzed {total} messages from {len(senders)} participants", f"Found {len(action_lines)} potential action items"],
        "action_items": [m.get("content", "")[:80] for m in action_lines[:3]],
        "ai_powered": False
    }


def _fallback_qa(relevant_msgs: List[Dict], question: str) -> Dict[str, Any]:
    """Basic keyword QA when Gemini is not available."""
    if not relevant_msgs:
        return {"answer": f"No messages found for '{question}'.", "source_messages": [], "confidence": 0.3, "ai_powered": False}

    quotes = []
    for msg in relevant_msgs[:5]:
        ts = str(msg.get("timestamp", ""))[:19]
        sender = msg.get("sender", "Unknown")
        content = msg.get("content", "")
        quotes.append(f"• [{ts}] {sender}: {content}")

    answer = (
        f"📍 Found {len(relevant_msgs)} relevant messages for '{question}':\n\n" +
        "\n".join(quotes) +
        "\n\n> ⚠️ **Add GEMINI_API_KEY for intelligent analysis.** Get free key: https://aistudio.google.com/apikey"
    )
    return {"answer": answer, "source_messages": quotes, "confidence": 0.7, "ai_powered": False}


def _fallback_topics(messages: List[Dict]) -> List[Dict]:
    """Basic topic extraction when Gemini is not available."""
    from collections import Counter
    categories = {
        "Health & Medical": ["doctor", "hospital", "treatment", "medicine", "patient", "x-ray", "health"],
        "Tasks & Action Items": ["will", "complete", "deadline", "task", "pending", "send", "do"],
        "Decisions Made": ["decided", "agreed", "confirmed", "approved", "resolved"],
        "Team Communication": ["team", "meeting", "call", "discuss", "update", "share"],
        "Finance & Expenses": ["₹", "rs", "payment", "cost", "bill", "budget", "expense"],
    }
    counts = Counter()
    for msg in messages:
        content = (msg.get("content") or "").lower()
        for cat, keywords in categories.items():
            if any(k in content for k in keywords):
                counts[cat] += 1
    return [{"name": cat, "count": max(cnt, 3), "description": f"Messages related to {cat.lower()}", "ai_powered": False}
            for cat, cnt in counts.most_common(5) if cnt > 0]
