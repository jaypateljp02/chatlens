import React from 'react';
import './Sentiment.css';

const ConflictTimeline = ({ data = [] }) => {
  const events = data || [];

  return (
    <div className="card sentiment-card">
      <h3 className="card-title">Disagreement &amp; Conflict Timeline</h3>
      <div className="conflict-timeline">
        {events.length === 0 ? (
          <p style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>No major disagreement or conflict periods detected.</p>
        ) : (
          events.map((item, index) => (
            <div key={index} className="timeline-event">
              <div className="timeline-date">{new Date(item.start).toLocaleDateString()}</div>
              <div className="timeline-content">
                <div className="conflict-topic"><strong>Context:</strong> "{item.sample}"</div>
                <div className="conflict-parties"><strong>Between:</strong> {(item.participants || []).join(' & ')}</div>
                <div className="conflict-intensity">
                  <span>{item.messages_count} negative messages</span>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default ConflictTimeline;
