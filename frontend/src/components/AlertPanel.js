import React from 'react';

const AlertPanel = ({ prediction, state }) => {
  const getAlertColor = () => {
    switch (state) {
      case 'critical':
        return 'bg-red-100 border-red-500 text-red-700';
      case 'warning':
        return 'bg-yellow-100 border-yellow-500 text-yellow-700';
      default:
        return 'bg-green-100 border-green-500 text-green-700';
    }
  };

  return (
    <div className={`p-4 rounded-lg border ${getAlertColor()}`}>
      <h2 className="text-xl font-semibold mb-4">Equipment Status</h2>
      <div className="space-y-2">
        <p>
          <span className="font-medium">Status: </span>
          {state.charAt(0).toUpperCase() + state.slice(1)}
        </p>
        <p>
          <span className="font-medium">Maintenance Needed: </span>
          {prediction.needs_maintenance ? 'Yes' : 'No'}
        </p>
        <p>
          <span className="font-medium">Risk Level: </span>
          {prediction.risk_level}
        </p>
        <p>
          <span className="font-medium">Confidence: </span>
          {(prediction.confidence * 100).toFixed(1)}%
        </p>
      </div>
    </div>
  );
};

export default AlertPanel;