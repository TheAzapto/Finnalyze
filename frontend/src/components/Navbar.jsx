// src/components/Navbar.jsx
import React, { useState } from "react";
import { NavLink } from "react-router-dom";

const Navbar = () => {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <nav className="navbar">
      <div className="navbar-left">
        <span className="navbar-logo">Finnalyze</span>
      </div>

      {/* Hamburger toggle (visible on mobile only via CSS) */}
      <button
        className="navbar-toggle"
        onClick={() => setMenuOpen((prev) => !prev)}
        aria-label="Toggle navigation"
      >
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
          {menuOpen ? (
            <>
              <line x1="18" y1="6" x2="6" y2="18" />
              <line x1="6" y1="6" x2="18" y2="18" />
            </>
          ) : (
            <>
              <line x1="3" y1="6" x2="21" y2="6" />
              <line x1="3" y1="12" x2="21" y2="12" />
              <line x1="3" y1="18" x2="21" y2="18" />
            </>
          )}
        </svg>
      </button>

      <div className={`navbar-links${menuOpen ? " open" : ""}`}>
        <NavLink to="/" end className="nav-item" onClick={() => setMenuOpen(false)}>
          Sentiment
        </NavLink>
        <NavLink to="/market" className="nav-item" onClick={() => setMenuOpen(false)}>
          Live Market
        </NavLink>
        <NavLink to="/news" className="nav-item" onClick={() => setMenuOpen(false)}>
          News
        </NavLink>
      </div>
    </nav>
  );
};

export default Navbar;
