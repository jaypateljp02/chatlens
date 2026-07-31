import React from 'react';
import './Sentiment.css';

const StressLanguage = ({ data = {} }) => {
  const items = Object.entries(data || {}).map(([name, count]) => ({
    name,
    count,
    level: count >= 5 ? 'high' : count >= 2 ? 'medium' : 'low'
  }));

  return (
    <div className="card sentiment-card">
      <h3 className="card-title">Stress &amp; Anxiety Indicators</h3>
      <div className="stress-list">
        {items.length === 0 ? (
          <p style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>No high stress language indicators detected.</p>
        ) : (
          items.map((person, index) => (
            <div key={index} className="stress-item">
              <div className="stress-header">
                <span className="person-name">{person.name}</span>
                <span className={`alert-badge ${person.level}`}>
                  {person.level === 'high' ? '⚠️ High' : person.level === 'medium' ? '⚠️ Medium' : '✅ Low'}
                </span>
              </div>
              <div className="stress-phrases">
                <span className="phrase-tag">{person.count} stress indicators detected</span>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default StressLanguage;
