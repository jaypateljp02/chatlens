import React, { useState } from 'react';
import { NavLink } from 'react-router-dom';
import { 
  LayoutDashboard, 
  FileText, 
  BarChart2, 
  Users, 
  CheckSquare, 
  MoreHorizontal,
  UploadCloud,
  Share2,
  Tag,
  Clock,
  Settings,
  X,
  Brain
} from 'lucide-react';
import './MobileBottomNav.css';

const moreNavItems = [
  { path: '/', label: 'Upload Chat', icon: UploadCloud },
  { path: '/knowledge-graph', label: 'Knowledge Graph', icon: Share2 },
  { path: '/topics', label: 'Topic Extraction', icon: Tag },
  { path: '/timeline', label: 'Timeline & Milestones', icon: Clock },
  { path: '/settings', label: 'Settings', icon: Settings }
];

export default function MobileBottomNav() {
  const [sheetOpen, setSheetOpen] = useState(false);

  return (
    <>
      {/* MORE MENU BOTTOM SHEET OVERLAY */}
      {sheetOpen && (
        <div className="mobile-sheet-overlay" onClick={() => setSheetOpen(false)}>
          <div className="mobile-sheet-content animate-slide-up" onClick={(e) => e.stopPropagation()}>
            <div className="sheet-header">
              <div className="sheet-title">
                <Brain size={18} color="var(--primary)" />
                <span>More Features</span>
              </div>
              <button className="sheet-close-btn" onClick={() => setSheetOpen(false)}>
                <X size={18} />
              </button>
            </div>

            <div className="sheet-grid">
              {moreNavItems.map((item) => {
                const Icon = item.icon;
                return (
                  <NavLink
                    key={item.path}
                    to={item.path}
                    className="sheet-item"
                    onClick={() => setSheetOpen(false)}
                  >
                    <div className="sheet-icon-wrapper">
                      <Icon size={20} />
                    </div>
                    <span>{item.label}</span>
                  </NavLink>
                );
              })}
            </div>
          </div>
        </div>
      )}

      {/* NATIVE MOBILE BOTTOM NAVIGATION BAR */}
      <nav className="mobile-bottom-nav">
        <NavLink to="/dashboard" className={({ isActive }) => `bottom-tab ${isActive ? 'active' : ''}`}>
          <LayoutDashboard size={20} />
          <span>Home</span>
        </NavLink>

        <NavLink to="/summaries" className={({ isActive }) => `bottom-tab ${isActive ? 'active' : ''}`}>
          <FileText size={20} />
          <span>Ask AI</span>
        </NavLink>

        <NavLink to="/analytics" className={({ isActive }) => `bottom-tab ${isActive ? 'active' : ''}`}>
          <BarChart2 size={20} />
          <span>Stats</span>
        </NavLink>

        <NavLink to="/people" className={({ isActive }) => `bottom-tab ${isActive ? 'active' : ''}`}>
          <Users size={20} />
          <span>People</span>
        </NavLink>

        <NavLink to="/actions" className={({ isActive }) => `bottom-tab ${isActive ? 'active' : ''}`}>
          <CheckSquare size={20} />
          <span>Tasks</span>
        </NavLink>

        <button 
          className={`bottom-tab more-tab ${sheetOpen ? 'active' : ''}`}
          onClick={() => setSheetOpen(!sheetOpen)}
        >
          <MoreHorizontal size={20} />
          <span>More</span>
        </button>
      </nav>
    </>
  );
}
