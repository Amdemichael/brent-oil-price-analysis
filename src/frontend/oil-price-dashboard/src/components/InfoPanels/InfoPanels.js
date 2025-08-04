import React from 'react';

const InfoPanels = ({ dataSummary, impactSummary, changePoints }) => {
  const formatNumber = (num) => {
    if (num === null || num === undefined) return 'N/A';
    return typeof num === 'number' ? num.toFixed(2) : num;
  };

  const formatCurrency = (num) => {
    if (num === null || num === undefined) return 'N/A';
    return typeof num === 'number' ? `$${num.toFixed(2)}` : num;
  };

  return (
    <div className="info-panels">
      {/* Data Summary Panel */}
      <div className="info-panel">
        <h4 style={{ marginBottom: '15px', color: '#2a5298', fontSize: '16px' }}>
          📊 Data Summary
        </h4>
        {dataSummary ? (
          <div>
            <div style={{ marginBottom: '10px' }}>
              <strong>Total Records:</strong> {dataSummary.total_records?.toLocaleString()}
            </div>
            <div style={{ marginBottom: '10px' }}>
              <strong>Date Range:</strong> {dataSummary.date_range?.start} to {dataSummary.date_range?.end}
            </div>
            <div style={{ marginBottom: '10px' }}>
              <strong>Price Range:</strong> {formatCurrency(dataSummary.price_stats?.min)} - {formatCurrency(dataSummary.price_stats?.max)}
            </div>
            <div style={{ marginBottom: '10px' }}>
              <strong>Average Price:</strong> {formatCurrency(dataSummary.price_stats?.mean)}
            </div>
            <div>
              <strong>Price Volatility:</strong> {formatCurrency(dataSummary.price_stats?.std)}
            </div>
          </div>
        ) : (
          <div style={{ color: '#666', fontStyle: 'italic' }}>Loading data summary...</div>
        )}
      </div>

      {/* Impact Summary Panel */}
      <div className="info-panel">
        <h4 style={{ marginBottom: '15px', color: '#2a5298', fontSize: '16px' }}>
          📈 Impact Analysis
        </h4>
        {impactSummary ? (
          <div>
            <div style={{ marginBottom: '10px' }}>
              <strong>Total Events:</strong> {impactSummary.total_events}
            </div>
            <div style={{ marginBottom: '10px' }}>
              <strong>Avg Impact:</strong> {formatNumber(impactSummary.average_price_change)}%
            </div>
            <div style={{ marginBottom: '10px' }}>
              <strong>Max Positive:</strong> {formatNumber(impactSummary.max_positive_impact)}%
            </div>
            <div style={{ marginBottom: '10px' }}>
              <strong>Max Negative:</strong> {formatNumber(impactSummary.max_negative_impact)}%
            </div>
            <div>
              <strong>Positive Events:</strong> {impactSummary.events_with_positive_impact} / {impactSummary.total_events}
            </div>
          </div>
        ) : (
          <div style={{ color: '#666', fontStyle: 'italic' }}>Loading impact summary...</div>
        )}
      </div>

      {/* Change Point Panel */}
      <div className="info-panel">
        <h4 style={{ marginBottom: '15px', color: '#2a5298', fontSize: '16px' }}>
          🔍 Change Point Analysis
        </h4>
        {changePoints ? (
          <div>
            <div style={{ marginBottom: '10px' }}>
              <strong>Change Point Date:</strong> {changePoints.change_point_date}
            </div>
            <div style={{ marginBottom: '10px' }}>
              <strong>Price Change:</strong> {formatNumber(changePoints.price_change_pct)}%
            </div>
            <div style={{ marginBottom: '10px' }}>
              <strong>Volatility Change:</strong> {formatNumber(changePoints.volatility_change)}
            </div>
            <div style={{ marginBottom: '10px' }}>
              <strong>Before Avg Price:</strong> {formatCurrency(changePoints.before_stats?.mean_price)}
            </div>
            <div>
              <strong>After Avg Price:</strong> {formatCurrency(changePoints.after_stats?.mean_price)}
            </div>
          </div>
        ) : (
          <div style={{ color: '#666', fontStyle: 'italic' }}>
            Run change point analysis to see results
          </div>
        )}
      </div>

      {/* Quick Stats Panel */}
      <div className="info-panel">
        <h4 style={{ marginBottom: '15px', color: '#2a5298', fontSize: '16px' }}>
          ⚡ Quick Stats
        </h4>
        {impactSummary ? (
          <div>
            <div style={{ marginBottom: '10px' }}>
              <strong>Most Impactful Category:</strong>
              <br />
              {Object.entries(impactSummary.category_breakdown || {})
                .sort(([,a], [,b]) => b - a)[0]?.[0] || 'N/A'}
            </div>
            <div style={{ marginBottom: '10px' }}>
              <strong>Most Active Region:</strong>
              <br />
              {Object.entries(impactSummary.region_breakdown || {})
                .sort(([,a], [,b]) => b - a)[0]?.[0] || 'N/A'}
            </div>
            <div style={{ marginBottom: '10px' }}>
              <strong>Analysis Period:</strong>
              <br />
              {dataSummary?.date_range?.start} - {dataSummary?.date_range?.end}
            </div>
            <div>
              <strong>Data Quality:</strong>
              <br />
              {dataSummary?.total_records ? 'High' : 'Unknown'}
            </div>
          </div>
        ) : (
          <div style={{ color: '#666', fontStyle: 'italic' }}>Loading statistics...</div>
        )}
      </div>
    </div>
  );
};

export default InfoPanels; 