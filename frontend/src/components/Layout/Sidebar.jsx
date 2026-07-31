import React, { useState } from 'react';
import { NavLink } from 'react-router-dom';
import { 
  UploadCloud, 
  LayoutDashboard, 
  FileText, 
  BarChart2, 
  Heart, 
  Users, 
  Tag, 
  Clock, 
  CheckSquare, 
  Share2, 
  Settings,
  Menu,
  X,
  Brain
} from 'lucide-react';
import './Sidebar.css';

const navItems = [
  { path: '/', label: 'Upload', icon: UploadCloud },
  { path: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { path: '/summaries', label: 'Summaries', icon: FileText },
  { path: '/analytics', label: 'Analytics', icon: BarChart2 },
  { path: '/sentiment', label: 'Sentiment', icon: Heart },
  { path: '/people', label: 'People', icon: Users },
  { path: '/topics', label: 'Topics', icon: Tag },
  { path: '/timeline', label: 'Timeline', icon: Clock },
  { path: '/actions', label: 'Actions', icon: CheckSquare },
  { path: '/knowledge-graph', label: 'Knowledge Graph', icon: Share2 },
  { path: '/settings', label: 'Settings', icon: Settings }
];

export default function Sidebar() {
  const [collapsed, setCollapsed] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);

  const handleNavClick = () => {
    setMobileOpen(false);
  };

  return (
    <>
      {/* Mobile Hamburger Floating Button */}
      <button 
        className="mobile-hamburger-btn"
        onClick={() => setMobileOpen(!mobileOpen)}
        aria-label="Toggle Navigation"
      >
        {mobileOpen ? <X size={24} /> : <Menu size={24} />}
      </button>

      {/* Mobile Backdrop Overlay */}
      {mobileOpen && (
        <div 
          className="mobile-backdrop" 
          onClick={() => setMobileOpen(false)} 
        />
      )}

      <aside className={`sidebar ${collapsed ? 'collapsed' : ''} ${mobileOpen ? 'mobile-open' : ''}`} id="main-sidebar">
        <div className="sidebar-header">
          {!collapsed && <div className="brand animate-fade-in"><Brain className="brand-icon" /> <span>ChatLens AI</span></div>}
          {collapsed && <Brain className="brand-icon collapsed-brand" />}
          <button className="toggle-btn desktop-only-toggle" onClick={() => setCollapsed(!collapsed)} id="sidebar-toggle">
            <Menu size={20} />
          </button>
          <button className="toggle-btn mobile-close-btn" onClick={() => setMobileOpen(false)}>
            <X size={20} />
          </button>
        </div>
        
        <nav className="sidebar-nav">
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink 
                key={item.path} 
                to={item.path} 
                className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
                title={collapsed ? item.label : ''}
                end={item.path === '/'}
                onClick={handleNavClick}
              >
                <Icon size={20} className="nav-icon" />
                {!collapsed && <span className="nav-label">{item.label}</span>}
              </NavLink>
            );
          })}
        </nav>
      </aside>
    </>
  );
}
