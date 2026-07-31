import React from 'react';
import { MessageSquare, Heart, Award, Clock } from 'lucide-react';

const ProfileCard = ({ profile }) => {
  const getBadgeColor = (score) => {
    if (score >= 70) return '#25D366';
    if (score >= 40) return '#FFA726';
    return '#EF5350';
  };

  const getInitials = (name) => {
    return name
      .split(' ')
      .map(part => part[0])
      .join('')
      .substring(0, 2)
      .toUpperCase();
  };

  return (
    <div className="profile-card">
      <div className="profile-header">
        <div className="profile-avatar">
          {getInitials(profile.name)}
        </div>
        <div className="profile-info">
          <h3 className="profile-name">{profile.name}</h3>
          <span className="profile-style">{profile.communication_style}</span>
        </div>
        <div 
          className="engagement-badge"
          style={{ backgroundColor: `${getBadgeColor(profile.engagement_score)}15`, color: getBadgeColor(profile.engagement_score) }}
        >
          <Award size={14} />
          <span>{profile.engagement_score} pts</span>
        </div>
      </div>

      <div className="profile-stats">
        <div className="stat-item">
          <MessageSquare size={16} className="stat-icon" />
          <span className="stat-value">{profile.messages_count}</span>
          <span className="stat-label">Messages</span>
        </div>
        <div className="stat-item">
          <Clock size={16} className="stat-icon" />
          <span className="stat-value">{profile.peak_hour}:00</span>
          <span className="stat-label">Peak Hour</span>
        </div>
        <div className="stat-item">
          <Heart size={16} className="stat-icon" />
          <span className="stat-value">{profile.avg_msg_length} chars</span>
          <span className="stat-label">Avg Length</span>
        </div>
      </div>

      {profile.top_emojis && profile.top_emojis.length > 0 && (
        <div className="profile-emojis">
          <span className="emoji-title">Top Emojis:</span>
          <div className="emoji-list">
            {profile.top_emojis.map((item, idx) => (
              <span key={idx} className="emoji-pill" title={`${item.count} times`}>
                {item.emoji} {item.count}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default ProfileCard;
