"""
SQLite Structured Vault — Layer 1 of ChatLens AI Architecture
Every imported WhatsApp chat becomes a structured database, not just a .txt file.
This is the permanent source of truth. AI summaries are derived and regenerable.
"""

import sqlite3
import json
import os
import re
from datetime import datetime
from typing import List, Dict, Any, Optional

VAULT_DIR = os.path.join(os.path.dirname(__file__), "..", "uploads", "vault")
os.makedirs(VAULT_DIR, exist_ok=True)

MASTER_DB_PATH = os.path.join(VAULT_DIR, "chatlens_master.db")


def get_db(db_path: str = MASTER_DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize the master SQLite database with all required tables."""
    conn = get_db()
    cursor = conn.cursor()

    # ─── CONVERSATIONS TABLE ───────────────────────────────────────────────────
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id TEXT PRIMARY KEY,
            filename TEXT NOT NULL,
            group_name TEXT,
            total_messages INTEGER DEFAULT 0,
            participants TEXT,       -- JSON array
            date_start TEXT,
            date_end TEXT,
            imported_at TEXT,
            status TEXT DEFAULT 'active'
        )
    """)

    # ─── MESSAGES TABLE ────────────────────────────────────────────────────────
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id TEXT NOT NULL,
            sender TEXT,
            timestamp TEXT NOT NULL,
            content TEXT NOT NULL,
            message_type TEXT DEFAULT 'text',
            is_system INTEGER DEFAULT 0,
            reply_to_id INTEGER,
            has_link INTEGER DEFAULT 0,
            has_media INTEGER DEFAULT 0,
            FOREIGN KEY (conversation_id) REFERENCES conversations(id)
        )
    """)

    # ─── EXTRACTED OBJECTS TABLE (Bandhu-compatible) ──────────────────────────
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS extracted_objects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id TEXT NOT NULL,
            message_id INTEGER,
            object_type TEXT NOT NULL,  -- task, decision, promise, question, expense, person, topic
            content TEXT NOT NULL,
            owner TEXT,               -- person responsible
            deadline TEXT,
            status TEXT DEFAULT 'open',  -- open, completed, cancelled
            confidence REAL DEFAULT 0.8,
            source_timestamp TEXT,
            metadata TEXT,            -- JSON for extra fields
            created_at TEXT,
            FOREIGN KEY (conversation_id) REFERENCES conversations(id),
            FOREIGN KEY (message_id) REFERENCES messages(id)
        )
    """)

    # ─── PERSONS TABLE ────────────────────────────────────────────────────────
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT,
            total_messages INTEGER DEFAULT 0,
            first_seen TEXT,
            last_seen TEXT,
            conversation_ids TEXT,    -- JSON array
            sentiment_avg REAL DEFAULT 0.5,
            communication_style TEXT,
            metadata TEXT
        )
    """)

    # ─── AI INSIGHTS TABLE ───────────────────────────────────────────────────
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ai_insights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id TEXT NOT NULL,
            insight_type TEXT NOT NULL,  -- summary, qa_answer, topic_analysis
            question TEXT,
            answer TEXT NOT NULL,
            source_message_ids TEXT,     -- JSON array of message IDs
            confidence REAL DEFAULT 0.9,
            model_used TEXT DEFAULT 'gemini-1.5-flash',
            created_at TEXT,
            FOREIGN KEY (conversation_id) REFERENCES conversations(id)
        )
    """)

    # ─── INDEXES FOR FAST SEARCH ──────────────────────────────────────────────
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_messages_conv ON messages(conversation_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_messages_sender ON messages(sender)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_messages_timestamp ON messages(timestamp)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_extracted_type ON extracted_objects(object_type)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_extracted_status ON extracted_objects(status)")

    conn.commit()
    conn.close()
    print("[SQLite Vault] Database initialized successfully.")


def save_conversation(chat_id: str, filename: str, messages: List[Dict], metadata: Dict) -> str:
    """Save a parsed chat conversation to the structured SQLite vault."""
    conn = get_db()
    cursor = conn.cursor()

    participants = metadata.get("participants", [])
    dr = metadata.get("date_range", {})

    # Insert conversation record
    cursor.execute("""
        INSERT OR REPLACE INTO conversations
        (id, filename, group_name, total_messages, participants, date_start, date_end, imported_at, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'active')
    """, (
        chat_id,
        filename,
        metadata.get("group_name", filename),
        len(messages),
        json.dumps(participants),
        str(dr.get("start", "")),
        str(dr.get("end", "")),
        datetime.now().isoformat()
    ))

    # Insert all messages
    message_ids = []
    for msg in messages:
        content = msg.get("content", "")
        has_link = 1 if re.search(r'https?://', content) else 0
        has_media = 1 if re.search(r'<Media omitted>|image omitted|video omitted|audio omitted|document|\.pdf|\.jpg|\.mp4', content, re.IGNORECASE) else 0

        cursor.execute("""
            INSERT INTO messages
            (conversation_id, sender, timestamp, content, message_type, is_system, has_link, has_media)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            chat_id,
            msg.get("sender", "Unknown"),
            str(msg.get("timestamp", "")),
            content,
            msg.get("message_type", "text"),
            1 if msg.get("is_system", False) else 0,
            has_link,
            has_media
        ))
        message_ids.append(cursor.lastrowid)

    conn.commit()
    conn.close()

    # Run Stage A extraction (deterministic, no LLM needed)
    _extract_objects_stage_a(chat_id, messages, message_ids)

    return chat_id


def _extract_objects_stage_a(chat_id: str, messages: List[Dict], message_ids: List[int]):
    """
    Stage A: Deterministic extraction — no LLM needed.
    Extracts tasks, promises, decisions, questions, expenses from messages
    and stores them as structured Bandhu-compatible objects in SQLite.
    """
    conn = get_db()
    cursor = conn.cursor()
    now = datetime.now().isoformat()

    TASK_PATTERNS = [
        r'\b(will|going to|shall|need to|have to|must)\b.{0,60}\b(send|do|complete|finish|check|update|submit|prepare|arrange|confirm|call|follow|report|fix|review|share|upload|make|create|handle|deliver|collect)\b',
        r'\b(by|before|deadline|due)\b.{0,30}\b(friday|monday|tuesday|wednesday|thursday|saturday|sunday|tomorrow|today|next week|end of day|eod|morning|evening)\b',
        r'\b(task|action item|todo|to-do|pending|assigned to)\b',
    ]

    DECISION_PATTERNS = [
        r'\b(decided|agreed|confirmed|approved|finalised|finalized|resolved|concluded|chosen|selected)\b',
        r'\b(we will|let\'s|lets|go ahead|proceed with|moving forward with)\b',
    ]

    QUESTION_PATTERNS = [
        r'\?$',
        r'\b(kya|क्या|when will|what about|any update|status of|have you|did you|is it done|please confirm|please check)\b',
    ]

    EXPENSE_PATTERNS = [
        r'\b(₹|rs\.?|inr|rupees?)\s*[\d,]+',
        r'\b[\d,]+\s*(₹|rs\.?|inr|rupees?)\b',
        r'\b(cost|price|payment|invoice|bill|fee|budget|expense|paid|amount)\b.{0,30}\b[\d,]+\b',
    ]

    COMMITMENT_PATTERNS = [
        r'\b(i will|i\'ll|i promise|i commit|i guarantee|count on me|leave it to me|i\'ll handle|i take responsibility)\b',
        r'\b(mein karunga|mein kar lena|mein dekh leta|main karti hoon|main bhejti hoon)\b',
    ]

    for i, msg in enumerate(messages):
        content = msg.get("content", "")
        if not content or msg.get("is_system", False):
            continue

        content_lower = content.lower()
        msg_id = message_ids[i] if i < len(message_ids) else None
        sender = msg.get("sender", "Unknown")
        ts = str(msg.get("timestamp", ""))

        # Extract TASKS
        for pattern in TASK_PATTERNS:
            if re.search(pattern, content_lower, re.IGNORECASE):
                # Try to find deadline
                deadline_match = re.search(r'\b(by|before|on)\s+(friday|monday|tuesday|wednesday|thursday|saturday|sunday|tomorrow|today|\d{1,2}[\/\-]\d{1,2})', content_lower, re.IGNORECASE)
                deadline = deadline_match.group(0) if deadline_match else None

                cursor.execute("""
                    INSERT INTO extracted_objects
                    (conversation_id, message_id, object_type, content, owner, deadline, status, confidence, source_timestamp, created_at)
                    VALUES (?, ?, 'task', ?, ?, ?, 'open', 0.85, ?, ?)
                """, (chat_id, msg_id, content[:300], sender, deadline, ts, now))
                break

        # Extract DECISIONS
        for pattern in DECISION_PATTERNS:
            if re.search(pattern, content_lower, re.IGNORECASE):
                cursor.execute("""
                    INSERT INTO extracted_objects
                    (conversation_id, message_id, object_type, content, owner, status, confidence, source_timestamp, created_at)
                    VALUES (?, ?, 'decision', ?, ?, 'recorded', 0.80, ?, ?)
                """, (chat_id, msg_id, content[:300], sender, ts, now))
                break

        # Extract COMMITMENTS/PROMISES
        for pattern in COMMITMENT_PATTERNS:
            if re.search(pattern, content_lower, re.IGNORECASE):
                cursor.execute("""
                    INSERT INTO extracted_objects
                    (conversation_id, message_id, object_type, content, owner, status, confidence, source_timestamp, created_at)
                    VALUES (?, ?, 'promise', ?, ?, 'open', 0.90, ?, ?)
                """, (chat_id, msg_id, content[:300], sender, ts, now))
                break

        # Extract UNANSWERED QUESTIONS
        for pattern in QUESTION_PATTERNS:
            if re.search(pattern, content.strip(), re.IGNORECASE):
                cursor.execute("""
                    INSERT INTO extracted_objects
                    (conversation_id, message_id, object_type, content, owner, status, confidence, source_timestamp, created_at)
                    VALUES (?, ?, 'question', ?, ?, 'unanswered', 0.75, ?, ?)
                """, (chat_id, msg_id, content[:300], sender, ts, now))
                break

        # Extract EXPENSES
        for pattern in EXPENSE_PATTERNS:
            if re.search(pattern, content, re.IGNORECASE):
                amount_match = re.search(r'[\d,]+', content)
                amount = amount_match.group(0) if amount_match else ""
                cursor.execute("""
                    INSERT INTO extracted_objects
                    (conversation_id, message_id, object_type, content, owner, status, confidence, source_timestamp, metadata, created_at)
                    VALUES (?, ?, 'expense', ?, ?, 'recorded', 0.85, ?, ?, ?)
                """, (chat_id, msg_id, content[:300], sender, ts, json.dumps({"amount": amount}), now))
                break

    conn.commit()
    conn.close()
    print(f"[Stage A] Extraction complete for chat {chat_id}")


def search_messages(query: str, conversation_id: str = "all", limit: int = 50) -> List[Dict]:
    """
    Layer 2: Local Search — retrieve the most relevant messages for a query.
    This is the RAG retrieval step. We search BEFORE calling the AI.
    """
    conn = get_db()
    cursor = conn.cursor()

    # Build search tokens
    stop_words = {"is", "are", "the", "a", "an", "in", "on", "at", "to", "for", "of", "and", "or", "what", "who", "when", "where", "how", "did", "does", "do"}
    tokens = [w.lower() for w in re.findall(r'\b[a-zA-Z0-9\u0900-\u097F]{2,}\b', query) if w.lower() not in stop_words]

    if not tokens:
        tokens = [query.lower()]

    results = []
    seen_ids = set()

    for token in tokens[:5]:  # Use top 5 tokens
        if conversation_id == "all":
            cursor.execute("""
                SELECT m.*, c.filename, c.group_name
                FROM messages m
                JOIN conversations c ON m.conversation_id = c.id
                WHERE m.content LIKE ? AND m.is_system = 0
                ORDER BY m.timestamp DESC
                LIMIT ?
            """, (f"%{token}%", limit))
        else:
            cursor.execute("""
                SELECT m.*, c.filename, c.group_name
                FROM messages m
                JOIN conversations c ON m.conversation_id = c.id
                WHERE m.conversation_id = ? AND m.content LIKE ? AND m.is_system = 0
                ORDER BY m.timestamp DESC
                LIMIT ?
            """, (conversation_id, f"%{token}%", limit))

        for row in cursor.fetchall():
            if row["id"] not in seen_ids:
                seen_ids.add(row["id"])
                results.append(dict(row))

    conn.close()

    # Sort by timestamp descending, return top limit
    results.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    return results[:limit]


def get_extracted_objects(conversation_id: str = "all", object_type: str = None, status: str = None) -> List[Dict]:
    """Get structured extracted objects (tasks, decisions, promises, etc.)"""
    conn = get_db()
    cursor = conn.cursor()

    query = "SELECT * FROM extracted_objects WHERE 1=1"
    params = []

    if conversation_id != "all":
        query += " AND conversation_id = ?"
        params.append(conversation_id)

    if object_type:
        query += " AND object_type = ?"
        params.append(object_type)

    if status:
        query += " AND status = ?"
        params.append(status)

    query += " ORDER BY source_timestamp DESC LIMIT 500"
    cursor.execute(query, params)
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return results


def update_object_status(object_id: int, status: str):
    """Update status of an extracted object (e.g. mark task as complete)."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE extracted_objects SET status = ? WHERE id = ?", (status, object_id))
    conn.commit()
    conn.close()


def get_all_conversations() -> List[Dict]:
    """List all imported conversations."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM conversations WHERE status = 'active' ORDER BY imported_at DESC")
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return results


def delete_conversation(conversation_id: str):
    """Remove a conversation and all its data from the vault."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM extracted_objects WHERE conversation_id = ?", (conversation_id,))
    cursor.execute("DELETE FROM ai_insights WHERE conversation_id = ?", (conversation_id,))
    cursor.execute("DELETE FROM messages WHERE conversation_id = ?", (conversation_id,))
    cursor.execute("DELETE FROM conversations WHERE id = ?", (conversation_id,))
    conn.commit()
    conn.close()


def get_context_window(message_id: int, window: int = 5) -> List[Dict]:
    """Get surrounding context messages around a specific message for verification."""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT conversation_id FROM messages WHERE id = ?", (message_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return []

    conv_id = row["conversation_id"]
    cursor.execute("""
        SELECT * FROM messages
        WHERE conversation_id = ? AND id BETWEEN ? AND ?
        ORDER BY id ASC
    """, (conv_id, message_id - window, message_id + window))

    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return results


# Initialize DB on module import
init_db()
