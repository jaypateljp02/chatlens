import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceArea } from 'recharts';
import './Sentiment.css';

const MoodTrends = ({ data = [] }) => {
  const chartData = (data || []).map(item => ({
    date: item.week,
    sentiment: Math.round(item.avg_sentiment * 100)
  }));

  return (
    <div className="card sentiment-card">
      <h3 className="card-title">Mood Trends (Over Time)</h3>
      <div className="chart-container" style={{ height: 260 }}>
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="var(--border)" />
            <XAxis dataKey="date" stroke="var(--text-secondary)" />
            <YAxis domain={[-100, 100]} stroke="var(--text-secondary)" />
            <Tooltip contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }} />
            <ReferenceArea y1={0} y2={100} fill="var(--primary)" fillOpacity={0.05} />
            <ReferenceArea y1={-100} y2={0} fill="var(--accent-red)" fillOpacity={0.05} />
            <Line 
              type="monotone" 
              dataKey="sentiment" 
              stroke="var(--primary-dark)" 
              strokeWidth={3}
              dot={{ r: 4, strokeWidth: 2, fill: 'var(--bg-white)' }}
              activeDot={{ r: 6, stroke: 'var(--primary)', strokeWidth: 2 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default MoodTrends;
