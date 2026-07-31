import React from 'react';
import './Analytics.css';

const WordCloud = ({ words }) => {
  if (!words) return null;
  
  return (
    <div className="analytics-card">
      <h3 className="analytics-card-title">Top Used Words</h3>
      <div className="word-cloud-container">
        {words.map((word, index) => (
          <span
            key={index}
            className="word-pill"
            style={{
              fontSize: `${Math.max(0.8, Math.min(2, word.value / 50))}rem`,
              opacity: Math.max(0.6, Math.min(1, word.value / 100)),
              padding: '4px 12px',
              margin: '4px',
              backgroundColor: `rgba(37, 211, 102, ${Math.min(0.8, word.value / 300)})`,
              color: word.value > 150 ? '#fff' : 'var(--text-primary)',
            }}
          >
            {word.text}
          </span>
        ))}
      </div>
    </div>
  );
};

export default WordCloud;
