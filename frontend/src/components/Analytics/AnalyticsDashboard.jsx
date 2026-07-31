import React, { useState, useEffect } from 'react';
import { getCommunicationStats } from '../../utils/api';
import PeakHoursHeatmap from './PeakHoursHeatmap';
import ActiveDaysChart from './ActiveDaysChart';
import MessageVolumeChart from './MessageVolumeChart';
import WordCloud from './WordCloud';
import ConversationStarters from './ConversationStarters';
import { useNavigate } from 'react-router-dom';
import { UploadCloud } from 'lucide-react';
import './Analytics.css';

const AnalyticsDashboard = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();
  const activeChatId = localStorage.getItem('activeChatId');

  useEffect(() => {
    const fetchStats = async () => {
      if (!activeChatId) {
        setLoading(false);
        return;
      }
      try {
        const data = await getCommunicationStats(activeChatId);
        setStats(data);
      } catch (error) {
        console.error("Failed to load stats", error);
      } finally {
        setLoading(false);
      }
    };
    fetchStats();
  }, [activeChatId]);

  if (!activeChatId && !loading) {
    return (
      <div style={{ textAlign: 'center', padding: '60px 20px' }}>
        <div style={{ background: 'white', border: '1px solid var(--border)', borderRadius: '24px', padding: '48px 32px', maxWidth: '540px', margin: '0 auto' }}>
          <UploadCloud size={56} style={{ color: 'var(--primary)', marginBottom: '16px' }} />
          <h2 style={{ fontSize: '20px', fontWeight: '700', marginBottom: '8px' }}>No Chat Uploaded Yet</h2>
          <p style={{ color: 'var(--text-secondary)', fontSize: '14px', marginBottom: '24px' }}>Please upload a WhatsApp chat export file (.txt) to view communication analytics.</p>
          <button onClick={() => navigate('/')} style={{ background: 'var(--primary)', color: 'white', border: 'none', padding: '12px 28px', borderRadius: '24px', fontWeight: '700', cursor: 'pointer' }}>Upload WhatsApp Chat</button>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="analytics-dashboard" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '300px' }}>
        <div style={{ color: 'var(--primary)', fontSize: '18px', fontWeight: '700' }}>Loading Analytics...</div>
      </div>
    );
  }

  // Generate complete 24-hour activity array
  const rawHours = stats?.messages_per_hour || {};
  const hourlyActivity = Array.from({ length: 24 }, (_, i) => {
    const key = i.toString();
    const count = rawHours[key] || rawHours[i] || 0;
    return {
      hour: `${i.toString().padStart(2, '0')}:00`,
      count: count
    };
  });

  // Days of week array
  const dayNames = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
  const rawDays = stats?.messages_per_day_of_week || {};
  const activeDays = dayNames.map(day => ({
    day: day.substring(0, 3),
    messages: rawDays[day] || 0
  }));

  // Message volume per participant
  const messageVolume = stats?.messages_per_participant
    ? Object.entries(stats.messages_per_participant).map(([sender, count]) => ({
        date: sender,
        count: count
      }))
    : [];

  // Top words cloud
  const topWords = stats?.word_frequencies
    ? Object.entries(stats.word_frequencies).flatMap(([sender, words]) =>
        Object.entries(words).slice(0, 5).map(([word, value]) => ({ text: `${word} (${sender})`, value: value * 15 }))
      )
    : [];

  // Conversation starters
  const totalStarters = stats?.conversation_starters 
    ? Object.values(stats.conversation_starters).reduce((a, b) => a + b, 0) || 1 
    : 1;

  const starters = stats?.conversation_starters
    ? Object.entries(stats.conversation_starters).map(([name, count]) => ({
        name,
        count,
        percentage: Math.round((count / totalStarters) * 100)
      }))
    : [];

  return (
    <div className="analytics-dashboard animate-fade-in">
      <div className="analytics-header" style={{ marginBottom: '24px' }}>
        <h2 className="analytics-title">Communication Analytics</h2>
        <p style={{ color: 'var(--text-secondary)', fontSize: '14px', margin: 0 }}>Detailed 24-hour heatmaps, activity distribution, and word frequency breakdown</p>
      </div>
      <div className="analytics-grid" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(350px, 1fr))', gap: '20px' }}>
        <MessageVolumeChart data={messageVolume} />
        <PeakHoursHeatmap data={hourlyActivity} />
        <ActiveDaysChart data={activeDays} />
        <WordCloud words={topWords} />
        <ConversationStarters starters={starters} />
      </div>
    </div>
  );
};

export default AnalyticsDashboard;
