import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import UploadPage from './pages/UploadPage';
import ResultsPage from './pages/ResultsPage';

function App() {
  return (
    <Router>
      <div className="app-layout">
        <Routes>
          <Route path="/" element={<UploadPage />} />
          <Route path="/results/:jobId" element={<ResultsPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
