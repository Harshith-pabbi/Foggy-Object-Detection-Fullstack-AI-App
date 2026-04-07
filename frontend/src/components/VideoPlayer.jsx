import React from 'react';

const VideoPlayer = ({ src, title }) => {
  if (!src) {
    return (
      <div className="video-player-placeholder">
        <p>Video not available yet.</p>
      </div>
    );
  }

  return (
    <div className="video-player-container">
      {title && <h3 className="video-title">{title}</h3>}
      <video className="video-element" controls>
        <source src={src} type="video/mp4" />
        Your browser does not support the video tag.
      </video>
    </div>
  );
};

export default VideoPlayer;
