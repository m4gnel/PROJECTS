import React from 'react';
import { 
  SquarePen, 
  Search, 
  Folder, 
  Plus, 
  PanelLeftClose, 
  PanelLeft,
  Sparkles,
  Layers,
  FileText,
  BarChart3
} from 'lucide-react';

export default function Sidebar({ 
  collapsed, 
  setCollapsed, 
  projects, 
  activeProject, 
  setActiveProject,
  onNewChat,
  onOpenReport,
  onOpenMetrics,
  onOpenArchitecture,
  onOpenSamples
}) {
  return (
    <aside className={`sidebar ${collapsed ? 'collapsed' : ''}`}>
      {/* Sidebar Header */}
      <div className="sidebar-header">
        {!collapsed && (
          <div className="logo-group" onClick={onNewChat} title="Reset to Home">
            <div className="logo-icon">
              {/* Geometric flower emblem matching screenshot */}
              <svg className="logo-flower" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 2C13.1 2 14 2.9 14 4C14 4.7 13.6 5.3 13 5.7V8.3C13.6 8.7 14 9.3 14 10C14 11.1 13.1 12 12 12C10.9 12 10 11.1 10 10C10 9.3 10.4 8.7 11 8.3V5.7C10.4 5.3 10 4.7 10 4C10 2.9 10.9 2 12 2ZM6.3 7.7C7.1 6.9 8.4 6.9 9.2 7.7C9.7 8.2 9.9 8.9 9.7 9.5L11.5 11.3C12 11 12.7 11 13.2 11.4C14 12.2 14 13.5 13.2 14.3C12.4 15.1 11.1 15.1 10.3 14.3C9.9 13.8 9.9 13.1 10.2 12.6L8.4 10.8C7.8 11 7.1 10.8 6.6 10.3C5.8 9.5 5.8 8.2 6.6 7.4L6.3 7.7ZM17.7 7.7L17.4 7.4C18.2 8.2 18.2 9.5 17.4 10.3C16.9 10.8 16.2 11 15.6 10.8L13.8 12.6C14.1 13.1 14.1 13.8 13.7 14.3C12.9 15.1 11.6 15.1 10.8 14.3C10 13.5 10 12.2 10.8 11.4C11.3 11 12 11 12.5 11.3L14.3 9.5C14.1 8.9 14.3 8.2 14.8 7.7C15.6 6.9 16.9 6.9 17.7 7.7ZM12 14C13.1 14 14 14.9 14 16C14 16.7 13.6 17.3 13 17.7V20.3C13.6 20.7 14 21.3 14 22C14 23.1 13.1 24 12 24C10.9 24 10 23.1 10 22C10 21.3 10.4 20.7 11 20.3V17.7C10.4 17.3 10 16.7 10 16C10 14.9 10.9 14 12 14Z" opacity="0.9"/>
                <circle cx="12" cy="12" r="3" fill="#38bdf8"/>
              </svg>
            </div>
            <span className="logo-text">AIChat <span className="logo-badge">BiLSTM</span></span>
          </div>
        )}
        <button 
          className="icon-btn-ghost" 
          onClick={() => setCollapsed(!collapsed)}
          title={collapsed ? "Expand sidebar" : "Collapse sidebar"}
        >
          {collapsed ? <PanelLeft size={18} /> : <PanelLeftClose size={18} />}
        </button>
      </div>

      {/* Main Action Buttons */}
      <div className="sidebar-nav">
        <button className="nav-item active" onClick={onNewChat} title="Start New Verification">
          <SquarePen size={18} />
          {!collapsed && <span>New Chat</span>}
        </button>
        <button className="nav-item" onClick={onOpenSamples} title="Search & Test Samples">
          <Search size={18} />
          {!collapsed && <span>Search</span>}
        </button>
      </div>

      {/* Projects Section (Matches Screenshot) */}
      <div className="sidebar-section">
        {!collapsed && (
          <div className="section-header">
            <span>Projects</span>
            <button className="icon-btn-ghost" onClick={onOpenSamples} title="Add Project or Sample">
              <Plus size={15} />
            </button>
          </div>
        )}
        
        <ul className="project-list">
          {projects.map((proj) => (
            <li 
              key={proj.id} 
              className={`project-item ${activeProject === proj.id ? 'selected' : ''}`}
              onClick={() => setActiveProject(proj.id)}
              title={`${proj.name} (${proj.category})`}
            >
              <div className="project-left">
                <Folder size={17} color={activeProject === proj.id ? '#60a5fa' : '#94a3b8'} />
                {!collapsed && <span>{proj.name}</span>}
              </div>
              {!collapsed && <span className="project-count-badge">{proj.count}</span>}
            </li>
          ))}
        </ul>

        {/* Quick Tools & Academic Shortcuts in Sidebar */}
        {!collapsed && (
          <div style={{ marginTop: '24px' }}>
            <div className="section-header">
              <span>Deep Learning Tools</span>
            </div>
            <div className="sidebar-nav" style={{ gap: '2px' }}>
              <button className="nav-item" onClick={onOpenMetrics} title="Model Metrics & Confusion Matrix">
                <BarChart3 size={16} color="#34d399" />
                <span>99.36% Metrics</span>
              </button>
              <button className="nav-item" onClick={onOpenArchitecture} title="BiLSTM Layer Schematic">
                <Layers size={16} color="#818cf8" />
                <span>Neural Net Arch</span>
              </button>
              <button className="nav-item" onClick={onOpenReport} title="Course Project Report (AIT-401)">
                <FileText size={16} color="#38bdf8" />
                <span>Course Report</span>
              </button>
            </div>
          </div>
        )}
      </div>

      {/* User Profile Pill at Bottom (Matches Reference Screenshot) */}
      <div className="user-profile-pill" title="Research Lead: Magnel Olivero (ASI23CA040)">
        <div className="user-info-left">
          {/* User profile avatar matching screenshot style */}
          <img 
            src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=120&q=80" 
            alt="Magnel Olivero" 
            className="user-avatar"
            onError={(e) => {
              e.target.onerror = null;
              e.target.src = "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=120&q=80";
            }}
          />
          {!collapsed && (
            <div className="user-text-col">
              <span className="user-name">Magnel...</span>
              <span className="user-plan">Free</span>
            </div>
          )}
        </div>
        {!collapsed && (
          <button className="upgrade-btn" onClick={onOpenReport} title="KTU Deep Learning Project Details">
            Upgrade
          </button>
        )}
      </div>
    </aside>
  );
}
