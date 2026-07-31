import React, { useState, useEffect } from 'react';
import { Share2, Network, Cpu, ShieldAlert, Sparkles, MessageCircle, Clock, Database } from 'lucide-react';
import { getKnowledgeGraph, getMemoryAlerts } from '../../utils/api';
import './KnowledgeGraph.css';

const KnowledgeGraphView = () => {
  const [graphData, setGraphData] = useState(null);
  const [alerts, setAlerts] = useState([]);
  const [selectedNode, setSelectedNode] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadGraphAndAlerts() {
      try {
        const [gData, aData] = await Promise.all([
          getKnowledgeGraph(),
          getMemoryAlerts()
        ]);
        setGraphData(gData);
        setAlerts(aData?.alerts || []);
        if (gData?.nodes?.length > 0) {
          setSelectedNode(gData.nodes[0]);
        }
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    loadGraphAndAlerts();
  }, []);

  const nodes = graphData?.nodes || [];
  const edges = graphData?.edges || [];

  return (
    <div className="kg-container animate-fade-in">
      <div className="kg-header">
        <div>
          <h2><Share2 size={24} className="title-icon" /> Knowledge Graph &amp; RAG Memory</h2>
          <p className="subtitle">Interconnected relationship network linking People ↔ Topics ↔ Group Conversations</p>
        </div>
        <div className="kg-badge">
          <Sparkles size={16} />
          <span>Continuous Learning Active</span>
        </div>
      </div>

      <div className="kg-content-grid">
        {/* GRAPH CANVAS WITH VISUAL NODE CONNECTORS */}
        <div className="graph-canvas-box">
          <div className="canvas-header">
            <span><Network size={16} /> Connected Entity Network ({nodes.length} Nodes, {edges.length} Connections)</span>
            <div className="legend">
              <span className="legend-item"><span className="dot group"></span> Group</span>
              <span className="legend-item"><span className="dot person"></span> Person</span>
              <span className="legend-item"><span className="dot topic"></span> Topic</span>
            </div>
          </div>

          {loading ? (
            <div style={{ padding: '60px', textAlign: 'center', color: 'var(--text-secondary)' }}>
              Building Knowledge Graph &amp; Relational Vectors...
            </div>
          ) : (
            <div className="visual-nodes-wrapper" style={{ position: 'relative', minHeight: '380px', display: 'flex', flexWrap: 'wrap', gap: '16px', padding: '24px', alignItems: 'center', justifyContent: 'center' }}>
              {nodes.map((node) => {
                const isSelected = selectedNode?.id === node.id;
                return (
                  <div 
                    key={node.id} 
                    className={`node-card ${node.type} ${isSelected ? 'selected' : ''}`}
                    style={{ 
                      borderColor: node.color || '#25D366',
                      transform: isSelected ? 'scale(1.06)' : 'scale(1)',
                      boxShadow: isSelected ? `0 8px 24px ${node.color || '#25D366'}40` : '0 4px 12px rgba(0,0,0,0.05)',
                      cursor: 'pointer',
                      transition: 'all 0.2s ease'
                    }}
                    onClick={() => setSelectedNode(node)}
                  >
                    <span className="node-type-label" style={{ background: node.color || '#25D366', color: 'white', padding: '2px 8px', borderRadius: '10px', fontSize: '10px', fontWeight: '700' }}>
                      {node.type.toUpperCase()}
                    </span>
                    <h4 className="node-name" style={{ marginTop: '8px', fontSize: '14px', fontWeight: '700' }}>{node.name}</h4>
                    {node.message_count > 0 && (
                      <span style={{ fontSize: '11px', color: 'var(--text-secondary)', display: 'block', marginTop: '4px' }}>
                        {node.message_count} msgs
                      </span>
                    )}
                  </div>
                );
              })}
            </div>
          )}
        </div>

        {/* NODE INTELLIGENCE INSPECTOR & VECTOR MEMORY DISPLAY */}
        <div className="node-details-box">
          <h3><Cpu size={18} /> Node Intelligence &amp; Vector Memory</h3>
          {selectedNode ? (
            <div className="details-card" style={{ background: 'white', border: '1px solid var(--border)', padding: '18px', borderRadius: '16px', marginBottom: '20px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                <span className="details-type" style={{ color: selectedNode.color || '#25D366', fontWeight: '800', fontSize: '11px', letterSpacing: '1px' }}>
                  {(selectedNode.type || 'node').toUpperCase()} ENTITY
                </span>
                {selectedNode.message_count > 0 && (
                  <span style={{ fontSize: '12px', background: 'var(--bg-main)', padding: '4px 10px', borderRadius: '12px', fontWeight: '600' }}>
                    <MessageCircle size={12} style={{ display: 'inline', marginRight: '4px' }} />
                    {selectedNode.message_count} messages
                  </span>
                )}
              </div>
              <h4 style={{ fontSize: '18px', fontWeight: '700', marginBottom: '6px' }}>{selectedNode.name}</h4>
              <p style={{ fontSize: '13px', color: 'var(--text-secondary)', lineHeight: '1.5', margin: '0 0 12px 0' }}>
                {selectedNode.details || `Mapped in local persistent vector memory.`}
              </p>
              
              {selectedNode.peak_hour && selectedNode.peak_hour !== 'N/A' && (
                <div style={{ fontSize: '12px', color: 'var(--primary-darker)', display: 'flex', alignItems: 'center', gap: '4px', fontWeight: '600', marginBottom: '12px' }}>
                  <Clock size={14} /> Peak Activity Time: {selectedNode.peak_hour}
                </div>
              )}

              {/* VECTOR MEMORY QUOTES INSPECTOR */}
              {selectedNode.sample_memory && (
                <div style={{ background: 'var(--bg-main)', padding: '12px', borderRadius: '10px', borderLeft: `3px solid ${selectedNode.color || '#25D366'}` }}>
                  <h5 style={{ margin: '0 0 6px 0', fontSize: '12px', color: 'var(--primary-darker)', display: 'flex', alignItems: 'center', gap: '4px' }}>
                    <Database size={12} /> Stored Vector Memory Chunks:
                  </h5>
                  <div style={{ fontSize: '12px', whiteSpace: 'pre-wrap', lineHeight: '1.5', color: 'var(--text-primary)' }}>
                    {selectedNode.sample_memory}
                  </div>
                </div>
              )}
            </div>
          ) : (
            <p className="empty-hint">Click any node on the left to inspect its RAG memory relationships.</p>
          )}

          {/* DYNAMIC PROACTIVE AI ALERTS */}
          <div className="proactive-alerts">
            <h4 style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '15px', fontWeight: '700', color: 'var(--primary-darker)', marginBottom: '12px' }}>
              <ShieldAlert size={18} className="alert-icon" color="#EF5350" /> Proactive AI Memory Alerts
            </h4>
            {alerts.length > 0 ? (
              alerts.map((alert, idx) => (
                <div key={idx} className="alert-item" style={{ background: 'white', borderLeft: `4px solid ${alert.type === 'warning' ? '#EF5350' : alert.type === 'success' ? '#25D366' : '#53BDEB'}`, padding: '12px 14px', borderRadius: '8px', marginBottom: '10px', boxShadow: '0 2px 8px rgba(0,0,0,0.03)' }}>
                  <strong style={{ fontSize: '13px', display: 'block', color: 'var(--text-primary)', marginBottom: '4px' }}>{alert.title}</strong>
                  <p style={{ fontSize: '12px', color: 'var(--text-secondary)', margin: 0, lineHeight: '1.4' }}>{alert.description}</p>
                </div>
              ))
            ) : (
              <div style={{ fontSize: '13px', color: 'var(--text-secondary)', padding: '12px' }}>No active alerts for this chat session.</div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default KnowledgeGraphView;
