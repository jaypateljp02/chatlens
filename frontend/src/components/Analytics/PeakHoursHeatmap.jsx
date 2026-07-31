import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import './Analytics.css';

const PeakHoursHeatmap = ({ data = [] }) => {
  const maxCount = Math.max(...(data || []).map(d => d.count || 0), 1);

  return (
    <div className="analytics-card">
      <h3 className="analytics-card-title">Peak Hours Activity (24-Hour Heatmap)</h3>
      <div className="chart-container">
        <ResponsiveContainer width="100%" height={250}>
          <BarChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
            <XAxis dataKey="hour" tick={{ fontSize: 11, fill: 'var(--text-secondary)' }} tickLine={false} axisLine={false} />
            <YAxis tick={{ fontSize: 11, fill: 'var(--text-secondary)' }} tickLine={false} axisLine={false} />
            <Tooltip
              cursor={{ fill: 'var(--bg-chat)' }}
              contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }}
            />
            <Bar dataKey="count" radius={[4, 4, 0, 0]}>
              {(data || []).map((entry, index) => {
                const opacity = entry.count === 0 ? 0.15 : 0.35 + (entry.count / maxCount) * 0.65;
                const isPeak = entry.count === maxCount && maxCount > 0;
                return (
                  <Cell 
                    key={`cell-${index}`} 
                    fill={isPeak ? '#25D366' : '#128C7E'} 
                    fillOpacity={opacity} 
                  />
                );
              })}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default PeakHoursHeatmap;
