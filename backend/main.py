from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List
import uuid
import os
import json
from datetime import datetime, date

from config import settings
from parser.whatsapp_parser import parse_whatsapp_chat
from analytics.communication import calculate_communication_stats
from analytics.sentiment import calculate_sentiment_stats
from analytics.people import calculate_people_profiles
from analytics.actions import detect_action_items, mark_promise_completed
from analytics.timeline import extract_timeline, compare_periods
from analytics.knowledge_graph import generate_knowledge_graph
from analytics.report_generator import generate_executive_report
from ai.rag_memory import ingest_chat_into_memory, query_cross_chat_memory, detect_proactive_alerts
from ai.gemma_client import generate_gemma_summary, answer_gemma_question, extract_gemma_topics

from models.schemas import (
    UploadResponse, CommunicationStats, ParsedMessage, ChatMetadata,
    SummaryRequest, SummaryResponse, AskQuestionRequest, AskQuestionResponse, TopicResponse,
    SentimentStats, PeopleProfilesResponse, ActionItemsResponse, TimelineResponse,
    ComparisonRequest, ComparisonResponse
)

app = FastAPI(title="ChatLens AI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Persistent disk storage directory
STORAGE_DIR = os.path.join(os.path.dirname(__file__), "uploads", "sessions")
os.makedirs(STORAGE_DIR, exist_ok=True)

# In-memory RAM cache
chat_store: Dict[str, List[ParsedMessage]] = {}
chat_metadata_store: Dict[str, ChatMetadata] = {}

def _save_session_to_disk(chat_id: str, filename: str, text: str, messages: List[ParsedMessage], metadata: ChatMetadata):
    """Save session and parsed messages to disk for persistent recall across server restarts."""
    filepath = os.path.join(STORAGE_DIR, f"{chat_id}.json")
    msg_dicts = []
    for m in messages:
        msg_dicts.append({
            "timestamp": m.timestamp.isoformat() if hasattr(m.timestamp, 'isoformat') else str(m.timestamp),
            "sender": m.sender,
            "content": m.content,
            "message_type": m.message_type,
            "is_system": m.is_system
        })
    
    dr = metadata.date_range
    if hasattr(dr, 'dict'):
        dr = dr.dict()
    elif hasattr(dr, 'model_dump'):
        dr = dr.model_dump()
    
    date_range_val = {}
    if isinstance(dr, dict):
        for k, v in dr.items():
            if isinstance(v, (datetime, date)):
                date_range_val[k] = v.isoformat()
            else:
                date_range_val[k] = str(v)
    else:
        date_range_val = str(dr)

    meta_dict = {
        "filename": metadata.filename,
        "total_messages": metadata.total_messages,
        "participants": metadata.participants,
        "date_range": date_range_val,
        "group_name": metadata.group_name
    }
    session_data = {
        "chat_id": chat_id,
        "filename": filename,
        "raw_text": text[:50000],
        "metadata": meta_dict,
        "messages": msg_dicts,
        "saved_at": datetime.now().isoformat()
    }
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(session_data, f, ensure_ascii=False, indent=2)

def _load_session_from_disk(chat_id: str) -> bool:
    """Load session from disk if not present in RAM cache."""
    filepath = os.path.join(STORAGE_DIR, f"{chat_id}.json")
    if not os.path.exists(filepath):
        return False
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        parsed_msgs = []
        for m in data.get("messages", []):
            ts = datetime.fromisoformat(m["timestamp"])
            parsed_msgs.append(ParsedMessage(
                timestamp=ts,
                sender=m.get("sender"),
                content=m.get("content", ""),
                message_type=m.get("message_type", "text"),
                is_system=m.get("is_system", False)
            ))
        
        meta = data.get("metadata", {})
        metadata_obj = ChatMetadata(
            filename=meta.get("filename", "WhatsApp Chat"),
            total_messages=meta.get("total_messages", len(parsed_msgs)),
            participants=meta.get("participants", []),
            date_range=meta.get("date_range", {"start": "", "end": ""}),
            group_name=meta.get("group_name", "WhatsApp Group")
        )

        chat_store[chat_id] = parsed_msgs
        chat_metadata_store[chat_id] = metadata_obj
        ingest_chat_into_memory(chat_id, metadata_obj.filename, parsed_msgs)
        return True
    except Exception as e:
        print(f"Error loading session {chat_id} from disk:", e)
        return False

def _get_all_stored_messages() -> List[ParsedMessage]:
    """Retrieve all parsed messages combined across ALL chat sessions in RAM and on Disk."""
    if os.path.exists(STORAGE_DIR):
        for fname in os.listdir(STORAGE_DIR):
            if fname.endswith(".json"):
                cid = fname.replace(".json", "")
                if cid not in chat_store:
                    _load_session_from_disk(cid)

    all_msgs = []
    for cid, msg_list in chat_store.items():
        all_msgs.extend(msg_list)
        
    return all_msgs

def _auto_seed_sample_session():
    """Ensure at least one sample session exists on disk for instant Master Memory availability."""
    if os.path.exists(STORAGE_DIR) and len(os.listdir(STORAGE_DIR)) == 0:
        sample_text = """[10/01/2026, 10:15:30] Ravi: Hi team, welcome to the project kick-off!
[10/01/2026, 10:16:05] Priya: Great! Shared the design assets for client review.
[10/01/2026, 10:18:22] Amit: I will set up PostgreSQL and pgvector on Windows Server by Friday.
[10/01/2026, 10:20:00] Ravi: Thanks Priya! Please check pediatric health logs for Taare group as well.
[10/01/2026, 14:30:10] Sneha: Finished pediatric health audit. All symptoms resolved in 48 hours.
[10/01/2026, 14:35:00] Ravi: Excellent job! This deadline is tight, but we will deliver.
[11/01/2026, 11:00:00] Priya: Uploaded 12 new design wireframes to client portal.
[11/01/2026, 15:20:00] Amit: Database migration complete. 50,000 vectors indexed.
[12/01/2026, 16:45:00] Sneha: Python AI workshop completed with 45 attendees!"""
        msgs, meta = parse_whatsapp_chat(sample_text, "Sample_Project_Chat_Export.txt")
        cid = "demo-sample-session"
        chat_store[cid] = msgs
        chat_metadata_store[cid] = meta
        _save_session_to_disk(cid, "Sample_Project_Chat_Export.txt", sample_text, msgs, meta)

_auto_seed_sample_session()

@app.get("/api/health")
def health_check():
    return {"status": "ok", "engine": "ChatLens On-Device AI Active"}

@app.get("/api/chats")
def list_saved_chats():
    """List all saved chat sessions stored on disk."""
    sessions = []
    if os.path.exists(STORAGE_DIR):
        for fname in os.listdir(STORAGE_DIR):
            if fname.endswith(".json"):
                cid = fname.replace(".json", "")
                fpath = os.path.join(STORAGE_DIR, fname)
                try:
                    with open(fpath, "r", encoding="utf-8") as f:
                        d = json.load(f)
                    sessions.append({
                        "chat_id": cid,
                        "filename": d.get("filename", "Chat"),
                        "total_messages": d.get("metadata", {}).get("total_messages", 0),
                        "saved_at": d.get("saved_at")
                    })
                except Exception:
                    pass
    return {"sessions": sessions}

@app.delete("/api/chats/{chat_id}")
def delete_saved_chat(chat_id: str):
    """Delete an uploaded chat session from disk storage and RAM cache."""
    if chat_id == "all":
        if os.path.exists(STORAGE_DIR):
            for fname in os.listdir(STORAGE_DIR):
                if fname.endswith(".json"):
                    os.remove(os.path.join(STORAGE_DIR, fname))
        chat_store.clear()
        chat_metadata_store.clear()
        return {"status": "success", "message": "All saved chat sessions deleted from memory."}
        
    filepath = os.path.join(STORAGE_DIR, f"{chat_id}.json")
    if os.path.exists(filepath):
        os.remove(filepath)
        
    chat_store.pop(chat_id, None)
    chat_metadata_store.pop(chat_id, None)
    return {"status": "success", "deleted_chat_id": chat_id}

@app.post("/api/upload", response_model=UploadResponse)
async def upload_chat(file: UploadFile = File(...)):
    if not file.filename.endswith(".txt"):
        raise HTTPException(status_code=400, detail="Only .txt files are supported")
        
    content = await file.read()
    
    text = None
    for enc in ["utf-8", "utf-16", "latin-1"]:
        try:
            text = content.decode(enc)
            break
        except UnicodeDecodeError:
            continue
            
    if text is None:
        raise HTTPException(status_code=400, detail="Could not decode the file. Ensure it is UTF-8 encoded.")
    
    if len(content) > settings.MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=400, detail=f"File exceeds maximum size of {settings.MAX_FILE_SIZE_MB}MB")
        
    messages, metadata = parse_whatsapp_chat(text, file.filename)
    
    chat_id = str(uuid.uuid4())
    chat_store[chat_id] = messages
    chat_metadata_store[chat_id] = metadata
    
    # Save session permanently to disk
    _save_session_to_disk(chat_id, file.filename, text, messages, metadata)
    
    # Auto-ingest into RAG Memory Layer
    ingest_chat_into_memory(chat_id, file.filename, messages)
    
    return UploadResponse(
        chat_id=chat_id,
        metadata=metadata,
        preview_messages=messages[:50]
    )

