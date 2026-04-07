import React from 'react';

const DetectionTable = ({ detections }) => {
  if (!detections || detections.length === 0) {
    return (
      <div className="empty-state">
        <p>No detections recorded for this video.</p>
      </div>
    );
  }

  return (
    <div className="table-container">
      <table className="detection-table">
        <thead>
          <tr>
            <th>Class</th>
            <th>Confidence</th>
            <th>Bounding Box</th>
          </tr>
        </thead>
        <tbody>
          {detections.map((det, index) => (
            <tr key={index}>
              <td>
                <span className="class-badge">{det.class}</span>
              </td>
              <td>
                <div className="confidence-bar-container">
                  <div 
                    className="confidence-fill" 
                    style={{ width: `${det.confidence * 100}%` }}
                  ></div>
                </div>
                <span className="confidence-text">{(det.confidence * 100).toFixed(1)}%</span>
              </td>
              <td className="monospace">[{det.bbox.join(', ')}]</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default DetectionTable;
