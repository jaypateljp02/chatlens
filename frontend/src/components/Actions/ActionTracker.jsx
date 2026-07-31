import React, { useState, useEffect } from 'react';
import { CheckCircle2, Clock, AlertCircle, Check } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { getActionItems, completeActionItem } from '../../utils/api';
import './Actions.css';

const ActionTracker = () => {
  const [actions, setActions] = useState([]);
  const [filter, setFilter] = useState('all');
  const [loading, setLoading] = useState(true);
  const [completingPromise, setCompletingPromise] = useState(null);
  const navigate = useNavigate();
  const activeChatId = localStorage.getItem('activeChatId') || 'all';

  const loadData = async () => {
    try {
      const data = await getActionItems();
      setActions(data?.action_items || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [activeChatId]);

  const handleMarkComplete = async (promiseText) => {
    setCompletingPromise(promiseText);
    try {
      await completeActionItem(promiseText);
      await loadData();
    } catch (e) {
      alert('Failed to mark item complete.');
    } finally {
      setCompletingPromise(null);
    }
  };

  const filteredActions = actions.filter(item => {
    if (filter === 'pending') return item.status === 'pending';
    if (filter === 'completed') return item.status === 'completed';
    return true;
  });

  return (
    <div className="actions-container animate-fade-in">
      <div className="actions-header">
        <div>
          <h2><AlertCircle size={24} className="title-icon" /> Action Items &amp; Commitments</h2>
          <p className="subtitle">
            {activeChatId === 'all' ? '🌐 Showing all action items across Master Memory' : 'Showing action items for selected chat'}
          </p>
        </div>

        <div className="filter-tabs">
          <button 
            className={filter === 'all' ? 'active' : ''} 
            onClick={() => setFilter('all')}
          >
            All Messaging ({actions.length})
          </button>
          <button 
            className={filter === 'pending' ? 'active' : ''} 
            onClick={() => setFilter('pending')}
          >
            Pending ({actions.filter(a => a.status === 'pending').length})
          </button>
          <button 
            className={filter === 'completed' ? 'active' : ''} 
            onClick={() => setFilter('completed')}
          >
            Completed ({actions.filter(a => a.status === 'completed').length})
          </button>
        </div>
      </div>

      {loading ? (
        <div className="loading-state">Detecting action items...</div>
      ) : actions.length === 0 ? (
        <div style={{ padding: '30px', textAlign: 'center', color: 'var(--text-secondary)' }}>
          No commitment statements or action items detected in this chat session.
        </div>
      ) : (
        <div className="actions-list">
          {filteredActions.map((item, idx) => (
            <div key={idx} className={`action-card ${item.status}`} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div style={{ display: 'flex', gap: '14px', alignItems: 'flex-start', flex: 1 }}>
                <div className="action-status-icon">
                  {item.status === 'completed' ? (
                    <CheckCircle2 size={22} className="icon-done" color="#25D366" />
                  ) : (
                    <Clock size={22} className="icon-pending" color="#FFA726" />
                  )}
                </div>

                <div className="action-details">
                  <p className="action-promise">"{item.promise}"</p>
                  <div className="action-meta">
                    <span className="action-assignee">Assigned: <strong>{item.assignee}</strong></span>
                    <span className="action-date">{new Date(item.detected_date).toLocaleDateString()}</span>
                    <span className={`status-badge ${item.status}`} style={{ background: item.status === 'completed' ? '#25D36620' : '#FFA72620', color: item.status === 'completed' ? '#25D366' : '#E65100', padding: '3px 10px', borderRadius: '12px', fontSize: '11px', fontWeight: '700' }}>
                      {item.status === 'completed' ? '✓ Completed' : '⏳ Pending'}
                    </span>
                  </div>
                </div>
              </div>

              {item.status === 'pending' && (
                <button
                  onClick={() => handleMarkComplete(item.promise)}
                  disabled={completingPromise === item.promise}
                  style={{
                    background: '#25D366',
                    color: 'white',
                    border: 'none',
                    padding: '8px 14px',
                    borderRadius: '16px',
                    fontSize: '12px',
                    fontWeight: '700',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '4px',
                    marginLeft: '16px',
                    flexShrink: 0
                  }}
                >
                  <Check size={14} />
                  <span>{completingPromise === item.promise ? 'Updating...' : 'Mark Complete'}</span>
                </button>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default ActionTracker;