def _get_messages(chat_id: str) -> List[ParsedMessage]:
    if chat_id == "all":
        return _get_all_stored_messages()
        
    if chat_id not in chat_store:
        loaded = _load_session_from_disk(chat_id)
        if not loaded:
            if os.path.exists(STORAGE_DIR):
                saved = [f for f in os.listdir(STORAGE_DIR) if f.endswith(".json")]
                if saved:
                    latest_cid = saved[-1].replace(".json", "")
                    _load_session_from_disk(latest_cid)
                    if latest_cid in chat_store:
                        return chat_store[latest_cid]
            raise HTTPException(status_code=404, detail="Chat session not found. Please upload a WhatsApp chat file.")
    return chat_store[chat_id]

@app.get("/api/analytics/communication/{chat_id}", response_model=CommunicationStats)
def get_communication_stats(chat_id: str):
    messages = _get_messages(chat_id)
    return calculate_communication_stats(messages)

def _get_chat_text(chat_id: str) -> str:
    messages = _get_messages(chat_id)
    lines = []
    for msg in messages:
        if not msg.is_system:
            sender = msg.sender or "Unknown"
            lines.append(f"[{msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] {sender}: {msg.content}")
    return "\n".join(lines)

@app.post("/api/summarize/{chat_id}", response_model=SummaryResponse)
def summarize_chat(chat_id: str, request: SummaryRequest):
    chat_text = _get_chat_text(chat_id)
    result = generate_gemma_summary(chat_text, request.mode)
    return SummaryResponse(**result)

