import React, { useState, useEffect } from 'react';
import { Search, Users, UploadCloud } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import ProfileCard from './ProfileCard';
import { getPeopleProfiles } from '../../utils/api';
import './People.css';

const PeoplePage = () => {
  const [profiles, setProfiles] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();
  const activeChatId = localStorage.getItem('activeChatId');

  useEffect(() => {
    async function loadData() {
      if (!activeChatId) {
        setLoading(false);
        return;
      }
      try {
        const data = await getPeopleProfiles();
        setProfiles(data?.profiles || []);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, [activeChatId]);

  const filteredProfiles = profiles.filter(p => 
    p.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (!activeChatId && !loading) {
    return (
      <div style={{ textAlign: 'center', padding: '60px 20px' }}>
        <div style={{ background: 'white', border: '1px solid var(--border)', borderRadius: '24px', padding: '48px 32px', maxWidth: '540px', margin: '0 auto' }}>
          <UploadCloud size={56} style={{ color: 'var(--primary)', marginBottom: '16px' }} />
          <h2 style={{ fontSize: '20px', fontWeight: '700', marginBottom: '8px' }}>No Chat Uploaded Yet</h2>
          <p style={{ color: 'var(--text-secondary)', fontSize: '14px', marginBottom: '24px' }}>Please upload a WhatsApp chat export file (.txt) to view participant profiles.</p>
          <button onClick={() => navigate('/')} style={{ background: 'var(--primary)', color: 'white', border: 'none', padding: '12px 28px', borderRadius: '24px', fontWeight: '700', cursor: 'pointer' }}>Upload WhatsApp Chat</button>
        </div>
      </div>
    );
  }

  return (
    <div className="people-container animate-fade-in">
      <div className="people-header-row">
        <div>
          <h2><Users size={24} className="title-icon" /> People Profiles</h2>
          <p className="subtitle">Individual participation scores, communication styles, and interaction metrics</p>
        </div>
        <div className="search-box">
          <Search size={18} className="search-icon" />
          <input 
            type="text" 
            placeholder="Search participant..." 
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
      </div>

      {loading ? (
        <div className="loading-state">Loading profiles...</div>
      ) : (
        <div className="profiles-grid">
          {filteredProfiles.map((profile, idx) => (
            <ProfileCard key={idx} profile={profile} />
          ))}
        </div>
      )}
    </div>
  );
};

export default PeoplePage;
