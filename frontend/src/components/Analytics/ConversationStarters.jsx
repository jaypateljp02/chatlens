import React from 'react';
import './Analytics.css';

const ConversationStarters = ({ starters }) => {
  if (!starters) return null;

  return (
    <div className="analytics-card">
      <h3 className="analytics-card-title">Conversation Starters</h3>
      <div className="starters-list">
        {starters.map((starter, index) => (
          <div key={index} className="starter-item">
            <div className="starter-info">
              <span className="starter-name">{starter.name}</span>
              <span className="starter-count">{starter.count} times</span>
            </div>
            <div className="starter-bar-container">
              <div 
                className="starter-bar" 
                style={{ width: `${starter.percentage}%`, backgroundColor: index === 0 ? 'var(--primary)' : 'var(--accent-blue)' }}
              ></div>
            </div>
            <span className="starter-percentage">{starter.percentage}%</span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ConversationStarters;
