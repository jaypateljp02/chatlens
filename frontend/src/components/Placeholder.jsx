import React from 'react';

export default function PlaceholderPage({ title }) {
  return (
    <div className="animate-fade-in" style={{ 
      display: 'flex', 
      flexDirection: 'column', 
      alignItems: 'center', 
      justifyContent: 'center',
      height: '60vh',
      textAlign: 'center'
    }}>
      <h2 style={{ fontSize: '2rem', marginBottom: '1rem', color: 'var(--text-primary)' }}>{title}</h2>
      <p style={{ color: 'var(--text-secondary)', maxWidth: '500px' }}>
        This module is currently under development. It will provide deep insights and visualizations for your WhatsApp chats.
      </p>
      <div style={{ marginTop: '2rem', padding: '2rem', background: 'var(--bg-white)', borderRadius: 'var(--radius-lg)', border: '1px dashed var(--border)', width: '100%', maxWidth: '600px' }}>
        <div className="shimmer-block" style={{ width: '100%', height: '200px', margin: '0' }}></div>
      </div>
    </div>
  );
}
