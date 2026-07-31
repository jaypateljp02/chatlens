// Universal Resilient API Base Selector
const getApiBaseUrl = () => {
  if (typeof import.meta !== 'undefined' && import.meta.env && import.meta.env.VITE_API_BASE) {
    return import.meta.env.VITE_API_BASE.replace(/\/$/, '') + '/api';
  }
  if (typeof window !== 'undefined') {
    const host = window.location.hostname;
    if (host === 'localhost' || host === '127.0.0.1') {
      return 'http://localhost:8000/api';
    }
  }
  return '/api';
};

const API_BASE = getApiBaseUrl();

// Synchronous default initialization for activeChatId
if (!localStorage.getItem('activeChatId')) {
  localStorage.setItem('activeChatId', 'all');
  localStorage.setItem('chatMetadata', JSON.stringify({ filename: 'All Chats (Master Memory)', total_messages: 'All Combined' }));
}

async function apiFetch(endpoint, options = {}) {
  try {
    const res = await fetch(`${API_BASE}${endpoint}`, options);
    if (res.ok) return res;
    // Fallback attempt for local port 8000 if relative /api returned 404
    if (API_BASE !== 'http://localhost:8000/api') {
      const fallbackRes = await fetch(`http://localhost:8000/api${endpoint}`, options);
      if (fallbackRes.ok) return fallbackRes;
    }
    return res;
  } catch (e) {
    if (API_BASE !== 'http://localhost:8000/api') {
      return await fetch(`http://localhost:8000/api${endpoint}`, options);
    }
    throw e;
  }
}

export async function getSavedChats() {
  try {
    const res = await apiFetch('/chats');
    if (!res.ok) return [];
    const data = await res.json();
    return data.sessions || [];
  } catch (e) {
    return [];
  }
}

export async function deleteSavedChat(chatId) {
  try {
    const res = await apiFetch(`/chats/${chatId}`, { method: 'DELETE' });
    if (!res.ok) throw new Error('Delete failed');
    return await res.json();
  } catch (e) {
    console.error('Failed to delete chat:', e);
    throw e;
  }
}

export async function completeActionItem(promise) {
  try {
    const res = await apiFetch('/analytics/actions/complete', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ promise })
    });
    if (!res.ok) throw new Error('Completion failed');
    return await res.json();
  } catch (e) {
    console.error('Failed to complete action item:', e);
    throw e;
  }
}

export async function getActiveChatId(chatId) {
  if (chatId) return chatId;
  const active = localStorage.getItem('activeChatId');
  return active || 'all';
}

export async function uploadChat(file) {
  const formData = new FormData();
  formData.append('file', file);
  const res = await apiFetch('/upload', {
    method: 'POST',
    body: formData,
  });
  if (!res.ok) throw new Error('Upload failed');
  const data = await res.json();
  if (data.chat_id) {
    localStorage.setItem('activeChatId', data.chat_id);
    localStorage.setItem('chatMetadata', JSON.stringify(data.metadata));
  }
  return data;
}

export async function loadDemoChatSession() {
  const sampleChatText = `[10/01/2026, 10:15:30] Ravi: Hi team, welcome to the project kick-off!
[10/01/2026, 10:16:05] Priya: Great! Shared the design assets for client review.
[10/01/2026, 10:18:22] Amit: I will set up PostgreSQL and pgvector on Windows Server by Friday.
[10/01/2026, 10:20:00] Ravi: Thanks Priya! Please check pediatric health logs for Taare group as well.
[10/01/2026, 14:30:10] Sneha: Finished pediatric health audit. All symptoms resolved in 48 hours.
[10/01/2026, 14:35:00] Ravi: Excellent job! This deadline is tight, but we will deliver.
[11/01/2026, 11:00:00] Priya: Uploaded 12 new design wireframes to client portal.
[11/01/2026, 15:20:00] Amit: Database migration complete. 50,000 vectors indexed.
[12/01/2026, 16:45:00] Sneha: Python AI workshop completed with 45 attendees!`;

  const blob = new Blob([sampleChatText], { type: 'text/plain' });
  const sampleFile = new File([blob], 'Sample_Project_Chat_Export.txt', { type: 'text/plain' });
  return await uploadChat(sampleFile);
}

export async function getCommunicationStats(chatId) {
  const targetId = await getActiveChatId(chatId);
  const res = await apiFetch(`/analytics/communication/${targetId}`);
  if (!res.ok) throw new Error('Failed to fetch communication stats');
  return await res.json();
}

export async function getSummary(chatId, mode = 'bullet') {
  const targetId = await getActiveChatId(chatId);
  const res = await apiFetch(`/summarize/${targetId}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ mode })
  });
  if (!res.ok) throw new Error('Failed to fetch summary');
  return await res.json();
}

export async function askQuestion(chatId, question) {
  const targetId = await getActiveChatId(chatId);
  const res = await apiFetch(`/ask/${targetId}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question })
  });
  if (!res.ok) throw new Error('Failed to get answer');
  return await res.json();
}

export async function getTopics(chatId) {
  const targetId = await getActiveChatId(chatId);
  const res = await apiFetch(`/topics/${targetId}`);
  if (!res.ok) throw new Error('Failed to fetch topics');
  return await res.json();
}

export async function getSentimentStats(chatId) {
  const targetId = await getActiveChatId(chatId);
  const res = await apiFetch(`/analytics/sentiment/${targetId}`);
  if (!res.ok) throw new Error('Failed to fetch sentiment stats');
  return await res.json();
}

export async function getPeopleProfiles(chatId) {
  const targetId = await getActiveChatId(chatId);
  const res = await apiFetch(`/analytics/people/${targetId}`);
  if (!res.ok) throw new Error('Failed to fetch people profiles');
  return await res.json();
}

export async function getActionItems(chatId) {
  const targetId = await getActiveChatId(chatId);
  const res = await apiFetch(`/analytics/actions/${targetId}`);
  if (!res.ok) throw new Error('Failed to fetch action items');
  return await res.json();
}

export async function getTimeline(chatId) {
  const targetId = await getActiveChatId(chatId);
  const res = await apiFetch(`/analytics/timeline/${targetId}`);
  if (!res.ok) throw new Error('Failed to fetch timeline');
  return await res.json();
}

export async function comparePeriods(chatId, p1Start, p1End, p2Start, p2End) {
  const targetId = await getActiveChatId(chatId);
  const res = await apiFetch(`/analytics/compare/${targetId}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      period1_start: p1Start,
      period1_end: p1End,
      period2_start: p2Start,
      period2_end: p2End
    })
  });
  if (!res.ok) throw new Error('Failed to compare periods');
  return await res.json();
}

export async function getKnowledgeGraph(chatId) {
  const targetId = await getActiveChatId(chatId);
  const res = await apiFetch(`/graph/${targetId}`);
  if (!res.ok) throw new Error('Failed to fetch knowledge graph');
  return await res.json();
}

export async function getMemoryAlerts() {
  try {
    const res = await apiFetch('/memory/alerts');
    if (!res.ok) throw new Error('Failed to fetch memory alerts');
    return await res.json();
  } catch (e) {
    return { alerts: [] };
  }
}
