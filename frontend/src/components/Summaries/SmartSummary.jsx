import React, { useState } from 'react';
import { getSummary } from '../../utils/api';
import './Summaries.css';

const modes = [
  { id: 'bullet', icon: '📋', label: 'Bullet Points' },
  { id: 'story', icon: '📖', label: 'Story Mode' },
  { id: 'timeline', icon: '📅', label: 'Project Timeline' },
  { id: 'pending', icon: '⚠️', label: 'Pending Items' },
];

const SmartSummary = () => {
  const [activeMode, setActiveMode] = useState(modes[0].id);
  const [loading, setLoading] = useState(false);
  const [summaryData, setSummaryData] = useState(null);
  const activeChatId = localStorage.getItem('activeChatId');

  const handleGenerate = async () => {
    if (!activeChatId) {
      alert('Please upload a WhatsApp chat file (.txt) first!');
      return;
    }
    setLoading(true);
    try {
      const data = await getSummary(activeChatId, activeMode);
      setSummaryData(data);
    } catch (error) {
      console.error('Failed to generate summary', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = () => {
    if (summaryData?.summary_text) {
      navigator.clipboard.writeText(summaryData.summary_text);
      alert('Copied to clipboard!');
    }
  };

  const handleExport = () => {
    if (summaryData?.summary_text) {
      const blob = new Blob([summaryData.summary_text], { type: 'text/plain' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `summary-${activeMode}.txt`;
      a.click();
      URL.revokeObjectURL(url);
    }
  };

  const textToRender = summaryData?.summary_text || null;

  return (
    <div className="summary-card">
      <div className="summary-header">
        <h2 className="summary-title">Smart Summaries</h2>
        <div className="mode-selector">
          {modes.map((mode) => (
            <button
              key={mode.id}
              className={`mode-btn ${activeMode === mode.id ? 'active' : ''}`}
              onClick={() => setActiveMode(mode.id)}
            >
              <span>{mode.icon}</span> {mode.label}
            </button>
          ))}
        </div>
        <button 
          className="generate-btn" 
          onClick={handleGenerate}
          disabled={loading}
        >
          {loading ? 'Generating Summary...' : 'Generate Summary'}
        </button>
      </div>

      <div className="summary-result">
        {textToRender ? (
          <>
            <div className="summary-output">
              {textToRender.split('\n').map((line, i) => {
                if (line.startsWith('###')) return <h3 key={i} style={{ marginTop: '12px', color: 'var(--primary-darker)' }}>{line.replace('### ', '')}</h3>;
                if (line.startsWith('- **') || line.startsWith('**')) return <p key={i} style={{ margin: '8px 0', fontWeight: '600' }}>{line}</p>;
                return <p key={i} style={{ margin: '6px 0' }}>{line}</p>;
              })}
            </div>
            <div className="summary-actions" style={{ marginTop: '16px', display: 'flex', gap: '12px' }}>
              <button className="action-btn" onClick={handleCopy}>Copy to Clipboard</button>
              <button className="action-btn" onClick={handleExport}>Export TXT</button>
            </div>
          </>
        ) : (
          <div style={{ padding: '30px', textAlign: 'center', color: 'var(--text-secondary)' }}>
            Select a mode above and click <strong>Generate Summary</strong> to summarize your uploaded chat file.
          </div>
        )}
      </div>
    </div>
  );
};

export default SmartSummary;
