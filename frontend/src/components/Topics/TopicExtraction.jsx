import React, { useState, useEffect } from 'react';
import { Tag, Hash, Sparkles, UploadCloud } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { getTopics } from '../../utils/api';
import './Topics.css';

const TopicExtraction = () => {
  const [topics, setTopics] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();
  const activeChatId = localStorage.getItem('activeChatId');

  useEffect(() => {
    async function loadData() {
      if (!activeChatId) {
        setLoading(false);
        return;
      }
      try {
        const data = await getTopics();
        setTopics(data?.topics || []);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, [activeChatId]);

  const getCategoryBadge = (category) => {
    switch (category?.toLowerCase()) {
      case 'health':
        return { emoji: '🏥', label: 'Health & Wellness', color: '#EF5350' };
      case 'training':
        return { emoji: '📚', label: 'Training & Skills', color: '#0091EA' };
      case 'project':
        return { emoji: '🏗️', label: 'Project Progress', color: '#FF6D00' };
      case 'operations':
        return { emoji: '⚙️', label: 'Operations & Logistics', color: '#7C4DFF' };
      case 'finance':
        return { emoji: '💰', label: 'Finance & Budget', color: '#25D366' };
      default:
        return { emoji: '💬', label: 'General Discussion', color: '#667781' };
    }
  };

  if (!activeChatId && !loading) {
    return (
      <div style={{ textAlign: 'center', padding: '60px 20px' }}>
        <div style={{ background: 'white', border: '1px solid var(--border)', borderRadius: '24px', padding: '48px 32px', maxWidth: '540px', margin: '0 auto' }}>
          <UploadCloud size={56} style={{ color: 'var(--primary)', marginBottom: '16px' }} />
          <h2 style={{ fontSize: '20px', fontWeight: '700', marginBottom: '8px' }}>No Chat Uploaded Yet</h2>
          <p style={{ color: 'var(--text-secondary)', fontSize: '14px', marginBottom: '24px' }}>Please upload a WhatsApp chat export file (.txt) to view topic extraction.</p>
          <button onClick={() => navigate('/')} style={{ background: 'var(--primary)', color: 'white', border: 'none', padding: '12px 28px', borderRadius: '24px', fontWeight: '700', cursor: 'pointer' }}>Upload WhatsApp Chat</button>
        </div>
      </div>
    );
  }

  return (
    <div className="topics-container animate-fade-in">
      <div className="topics-header">
        <h2><Tag size={24} className="title-icon" /> AI Topic Extraction &amp; Categorization</h2>
        <p className="subtitle">Automatically identified discussion themes, domain insights, and category breakdown</p>
      </div>

      {loading ? (
        <div className="loading-state">Extracting topics with AI...</div>
      ) : topics.length === 0 ? (
        <div style={{ padding: '30px', textAlign: 'center', color: 'var(--text-secondary)' }}>No topics extracted for this chat session yet.</div>
      ) : (
        <div className="topics-grid">
          {topics.map((topic, idx) => {
            const badge = getCategoryBadge(topic.category);
            return (
              <div key={idx} className="topic-card">
                <div className="topic-card-header">
                  <span className="category-pill" style={{ borderColor: badge.color, color: badge.color }}>
                    {badge.emoji} {badge.label}
                  </span>
                  <span className="topic-count"><Hash size={14} /> {topic.count} msgs</span>
                </div>

                <h3 className="topic-name">{topic.name}</h3>
                <p className="topic-desc">{topic.description}</p>

                <div className="topic-footer">
                  <Sparkles size={14} className="ai-sparkle" />
                  <span>AI Insight Extracted</span>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default TopicExtraction;
