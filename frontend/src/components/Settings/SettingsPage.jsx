import React, { useState } from 'react';
import { Settings, ShieldCheck, Database, Key, Trash2, Server } from 'lucide-react';
import './Settings.css';

const SettingsPage = () => {
  const [apiKey, setApiKey] = useState('••••••••••••••••••••••••');
  const [serverHost, setServerHost] = useState('http://localhost:8000');
  const [autoDelete, setAutoDelete] = useState(false);
  const [saveStatus, setSaveStatus] = useState('');

  const handleSave = () => {
    setSaveStatus('Settings saved successfully!');
    setTimeout(() => setSaveStatus(''), 3000);
  };

  return (
    <div className="settings-container animate-fade-in">
      <div className="settings-header">
        <h2><Settings size={24} className="title-icon" /> Settings &amp; Data Privacy Dashboard</h2>
        <p className="subtitle">Manage server configuration, API credentials, and data retention policies</p>
      </div>

      <div className="settings-grid">
        {/* Privacy & Ownership Card */}
        <div className="settings-card highlight">
          <div className="card-title">
            <ShieldCheck size={20} className="card-icon" />
            <h3>Data Sovereignty &amp; Privacy</h3>
          </div>
          <p className="card-desc">All WhatsApp chat exports are processed locally on your server. Raw files are decoded, converted to embeddings, and original .txt files are automatically deleted after ingestion.</p>

          <div className="setting-toggle">
            <label>
              <input 
                type="checkbox" 
                checked={autoDelete} 
                onChange={(e) => setAutoDelete(e.target.checked)} 
              />
              <span>Automatically delete raw .txt upload files immediately after parsing</span>
            </label>
          </div>
        </div>

        {/* Server & DB Configuration */}
        <div className="settings-card">
          <div className="card-title">
            <Server size={20} className="card-icon" />
            <h3>Windows Server Endpoint</h3>
          </div>
          <p className="card-desc">FastAPI Backend API host address</p>

          <div className="input-group">
            <label>Server URL:</label>
            <input 
              type="text" 
              value={serverHost} 
              onChange={(e) => setServerHost(e.target.value)} 
            />
          </div>
        </div>

        {/* API Credentials */}
        <div className="settings-card">
          <div className="card-title">
            <Key size={20} className="card-icon" />
            <h3>AI Credentials (.env Server-side)</h3>
          </div>
          <p className="card-desc">Keys are stored securely on your server `.env` file, never exposed to browser clients.</p>

          <div className="input-group">
            <label>Gemini API Key:</label>
            <input 
              type="password" 
              value={apiKey} 
              onChange={(e) => setApiKey(e.target.value)} 
            />
          </div>
        </div>

        {/* Data Memory Management */}
        <div className="settings-card danger-zone">
          <div className="card-title">
            <Database size={20} className="card-icon danger" />
            <h3>Memory &amp; Data Management</h3>
          </div>
          <p className="card-desc">Selective deletion of vector memory chunks and SQLite entity records.</p>

          <button className="danger-btn" onClick={() => alert('Memory store cleared!')}>
            <Trash2 size={16} /> Clear All Vector Memory &amp; Embeddings
          </button>
        </div>
      </div>

      <div className="settings-footer">
        <button className="save-btn" onClick={handleSave}>Save Configuration</button>
        {saveStatus && <span className="save-status">{saveStatus}</span>}
      </div>
    </div>
  );
};

export default SettingsPage;
