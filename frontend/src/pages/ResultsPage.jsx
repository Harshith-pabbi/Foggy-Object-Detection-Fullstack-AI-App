import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { ArrowLeft, RefreshCw } from 'lucide-react';
import { getResults, getFileUrl } from '../api';
import VideoPlayer from '../components/VideoPlayer';
import DetectionTable from '../components/DetectionTable';
import StatusBadge from '../components/StatusBadge';

const ResultsPage = () => {
  const { jobId } = useParams();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchResults = async () => {
    try {
      const result = await getResults(jobId);
      setData(result);
      setLoading(false);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to fetch results.');
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchResults();
    // Poll if still processing
    let interval;
    if (data && (data.status === 'pending' || data.status === 'processing')) {
      interval = setInterval(fetchResults, 3000);
    }
    return () => clearInterval(interval);
  }, [jobId, data?.status]);

  if (loading) {
    return (
      <div className="page-container content-center">
        <div className="loading-spinner-large"></div>
        <p className="loading-text">Loading details...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="page-container content-center">
        <div className="error-card glass-panel">
          <h2>Error</h2>
          <p>{error}</p>
          <Link to="/" className="link-btn"><ArrowLeft size={16} /> Back to Upload</Link>
        </div>
      </div>
    );
  }

  return (
    <div className="page-container">
      <header className="page-header">
        <Link to="/" className="back-link"><ArrowLeft size={18} /> Back</Link>
        <div className="header-info">
          <h2>Analysis Results</h2>
          <StatusBadge status={data.status} />
        </div>
      </header>

      <div className="dashboard-grid">
        <div className="dashboard-col left-col">
          <div className="video-card glass-panel">
            <VideoPlayer 
              src={getFileUrl(data.input_url)} 
              title="Original Video" 
            />
          </div>
          <div className="video-card glass-panel">
            <VideoPlayer 
              src={getFileUrl(data.output_url)} 
              title="Dehazed & Detected Video" 
            />
          </div>
        </div>

        <div className="dashboard-col right-col glass-panel">
          <h3>Detection Summaries</h3>
          {data.status === 'completed' ? (
            <DetectionTable detections={data.detections} />
          ) : (
            <div className="processing-state">
              <RefreshCw className="spin-icon" size={24} />
              <p>AI pipeline is currently processing the video...</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ResultsPage;
