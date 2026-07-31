import React, { useState, useEffect } from 'react';
import { MessageCircle, Users, Calendar, BarChart2, Sparkles, Heart, Activity, ArrowRight, UploadCloud } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import StatCard from './StatCard';
import { getCommunicationStats, getSentimentStats, getSummary, loadDemoChatSession } from '../../utils/api';
import './Dashboard.css';

export default function DashboardOverview() {
  const navigate = useNavigate();
  const [commStats, setCommStats] = useState(null);
  const [sentimentStats, setSentimentStats] = useState(null);
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);

  const activeChatId = localStorage.getItem('activeChatId') || 'all';

  useEffect(() => {
    async function loadDashboardData() {
      try {
        const comm = await getCommunicationStats(activeChatId);
        const sent = await getSentimentStats(activeChatId);
        const sum = await getSummary(activeChatId, 'bullet');
        setCommStats(comm);
        setSentimentStats(sent);
        setSummary(sum);
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    }
    loadDashboardData();
  }, [activeChatId]);

  const handleTrySample = async () => {
    setLoading(true);
    try {
      await loadDemoChatSession();
      window.location.reload();
    } catch (e) {
      console.error(e);
      setLoading(false);
    }
  };

  const totalMsgs = commStats?.messages_per_participant 
    ? Object.values(commStats.messages_per_participant).reduce((a, b) => a + b, 0) 
    : 0;

  const participantsCount = commStats?.messages_per_participant 
    ? Object.keys(commStats.messages_per_participant).length 
    : 0;

  return (
    <div className="dashboard-container animate-fade-in" id="dashboard-overview">
      <div className="dashboard-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '12px' }}>
        <div>
          <h2>Executive Overview Dashboard</h2>
          <p className="subtitle">
            {activeChatId === 'all' ? '🌐 Master Organization Memory View (Combined Across All Chats)' : 'High-level communication health, sentiment snapshot, and AI summary'}
          </p>
        </div>
        <button 
          onClick={() => navigate('/summaries')}
          className="btn"
          style={{ 
            background: 'var(--primary)', 
            color: 'white', 
            border: 'none', 
            padding: '10px 18px', 
            borderRadius: '20px', 
            fontWeight: '600', 
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '6px'
          }}
        >
          <Sparkles size={16} />
          <span>Ask AI Questions</span>
        </button>
      </div>

      {/* STAT CARDS ROW */}
      <div className="stats-grid">
        <StatCard 
          title="Total Messages" 
          value={totalMsgs.toLocaleString()} 
          icon={MessageCircle} 
          trend="+100%" 
          trendUp={true} 
          color="primary"
          delay="0.1s"
        />
        <StatCard 
          title="Participants" 
          value={participantsCount.toString()} 
          icon={Users} 
          trend="Active" 
          trendUp={true} 
          color="blue"
          delay="0.2s"
        />
        <StatCard 
          title="Top Participant" 
          value={commStats?.most_active_participant || 'N/A'} 
          icon={Activity} 
          color="purple"
          delay="0.3s"
        />
        <StatCard 
          title="Peak Hour" 
          value={commStats?.peak_hours?.length ? `${commStats.peak_hours[0]}:00` : 'N/A'} 
          icon={BarChart2} 
          color="orange"
          delay="0.4s"
        />
      </div>

      {/* DASHBOARD CONTENT GRID */}
      <div className="dashboard-content-grid">
        
        {/* LEFT COLUMN: AI SUMMARY SNAPSHOT */}
        <div className="card animate-slide-up" style={{ padding: '20px', background: 'white', borderRadius: '16px', border: '1px solid var(--border)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px', flexWrap: 'wrap', gap: '8px' }}>
            <h3 style={{ fontSize: '16px', fontWeight: '700', color: 'var(--primary-darker)', display: 'flex', alignItems: 'center', gap: '8px', margin: 0 }}>
              <Sparkles size={18} color="var(--primary)" />
              AI Executive Summary
            </h3>
            <button 
              onClick={() => navigate('/summaries')} 
              style={{ background: 'none', border: 'none', color: 'var(--primary-dark)', fontWeight: '600', cursor: 'pointer', fontSize: '13px', display: 'flex', alignItems: 'center', gap: '4px' }}
            >
              View Full Summary <ArrowRight size={14} />
            </button>
          </div>

          <div style={{ background: 'var(--bg-main)', padding: '16px', borderRadius: '12px', marginBottom: '16px', fontSize: '14px', lineHeight: '1.6' }}>
            {summary?.summary_text ? (
              summary.summary_text.split('\n').map((line, idx) => {
                if (line.startsWith('###')) return <h4 key={idx} style={{ margin: '8px 0', color: 'var(--primary-darker)' }}>{line.replace('### ', '')}</h4>;
                if (line.startsWith('- **') || line.startsWith('**')) return <p key={idx} style={{ margin: '4px 0', fontWeight: '600' }}>{line}</p>;
                return <p key={idx} style={{ margin: '4px 0' }}>{line}</p>;
              })
            ) : (
              <p style={{ margin: 0, color: 'var(--text-secondary)' }}>Generating ChatLens AI summary...</p>
            )}
          </div>

          <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
            <button 
              onClick={() => navigate('/analytics')} 
              style={{ flex: 1, minWidth: '130px', padding: '10px', borderRadius: '10px', border: '1px solid var(--border)', background: 'white', fontWeight: '600', cursor: 'pointer' }}
            >
              📊 View Analytics
            </button>
            <button 
              onClick={() => navigate('/actions')} 
              style={{ flex: 1, minWidth: '130px', padding: '10px', borderRadius: '10px', border: '1px solid var(--border)', background: 'white', fontWeight: '600', cursor: 'pointer' }}
            >
              ⚠️ Action Tracker
            </button>
          </div>
        </div>

        {/* RIGHT COLUMN: SENTIMENT SNAPSHOT */}
        <div className="card animate-slide-up" style={{ padding: '20px', background: 'white', borderRadius: '16px', border: '1px solid var(--border)' }}>
          <h3 style={{ fontSize: '16px', fontWeight: '700', color: 'var(--primary-darker)', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px', margin: 0 }}>
            <Heart size={18} color="#EF5350" />
            Sentiment Breakdown
          </h3>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span style={{ fontSize: '14px' }}>🟢 Positive Messages</span>
              <strong style={{ color: '#25D366' }}>{sentimentStats?.overall_sentiment?.positive || 0}</strong>
            </div>
            <div style={{ background: '#E0E0E0', height: '8px', borderRadius: '4px', overflow: 'hidden' }}>
              <div style={{ width: `${Math.min(100, (sentimentStats?.overall_sentiment?.positive || 0) * 10)}%`, background: '#25D366', height: '100%' }}></div>
            </div>

            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '8px' }}>
              <span style={{ fontSize: '14px' }}>⚪ Neutral Messages</span>
              <strong style={{ color: '#667781' }}>{sentimentStats?.overall_sentiment?.neutral || 0}</strong>
            </div>
            <div style={{ background: '#E0E0E0', height: '8px', borderRadius: '4px', overflow: 'hidden' }}>
              <div style={{ width: `${Math.min(100, (sentimentStats?.overall_sentiment?.neutral || 0) * 10)}%`, background: '#667781', height: '100%' }}></div>
            </div>

            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '8px' }}>
              <span style={{ fontSize: '14px' }}>🔴 Negative / Stress</span>
              <strong style={{ color: '#EF5350' }}>{sentimentStats?.overall_sentiment?.negative || 0}</strong>
            </div>
            <div style={{ background: '#E0E0E0', height: '8px', borderRadius: '4px', overflow: 'hidden' }}>
              <div style={{ width: `${Math.min(100, (sentimentStats?.overall_sentiment?.negative || 0) * 10)}%`, background: '#EF5350', height: '100%' }}></div>
            </div>

            <button 
              onClick={() => navigate('/sentiment')} 
              style={{ marginTop: '12px', background: 'var(--bg-main)', border: 'none', padding: '8px', borderRadius: '8px', fontWeight: '600', cursor: 'pointer', color: 'var(--primary-darker)' }}
            >
              Explore Full Mood Trends →
            </button>
          </div>
        </div>

      </div>
    </div>
  );
}