@app.post("/api/ask/{chat_id}", response_model=AskQuestionResponse)
def ask_question(chat_id: str, request: AskQuestionRequest):
    chat_text = _get_chat_text(chat_id)
    result = answer_gemma_question(chat_text, request.question)
    return AskQuestionResponse(**result)

@app.get("/api/topics/{chat_id}", response_model=TopicResponse)
def get_topics(chat_id: str):
    chat_text = _get_chat_text(chat_id)
    topics = extract_gemma_topics(chat_text)
    return TopicResponse(topics=topics)

@app.get("/api/analytics/sentiment/{chat_id}", response_model=SentimentStats)
def get_sentiment_stats(chat_id: str):
    messages = _get_messages(chat_id)
    return calculate_sentiment_stats(messages)

@app.get("/api/analytics/people/{chat_id}", response_model=PeopleProfilesResponse)
def get_people_profiles(chat_id: str):
    messages = _get_messages(chat_id)
    return calculate_people_profiles(messages)

@app.get("/api/analytics/actions/{chat_id}", response_model=ActionItemsResponse)
def get_action_items(chat_id: str):
    messages = _get_messages(chat_id)
    return detect_action_items(messages)

@app.post("/api/analytics/actions/complete")
def complete_action_item(request: dict):
    promise = request.get("promise")
    if promise:
        mark_promise_completed(promise)
        return {"status": "success", "promise": promise, "message": "Action item marked complete in memory."}
    raise HTTPException(status_code=400, detail="Promise text is required.")

@app.get("/api/analytics/timeline/{chat_id}", response_model=TimelineResponse)
def get_timeline(chat_id: str):
    messages = _get_messages(chat_id)
    return extract_timeline(messages)

@app.post("/api/analytics/compare/{chat_id}", response_model=ComparisonResponse)
def compare_chat_periods(chat_id: str, request: ComparisonRequest):
    messages = _get_messages(chat_id)
    return compare_periods(
        messages,
        request.period1_start,
        request.period1_end,
        request.period2_start,
        request.period2_end
    )

@app.get("/api/report/html/{chat_id}", response_class=HTMLResponse)
def download_executive_report(chat_id: str):
    """Generate printable HTML executive report."""
    messages = _get_messages(chat_id)
    title = "Master Organization Summary" if chat_id == "all" else "WhatsApp Chat Audit Report"
    html_content = generate_executive_report(messages, title)
    return HTMLResponse(content=html_content, status_code=200)

# --- Module 10: Master Cross-Chat Knowledge Graph & Memory Endpoints ---

@app.get("/api/graph/{chat_id}")
def get_knowledge_graph(chat_id: str):
    messages = _get_messages(chat_id)
    name = "Master Organization Memory" if chat_id == "all" else "WhatsApp Group"
    return generate_knowledge_graph(messages, name)

@app.post("/api/memory/query")
def query_memory(request: AskQuestionRequest):
    return query_cross_chat_memory(request.question)

@app.get("/api/memory/alerts")
def get_memory_alerts():
    return {"alerts": detect_proactive_alerts()}

# --- UNIFIED FRONTEND STATIC FILES MOUNTING FOR ALL-IN-ONE RENDER DEPLOYMENT ---
candidate_paths = [
    os.path.join(os.path.dirname(__file__), "..", "frontend", "dist"),
    os.path.join(os.getcwd(), "..", "frontend", "dist"),
    os.path.join(os.getcwd(), "frontend", "dist"),
    "/opt/render/project/src/frontend/dist"
]

FRONTEND_DIST = None
for p in candidate_paths:
    if os.path.exists(p) and os.path.isdir(p):
        FRONTEND_DIST = os.path.abspath(p)
        break

if FRONTEND_DIST:
    assets_dir = os.path.join(FRONTEND_DIST, "assets")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    @app.get("/{full_path:path}")
    def serve_frontend_spa(full_path: str = ""):
        if full_path.startswith("api/"):
            raise HTTPException(status_code=404, detail="API route not found")
        file_path = os.path.join(FRONTEND_DIST, full_path)
        if full_path and os.path.exists(file_path) and os.path.isfile(file_path):
            return FileResponse(file_path)
        index_file = os.path.join(FRONTEND_DIST, "index.html")
        if os.path.exists(index_file):
            return FileResponse(index_file)
        raise HTTPException(status_code=404, detail="Frontend index.html not found")
