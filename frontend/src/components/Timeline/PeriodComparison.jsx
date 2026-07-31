import React, { useState } from 'react';
import { ArrowRightLeft, TrendingUp, TrendingDown, Calendar } from 'lucide-react';
import { comparePeriods } from '../../utils/api';

const PeriodComparison = () => {
  const [p1Start, setP1Start] = useState('2026-01-01');
  const [p1End, setP1End] = useState('2026-03-31');
  const [p2Start, setP2Start] = useState('2026-04-01');
  const [p2End, setP2End] = useState('2026-06-30');

  const [comparison, setComparison] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleCompare = async () => {
    const activeChatId = localStorage.getItem('activeChatId');
    if (!activeChatId) {
      alert('Please upload a WhatsApp chat file (.txt) or click Try Sample Chat Demo first!');
      return;
    }
    setLoading(true);
    try {
      const data = await comparePeriods(activeChatId, p1Start, p1End, p2Start, p2End);
      setComparison(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="comparison-box">
      <div className="comparison-header">
        <h3><ArrowRightLeft size={18} /> Period Comparison Engine</h3>
        <p>Compare communication volume, sentiment shift, and participant activity across 2 time windows</p>
      </div>

      <div className="range-controls">
        <div className="range-group">
          <label>Period A Range:</label>
          <input type="date" value={p1Start} onChange={(e) => setP1Start(e.target.value)} />
          <span>to</span>
          <input type="date" value={p1End} onChange={(e) => setP1End(e.target.value)} />
        </div>

        <div className="range-group">
          <label>Period B Range:</label>
          <input type="date" value={p2Start} onChange={(e) => setP2Start(e.target.value)} />
          <span>to</span>
          <input type="date" value={p2End} onChange={(e) => setP2End(e.target.value)} />
        </div>

        <button className="compare-btn" onClick={handleCompare} disabled={loading}>
          {loading ? 'Comparing...' : 'Compare Periods'}
        </button>
      </div>

      {comparison && comparison.changes && (
        <div className="comparison-results">
          <div className="result-card">
            <h4>Message Volume Change</h4>
            <div className="metric-val">
              {comparison.changes.volume_change_percent >= 0 ? (
                <span className="positive"><TrendingUp size={20} /> +{comparison.changes.volume_change_percent}%</span>
              ) : (
                <span className="negative"><TrendingDown size={20} /> {comparison.changes.volume_change_percent}%</span>
              )}
            </div>
            <p className="sub-text">
              Period A: {comparison.period1?.message_count || 0} msgs → Period B: {comparison.period2?.message_count || 0} msgs
            </p>
          </div>

          <div className="result-card">
            <h4>Sentiment Shift</h4>
            <div className="metric-val">
              {comparison.changes.sentiment_change >= 0 ? (
                <span className="positive">+{comparison.changes.sentiment_change} score</span>
              ) : (
                <span className="negative">{comparison.changes.sentiment_change} score</span>
              )}
            </div>
            <p className="sub-text">
              Sentiment trend shifted from {comparison.period1?.avg_sentiment || 0} to {comparison.period2?.avg_sentiment || 0}
            </p>
          </div>

          <div className="result-card">
            <h4>Active Participants</h4>
            <div className="metric-val">
              <span>{comparison.period2?.participant_count || 0} people</span>
            </div>
            <p className="sub-text">
              {comparison.changes.new_participants?.length || 0} new participants joined in Period B
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

export default PeriodComparison;
