import os
from config import settings
from ai.prompts import RAG_SYSTEM_PROMPT, SUMMARY_PROMPTS

try:
    import openai
    from openai import OpenAI
    
    api_key = getattr(settings, 'OPENAI_API_KEY', os.environ.get("OPENAI_API_KEY"))
    client = OpenAI(api_key=api_key) if api_key else None
except ImportError:
    client = None

def answer_question(chat_text: str, question: str) -> dict:
    """Answer a question about the chat using OpenAI."""
    if not client:
        return {
            "answer": "Mock Answer: This is a placeholder because OpenAI API is not configured.",
            "source_messages": ["Mock message 1"],
            "confidence": 0.85
        }
        
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": RAG_SYSTEM_PROMPT},
                {"role": "user", "content": f"Context:\n{chat_text[:30000]}\n\nQuestion: {question}"}
            ]
        )
        return {
            "answer": response.choices[0].message.content,
            "source_messages": [],
            "confidence": 0.95
        }
    except Exception as e:
        return {
            "answer": f"Mock Answer (API Error: {str(e)})",
            "source_messages": [],
            "confidence": 0.0
        }

def generate_story(chat_text: str) -> dict:
    """Generate a story summary using OpenAI."""
    if not client:
        return {
            "summary_text": "Mock Story: Two people started talking and became great friends.",
            "key_takeaways": ["Friendship"],
            "action_items": []
        }
        
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SUMMARY_PROMPTS["story"]},
                {"role": "user", "content": chat_text[:30000]}
            ]
        )
        return {
            "summary_text": response.choices[0].message.content,
            "key_takeaways": [],
            "action_items": []
        }
    except Exception as e:
        return {
            "summary_text": f"Mock Story (API Error: {str(e)})",
            "key_takeaways": [],
            "action_items": []
        }
