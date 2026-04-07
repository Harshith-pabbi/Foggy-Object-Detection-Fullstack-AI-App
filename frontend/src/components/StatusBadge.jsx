import React from 'react';

const StatusBadge = ({ status }) => {
  const statusConfig = {
    pending: { color: 'var(--color-warning)', label: 'Pending', icon: '⏳' },
    processing: { color: 'var(--color-info)', label: 'Processing', icon: '⚙️' },
    completed: { color: 'var(--color-success)', label: 'Completed', icon: '✅' },
    failed: { color: 'var(--color-error)', label: 'Failed', icon: '❌' },
  };

  const config = statusConfig[status.toLowerCase()] || statusConfig.pending;

  return (
    <span 
      className="status-badge" 
      style={{ 
        backgroundColor: `color-mix(in srgb, ${config.color} 20%, transparent)`,
        color: config.color,
        border: `1px solid ${config.color}`
      }}
    >
      <span className="status-icon">{config.icon}</span>
      {config.label}
    </span>
  );
};

export default StatusBadge;
