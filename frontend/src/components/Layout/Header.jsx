import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { User, UploadCloud, Folder, Globe, FileText, Trash2, Cpu } from 'lucide-react';
import { getSavedChats, deleteSavedChat } from '../../utils/api';
import './Header.css';

export default function Header() {
  const location = useLocation();
  const navigate = useNavigate();
  const [savedSessions, setSavedSessions] = useState([]);
  
  const activeChatId = localStorage.getItem('activeChatId') || 'all';
  let meta = null;
  try {
    meta = JSON.parse(localStorage.getItem('chatMetadata') || '{}');
  } catch (e) {}

  useEffect(() => {
    async function loadSessions() {
      const chats = await getSavedChats();
      setSavedSessions(chats);
      if (!localStorage.getItem('activeChatId')) {
        localStorage.setItem('activeChatId', 'all');
        localStorage.setItem('chatMetadata', JSON.stringify({ filename: 'All Chats (Master Memory)', total_messages: 'All Combined' }));
      }
    }
    loadSessions();
  }, []);

  const getPageTitle = () => {
    const path = location.pathname;
    if (path === '/') return 'Upload Chat';
    const formatted = path.substring(1).replace(/-/g, ' ');
    return formatted.charAt(0).toUpperCase() + formatted.slice(1);
  };

  const handleSelectSession = (e) => {
    const selectedCid = e.target.value;
    if (selectedCid === 'new') {
      localStorage.removeItem('activeChatId');
      localStorage.removeItem('chatMetadata');
      navigate('/');
      window.location.reload();
      return;
    }
    if (selectedCid === 'all') {
      localStorage.setItem('activeChatId', 'all');
      localStorage.setItem('chatMetadata', JSON.stringify({ filename: 'All Chats (Master Memory)', total_messages: 'All Combined' }));
      window.location.reload();
      return;
    }
    const found = savedSessions.find(s => s.chat_id === selectedCid);
    if (found) {
      localStorage.setItem('activeChatId', found.chat_id);
      localStorage.setItem('chatMetadata', JSON.stringify({ filename: found.filename, total_messages: found.total_messages }));
      window.location.reload();
    }
  };

  const handleDeleteActiveChat = async () => {
    const cid = activeChatId || 'all';
    const targetName = meta?.filename || 'selected chat';
    
    if (cid === 'all') {
      if (window.confirm('Are you sure you want to delete ALL saved chat files from memory? This cannot be undone.')) {
        try {
          await deleteSavedChat('all');
          localStorage.setItem('activeChatId', 'all');
          localStorage.setItem('chatMetadata', JSON.stringify({ filename: 'All Chats (Master Memory)', total_messages: 'All Combined' }));
          window.location.reload();
        } catch (e) {
          alert('Failed to delete all chats.');
        }
      }
      return;
    }

    if (window.confirm(`Are you sure you want to delete "${targetName}" from memory?`)) {
      try {
        await deleteSavedChat(cid);
        localStorage.setItem('activeChatId', 'all');
        localStorage.setItem('chatMetadata', JSON.stringify({ filename: 'All Chats (Master Memory)', total_messages: 'All Combined' }));
        window.location.reload();
      } catch (e) {
        alert('Failed to delete selected chat.');
      }
    }
  };

  const handleExportReport = () => {
    const cid = activeChatId || 'all';
    window.open(`http://localhost:8000/api/report/html/${cid}`, '_blank');
  };

  return (
    <header className="header" id="main-header">
      <div className="header-title animate-slide-in-left">
        <h1>{getPageTitle()}</h1>
        {meta?.filename && (
          <span style={{ fontSize: '12px', color: 'var(--primary-dark)', marginLeft: '12px', fontWeight: '600', display: 'inline-flex', alignItems: 'center', gap: '4px' }}>
            {activeChatId === 'all' && <Globe size={12} />}
            Active View: {meta.filename} {meta.total_messages ? `(${meta.total_messages})` : ''}
          </span>
        )}
      </div>
      
      <div className="header-actions" style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
        {/* LIVE CONTINUOUS LEARNING ENGINE INDICATOR */}
        <div style={{ background: '#25D36615', border: '1px solid #25D36640', padding: '5px 12px', borderRadius: '16px', fontSize: '11px', fontWeight: '700', color: '#128C7E', display: 'flex', alignItems: 'center', gap: '6px' }}>
          <Cpu size={14} color="#25D366" className="animate-pulse" />
          <span>🟢 Learning Engine: Active ({savedSessions.length} Chats Ingested)</span>
        </div>

        {/* MASTER SESSIONS SELECTOR DROPDOWN */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px', background: 'var(--bg-main)', padding: '4px 10px', borderRadius: '16px', border: '1px solid var(--border)' }}>
          <Folder size={14} color="var(--primary-dark)" />
          <select 
            value={activeChatId} 
            onChange={handleSelectSession}
            style={{ background: 'transparent', border: 'none', fontSize: '12px', fontWeight: '600', color: 'var(--text-primary)', cursor: 'pointer', outline: 'none' }}
          >
            <option value="all">🌐 All Chats (Master Memory)</option>
            {savedSessions.map((s) => (
              <option key={s.chat_id} value={s.chat_id}>
                📄 {s.filename} ({s.total_messages} msgs)
              </option>
            ))}
            <option value="new">+ Upload New Chat</option>
          </select>

          {/* DELETE BUTTON */}
          {savedSessions.length > 0 && (
            <button 
              onClick={handleDeleteActiveChat}
              title="Delete selected chat file from memory"
              style={{ background: 'none', border: 'none', cursor: 'pointer', color: '#EF5350', padding: '2px 4px', display: 'flex', alignItems: 'center' }}
            >
              <Trash2 size={14} />
            </button>
          )}
        </div>

        {/* 1-CLICK EXECUTIVE REPORT EXPORT BUTTON */}
        <button 
          onClick={handleExportReport}
          title="Printable Executive PDF/HTML Report"
          style={{ 
            background: 'var(--primary-darker)', 
            color: 'white', 
            border: 'none', 
            padding: '8px 14px', 
            borderRadius: '20px', 
            fontSize: '12px', 
            fontWeight: '700', 
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '6px'
          }}
        >
          <FileText size={15} />
          <span>Export Report</span>
        </button>

        <button 
          onClick={() => {
            localStorage.removeItem('activeChatId');
            localStorage.removeItem('chatMetadata');
            navigate('/');
            window.location.reload();
          }}
          style={{ 
            background: 'var(--primary)', 
            color: 'white', 
            border: 'none', 
            padding: '8px 14px', 
            borderRadius: '20px', 
            fontSize: '12px', 
            fontWeight: '700', 
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '6px'
          }}
        >
          <UploadCloud size={15} />
          <span>Upload File</span>
        </button>

        <div className="avatar" id="user-avatar">
          <User size={20} />
        </div>
      </div>
    </header>
  );
}
