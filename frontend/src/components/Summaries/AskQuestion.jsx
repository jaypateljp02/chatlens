import React, { useState } from 'react';
import { askQuestion } from '../../utils/api';
import './Summaries.css';

const suggestedQuestions = [
  "What were the main topics discussed?",
  "What tasks are pending?",
  "Who participated most in this conversation?",
  "Were there any urgent issues or deadlines?"
];

const AskQuestion = () => {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const activeChatId = localStorage.getItem('activeChatId');

  const handleAsk = async (q = query) => {
    if (!activeChatId) {
      alert('Please upload a WhatsApp chat file (.txt) first!');
      return;
    }
    if (!q.trim()) return;
    setQuery(q);
    setLoading(true);
    setResult(null);
    try {
      const data = await askQuestion(activeChatId, q);
      setResult(data);
    } catch (error) {
      console.error('Failed to ask question', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="ask-card" style={{ marginTop: '24px' }}>
      <h2 className="summary-title">Ask a Question</h2>
      
      <div className="suggested-chips" style={{ display: 'flex', gap: '8px', flexWrap: 'wrap', margin: '12px 0' }}>
        {suggestedQuestions.map((sq, i) => (
          <div 
            key={i} 
            className="chip" 
            onClick={() => handleAsk(sq)}
            style={{ 
              background: 'var(--bg-main)', 
              padding: '6px 14px', 
              borderRadius: '16px', 
              fontSize: '13px', 
              cursor: 'pointer',
              border: '1px solid var(--border)'
            }}
          >
            💬 {sq}
          </div>
        ))}
      </div>

      <div className="ask-input-group" style={{ display: 'flex', gap: '12px', marginTop: '12px' }}>
        <input 
          type="text" 
          className="ask-input" 
          placeholder="Ask anything about your uploaded chat..." 
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleAsk()}
          style={{ flex: 1, padding: '10px 16px', borderRadius: '20px', border: '1px solid var(--border)', fontSize: '14px' }}
        />
        <button 
          className="generate-btn" 
          onClick={() => handleAsk()}
          disabled={loading || !query.trim()}
          style={{ padding: '10px 20px', borderRadius: '20px', background: 'var(--primary)', color: 'white', border: 'none', fontWeight: '700', cursor: 'pointer' }}
        >
          {loading ? 'Thinking...' : 'Ask AI'}
        </button>
      </div>

      {result && (
        <div className="answer-card" style={{ marginTop: '16px', background: 'var(--bg-main)', padding: '16px', borderRadius: '12px' }}>
          <div className="answer-text" style={{ fontSize: '14px', lineHeight: '1.6', marginBottom: '12px' }}>
            {result.answer}
          </div>
          
          {result.source_messages && result.source_messages.length > 0 && (
            <div className="quotes-section">
              <h4 style={{ margin: '8px 0', fontSize: '13px', color: 'var(--text-secondary)' }}>Source References:</h4>
              {result.source_messages.map((quote, i) => (
                <div key={i} className="quote-card" style={{ fontSize: '12px', background: 'white', padding: '8px 12px', borderRadius: '8px', marginBottom: '6px', borderLeft: '3px solid var(--primary)' }}>
                  {quote}
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default AskQuestion;
