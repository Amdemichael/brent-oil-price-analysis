import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine
} from 'recharts';

const EventTimeline = ({ events, priceData }) => {
  // Transform price data for charting
  const chartData = priceData.map(item => ({
    date: item.date,
    price: item.price,
    name: item.date
  }));

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

  // Custom tooltip
  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      const eventsOnDate = events.filter(event => event.date === label);
      
      return (
        <div style={{
          backgroundColor: 'rgba(255, 255, 255, 0.95)',
          border: '1px solid #ccc',
          borderRadius: '5px',
          padding: '10px',
          boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)',
          maxWidth: '300px'
        }}>
          <p style={{ margin: '0 0 5px 0', fontWeight: 'bold' }}>
            {label}
          </p>
          <p style={{ margin: '0', color: '#2a5298' }}>
            Price: ${payload[0].value.toFixed(2)}
          </p>
          
          {eventsOnDate.length > 0 && (
            <div style={{ marginTop: '10px' }}>
              <p style={{ margin: '0 0 5px 0', fontWeight: 'bold', fontSize: '12px' }}>
                Events on this date:
              </p>
              {eventsOnDate.map((event, index) => (
                <div key={index} style={{ 
                  marginBottom: '5px', 
                  padding: '5px', 
                  backgroundColor: '#f0f0f0', 
                  borderRadius: '3px',
                  borderLeft: `3px solid ${getEventColor(event.category)}`
                }}>
                  <p style={{ margin: '0', fontSize: '11px', fontWeight: 'bold' }}>
                    {event.event}
                  </p>
                  <p style={{ margin: '0', fontSize: '10px', color: '#666' }}>
                    {event.category} - {event.expected_impact}
                  </p>
                  <p style={{ margin: '0', fontSize: '10px', color: '#666' }}>
                    Region: {event.region}
                  </p>
                </div>
              ))}
            </div>
          )}
        </div>
      );
    }
    return null;
  };

  // Group events by year for better visualization
  const eventsByYear = events.reduce((acc, event) => {
    const year = new Date(event.date).getFullYear();
    if (!acc[year]) {
      acc[year] = [];
    }
    acc[year].push(event);
    return acc;
  }, {});

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
                year: 'numeric'
              });
            }}
          />
          <YAxis 
            tick={{ fontSize: 12 }}
            tickFormatter={(value) => `$${value}`}
          />
          <Tooltip content={<CustomTooltip />} />
          
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
          {events.map((event, index) => (
            <ReferenceLine
              key={index}
              x={event.date}
              stroke={getEventColor(event.category)}
              strokeDasharray="5 5"
              strokeWidth={2}
              label={{
                value: event.event.substring(0, 15) + '...',
                position: 'top',
                fontSize: 8,
                fill: getEventColor(event.category),
                angle: -45
              }}
            />
          ))}
        </LineChart>
      </ResponsiveContainer>
      
      {/* Event Legend */}
      <div style={{ marginTop: '15px' }}>
        <h5 style={{ marginBottom: '10px', color: '#2a5298', fontSize: '14px' }}>
          Event Categories by Year
        </h5>
        <div style={{ 
          display: 'grid', 
          gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', 
          gap: '10px',
          fontSize: '11px'
        }}>
          {Object.entries(eventsByYear).map(([year, yearEvents]) => (
            <div key={year} style={{ 
              padding: '8px', 
              backgroundColor: '#f8f9fa', 
              borderRadius: '4px',
              border: '1px solid #e9ecef'
            }}>
              <strong style={{ color: '#2a5298' }}>{year}</strong>
              <div style={{ marginTop: '5px' }}>
                {yearEvents.map((event, index) => (
                  <div key={index} style={{ 
                    display: 'flex', 
                    alignItems: 'center', 
                    marginBottom: '3px',
                    fontSize: '10px'
                  }}>
                    <div style={{
                      width: '8px',
                      height: '8px',
                      backgroundColor: getEventColor(event.category),
                      borderRadius: '50%',
                      marginRight: '5px'
                    }} />
                    <span style={{ flex: 1 }}>{event.event}</span>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default EventTimeline; 