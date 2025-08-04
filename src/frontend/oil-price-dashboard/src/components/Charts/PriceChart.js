import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  ReferenceLine
} from 'recharts';

const PriceChart = ({ data, events, changePoints }) => {
  // Transform data for Recharts
  const chartData = data.map(item => ({
    date: item.date,
    price: item.price,
    name: item.date
  }));

  // Create event markers
  const eventMarkers = events.map(event => ({
    date: event.date,
    event: event.event,
    category: event.category,
    expected_impact: event.expected_impact
  }));

  // Custom tooltip
  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div style={{
          backgroundColor: 'rgba(255, 255, 255, 0.95)',
          border: '1px solid #ccc',
          borderRadius: '5px',
          padding: '10px',
          boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)'
        }}>
          <p style={{ margin: '0 0 5px 0', fontWeight: 'bold' }}>
            {label}
          </p>
          <p style={{ margin: '0', color: '#2a5298' }}>
            Price: ${payload[0].value.toFixed(2)}
          </p>
          
          {/* Show events on this date */}
          {eventMarkers.filter(event => event.date === label).map((event, index) => (
            <div key={index} style={{ marginTop: '5px', padding: '5px', backgroundColor: '#f0f0f0', borderRadius: '3px' }}>
              <p style={{ margin: '0', fontSize: '12px', fontWeight: 'bold' }}>
                {event.event}
              </p>
              <p style={{ margin: '0', fontSize: '10px', color: '#666' }}>
                {event.category} - {event.expected_impact}
              </p>
            </div>
          ))}
        </div>
      );
    }
    return null;
  };

  // Get color for event category
  const getEventColor = (category) => {
    const colors = {
      'Military Conflict': '#d32f2f',
      'Economic Crisis': '#f57c00',
      'OPEC Policy': '#1976d2',
      'Terrorism': '#7b1fa2',
      'Political Unrest': '#388e3c',
      'Technology': '#5d4037',
      'Pandemic': '#616161'
    };
    return colors[category] || '#666';
  };

  return (
    <div style={{ width: '100%', height: '400px' }}>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
          <XAxis 
            dataKey="date" 
            tick={{ fontSize: 12 }}
            tickFormatter={(value) => {
              const date = new Date(value);
              return date.toLocaleDateString('en-US', { 
                month: 'short', 
                year: '2-digit' 
              });
            }}
          />
          <YAxis 
            tick={{ fontSize: 12 }}
            tickFormatter={(value) => `$${value}`}
          />
          <Tooltip content={<CustomTooltip />} />
          <Legend />
          
          {/* Main price line */}
          <Line
            type="monotone"
            dataKey="price"
            stroke="#2a5298"
            strokeWidth={2}
            dot={false}
            name="Brent Oil Price"
          />
          
          {/* Event markers */}
          {eventMarkers.map((event, index) => (
            <ReferenceLine
              key={index}
              x={event.date}
              stroke={getEventColor(event.category)}
              strokeDasharray="5 5"
              strokeWidth={2}
              label={{
                value: event.event.substring(0, 20) + '...',
                position: 'top',
                fontSize: 10,
                fill: getEventColor(event.category)
              }}
            />
          ))}
          
          {/* Change point marker */}
          {changePoints && (
            <ReferenceLine
              x={changePoints.change_point_date}
              stroke="#ff6b35"
              strokeWidth={3}
              label={{
                value: `Change Point: ${changePoints.price_change_pct.toFixed(2)}%`,
                position: 'bottom',
                fontSize: 12,
                fill: '#ff6b35',
                fontWeight: 'bold'
              }}
            />
          )}
        </LineChart>
      </ResponsiveContainer>
      
      {/* Legend for event types */}
      <div style={{ marginTop: '10px', fontSize: '12px' }}>
        <strong>Event Types:</strong>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '10px', marginTop: '5px' }}>
          {Object.entries({
            'Military Conflict': '#d32f2f',
            'Economic Crisis': '#f57c00',
            'OPEC Policy': '#1976d2',
            'Terrorism': '#7b1fa2',
            'Political Unrest': '#388e3c',
            'Technology': '#5d4037',
            'Pandemic': '#616161'
          }).map(([category, color]) => (
            <span key={category} style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
              <div style={{
                width: '12px',
                height: '12px',
                backgroundColor: color,
                borderRadius: '2px'
              }} />
              {category}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
};

export default PriceChart; 