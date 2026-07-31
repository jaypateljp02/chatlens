import React, { useState, useEffect } from 'react';
import MoodTrends from './MoodTrends';
import StressLanguage from './StressLanguage';
import ConflictTimeline from './ConflictTimeline';
import GratitudeTrends from './GratitudeTrends';
import { getSentimentStats } from '../../utils/api';
import { useNavigate } from 'react-router-dom';
import { UploadCloud } from 'lucide-react';
import './Sentiment.css';

const SentimentDashboard = () => {
  const [data, setData] = useState(null);
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
        const res = await getSentimentStats();
        setData(res);
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
          <p style={{ color: 'var(--text-secondary)', fontSize: '14px', marginBottom: '24px' }}>Please upload a WhatsApp chat export file (.txt) to view sentiment &amp; stress analytics.</p>
          <button onClick={() => navigate('/')} style={{ background: 'var(--primary)', color: 'white', border: 'none', padding: '12px 28px', borderRadius: '24px', fontWeight: '700', cursor: 'pointer' }}>Upload WhatsApp Chat</button>
        </div>
      </div>
    );
  }

  if (loading) return <div className="loading-spinner" style={{ padding: '40px', textAlign: 'center' }}>Loading sentiment analysis...</div>;

  return (
    <div className="sentiment-dashboard fade-in">
      <div className="page-header" style={{ marginBottom: '24px' }}>
        <h2 className="page-title">Sentiment &amp; Emotion Analytics</h2>
        <p className="page-subtitle">Understand emotional dynamics, stress indicators, and tone trends in your conversations.</p>
      </div>
      
      <div className="dashboard-grid">
        <MoodTrends data={data?.mood_trends} />
        <GratitudeTrends data={data?.gratitude_per_person} />
        <StressLanguage data={data?.stress_per_person} />
        <ConflictTimeline data={data?.conflict_periods} />
      </div>
    </div>
  );
};

export default SentimentDashboard;
