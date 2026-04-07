import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { UploadCloud, FileVideo, ChevronRight } from 'lucide-react';
import { uploadVideo } from '../api';

const UploadPage = () => {
  const [file, setFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
      setError(null);
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    setIsUploading(true);
    setError(null);

    try {
      const response = await uploadVideo(file);
      navigate(`/results/${response.job_id}`);
    } catch (err) {
      setError(err.response?.data?.detail || 'An error occurred during upload.');
      setIsUploading(false);
    }
  };

  return (
    <div className="page-container content-center">
      <div className="upload-card glass-panel">
        <div className="hero-section">
          <h1 className="gradient-text">Foggy Weather Detection</h1>
          <p className="subtitle">Enhance visibility and detect objects in extreme weather conditions using AI.</p>
        </div>

        <div className="upload-zone">
          <input 
            type="file" 
            id="file-upload" 
            accept="video/*" 
            onChange={handleFileChange}
            className="hidden-input"
          />
          <label htmlFor="file-upload" className="upload-label">
            <UploadCloud size={48} className="upload-icon" />
            <span className="upload-text">
              {file ? file.name : "Click to select or drag and drop a video"}
            </span>
            <span className="upload-subtext">Supports MP4, AVI, MOV up to 100MB</span>
          </label>
        </div>

        {error && <div className="error-message">{error}</div>}

        <button 
          className="primary-btn" 
          onClick={handleUpload}
          disabled={!file || isUploading}
        >
          {isUploading ? (
            <span className="loading-state"><span className="spinner"></span> Processing...</span>
          ) : (
             <span className="btn-content">Analyze Video <ChevronRight size={18} /></span>
          )}
        </button>
      </div>
    </div>
  );
};

export default UploadPage;
