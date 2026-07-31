import React, { useState, useEffect } from 'react';
import { Calendar, Flag, UploadCloud } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { getTimeline } from '../../utils/api';
import PeriodComparison from './PeriodComparison';
import './Timeline.css';

const TimelineView = () => {
  const [events, setEvents] = useState([]);
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
        const data = await getTimeline();
        setEvents(data?.events || []);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, [activeChatId]);

  if (!activeChatId && !loading) {
    return (
      <div style={{ textAlign: 'center', padding: '60px 20px' }}>
        <div style={{ background: 'white', border: '1px solid var(--border)', borderRadius: '24px', padding: '48px 32px', maxWidth: '540px', margin: '0 auto' }}>
          <UploadCloud size={56} style={{ color: 'var(--primary)', marginBottom: '16px' }} />
          <h2 style={{ fontSize: '20px', fontWeight: '700', marginBottom: '8px' }}>No Chat Uploaded Yet</h2>
          <p style={{ color: 'var(--text-secondary)', fontSize: '14px', marginBottom: '24px' }}>Please upload a WhatsApp chat export file (.txt) to view timeline events &amp; period comparison.</p>
          <button onClick={() => navigate('/')} style={{ background: 'var(--primary)', color: 'white', border: 'none', padding: '12px 28px', borderRadius: '24px', fontWeight: '700', cursor: 'pointer' }}>Upload WhatsApp Chat</button>
        </div>
      </div>
    );
  }

  return (
    <div className="timeline-container animate-fade-in">
      <div className="timeline-header">
        <h2><Calendar size={24} className="title-icon" /> Chat Timeline &amp; Milestones</h2>
        <p className="subtitle">Key activity peaks, media bursts, and critical conversation events over time</p>
      </div>

      <PeriodComparison />

      <h3 className="section-title"><Flag size={18} /> Major Milestones Timeline</h3>

      {loading ? (
        <div className="loading-state">Extracting milestone timeline...</div>
      ) : events.length === 0 ? (
        <div style={{ padding: '30px', textAlign: 'center', color: 'var(--text-secondary)' }}>No timeline milestone events extracted for this chat.</div>
      ) : (
        <div className="vertical-timeline">
          {events.map((event, idx) => (
            <div key={idx} className={`timeline-item ${event.type}`}>
              <div className="timeline-badge">
                <span>{event.icon}</span>
              </div>
              <div className="timeline-card">
                <span className="timeline-date">{new Date(event.date).toLocaleDateString()}</span>
                <h4 className="timeline-title">{event.title}</h4>
                <p className="timeline-desc">{event.description}</p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default TimelineView;
