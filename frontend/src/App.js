// src/App.js
import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import "./App.css";
import Navbar from "./components/Navbar";
import SentimentPage from "./pages/SentimentPage";
import MarketPage from "./pages/MarketPage";
import NewsPage from "./pages/NewsPage";

function App() {
  return (
    <Router>
      <div className="app-root">
        <Navbar />
        <Routes>
          <Route path="/" element={<SentimentPage />} />
          <Route path="/market" element={<MarketPage />} />
          <Route path="/news" element={<NewsPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
