import React from 'react';
import { TrendingUp, TrendingDown } from 'lucide-react';
import './Dashboard.css';

export default function StatCard({ title, value, icon: Icon, trend, trendUp, color = 'primary', delay = '0s' }) {
  
  const getColorVar = () => {
    switch(color) {
      case 'primary': return 'var(--primary)';
      case 'blue': return 'var(--accent-blue)';
      case 'purple': return 'var(--accent-purple)';
      case 'orange': return 'var(--accent-orange)';
      case 'red': return 'var(--accent-red)';
      default: return 'var(--primary)';
    }
  };

  const bgStyle = {
    background: `linear-gradient(135deg, ${getColorVar()} 0%, transparent 0%)`,
    borderTop: `4px solid ${getColorVar()}`
  };

  return (
    <div className="stat-card card animate-slide-up" style={{ animationDelay: delay, ...bgStyle }}>
      <div className="stat-card-header">
        <div className="stat-icon-wrapper" style={{ backgroundColor: `${getColorVar()}20`, color: getColorVar() }}>
          <Icon size={24} />
        </div>
        {trend && (
          <div className={`stat-trend ${trendUp ? 'trend-up' : 'trend-down'}`}>
            {trendUp ? <TrendingUp size={16} /> : <TrendingDown size={16} />}
            <span>{trend}</span>
          </div>
        )}
      </div>
      <div className="stat-card-body">
        <h4 className="stat-title">{title}</h4>
        <div className="stat-value">{value}</div>
      </div>
    </div>
  );
}
