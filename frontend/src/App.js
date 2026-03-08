// src/App.js
import React, { Suspense, lazy } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import "./App.css";
import Navbar from "./components/Navbar";

// Lazy-loaded pages — each becomes its own chunk
const SentimentPage = lazy(() => import("./pages/SentimentPage"));
const MarketPage = lazy(() => import("./pages/MarketPage"));
const NewsPage = lazy(() => import("./pages/NewsPage"));

/** Route-level loading spinner shown while a lazy chunk downloads */
const RouteLoader = () => (
  <div className="route-loading">
    <div className="route-spinner" />
  </div>
);

function App() {
  return (
    <Router>
      <div className="app-root">
        <Navbar />
        <Suspense fallback={<RouteLoader />}>
          <Routes>
            <Route path="/" element={<SentimentPage />} />
            <Route path="/market" element={<MarketPage />} />
            <Route path="/news" element={<NewsPage />} />
          </Routes>
        </Suspense>
      </div>
    </Router>
  );
}

export default App;
