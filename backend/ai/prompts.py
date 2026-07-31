# AI Prompts

SUMMARY_PROMPTS = {
    "bullet": "Summarize this WhatsApp chat in bullet points. Focus on major and minor tasks given and completed.",
    "story": "Summarize this WhatsApp chat as a story, focusing on the relationship evolution narrative.",
    "timeline": "Summarize this WhatsApp chat chronologically, highlighting major milestones and project progress.",
    "pending": "List pending items, ideas, unresolved issues, assignments, and follow-ups from this WhatsApp chat."
}

RAG_SYSTEM_PROMPT = (
    "You are an AI assistant helping a user extract information from a WhatsApp chat. "
    "Use the provided chat context to answer the user's question accurately. "
    "If the answer is not in the context, say so."
)

TOPIC_EXTRACTION_PROMPT = (
    "Extract the main topics or themes from this WhatsApp chat (e.g., health, training, projects, personal). "
    "Provide the output as a list of up to 5 topics with brief descriptions."
)
