import React from 'react';

const NAV_ITEMS = [
  { id: 'landing', label: 'Home' },
  { id: 'plans', label: 'Plans' },
  { id: 'dashboard', label: 'Studio' },
];

export default function Navbar({ navigate, userData, currentPage }) {
  return (
    <header className="navbar">
      <div className="brand-cluster">
        <button className="brand-button" type="button" onClick={() => navigate('landing')}>
          <span className="brand-mark">Z</span>
          <span>Zebec AI</span>
        </button>
      </div>

      <nav className="nav-links" aria-label="Main navigation">
        {NAV_ITEMS.map((item) => (
          <button
            key={item.id}
            type="button"
            className={`nav-button ${currentPage === item.id ? 'is-active' : ''}`}
            onClick={() => navigate(item.id)}
          >
            {item.label}
          </button>
        ))}
      </nav>

      <div className="nav-user">
        <span className="status-dot" aria-hidden="true" />
        <p className="user-pill">{userData ? userData.email : 'Guest mode'}</p>
      </div>
    </header>
  );
}
