// src/components/Navbar.jsx
import React from "react";
import { NavLink } from "react-router-dom";

const Navbar = () => {
  return (
    <nav className="navbar">
      <div className="navbar-left">
        <span className="navbar-logo">FinSight</span>
      </div>
      <div className="navbar-links">
        <NavLink to="/" end className="nav-item">
          Sentiment
        </NavLink>
        <NavLink to="/market" className="nav-item">
          Live Market
        </NavLink>
        <NavLink to="/news" className="nav-item">
          News
        </NavLink>
      </div>
    </nav>
  );
};

export default Navbar;
