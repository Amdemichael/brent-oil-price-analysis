import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell
} from 'recharts';

const ImpactAnalysis = ({ data, filters }) => {
  // Filter data based on filters
  let filteredData = data;
  if (filters.category) {
    filteredData = data.filter(item => item.event_category === filters.category);
  }
  if (filters.region) {
    filteredData = data.filter(item => item.region === filters.region);
  }

  // Prepare data for bar chart (top 10 events by absolute impact)
  const barChartData = filteredData
    .map(item => ({
      name: item.event_name.substring(0, 20) + '...',
      impact: Math.abs(item.price_change_pct),
      actual_impact: item.price_change_pct,
      category: item.event_category,
      date: item.event_date
    }))
    .sort((a, b) => b.impact - a.impact)
    .slice(0, 10);

  // Prepare data for pie chart (impact by category)
  const categoryData = filteredData.reduce((acc, item) => {
    const category = item.event_category;
    if (!acc[category]) {
      acc[category] = {
        name: category,
        value: 0,
        count: 0,
        avg_impact: 0
      };
    }
    acc[category].value += Math.abs(item.price_change_pct);
    acc[category].count += 1;
    acc[category].avg_impact += item.price_change_pct;
    return acc;
  }, {});

  const pieChartData = Object.values(categoryData).map(item => ({
    ...item,
    avg_impact: item.avg_impact / item.count
  }));

  // Colors for categories
  const colors = [
    '#8884d8', '#82ca9d', '#ffc658', '#ff7300', '#ff0000',
    '#00ff00', '#0000ff', '#ffff00', '#ff00ff', '#00ffff'
  ];

  // Custom tooltip for bar chart
  const CustomBarTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div style={{
          backgroundColor: 'rgba(255, 255, 255, 0.95)',
          border: '1px solid #ccc',
          borderRadius: '5px',
          padding: '10px',
          boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)'
        }}>
          <p style={{ margin: '0 0 5px 0', fontWeight: 'bold' }}>
            {data.name}
          </p>
          <p style={{ margin: '0', color: '#2a5298' }}>
            Date: {data.date}
          </p>
          <p style={{ margin: '0', color: data.actual_impact > 0 ? '#4caf50' : '#f44336' }}>
            Impact: {data.actual_impact.toFixed(2)}%
          </p>
          <p style={{ margin: '0', fontSize: '12px', color: '#666' }}>
            Category: {data.category}
          </p>
        </div>
      );
    }
    return null;
  };

  // Custom tooltip for pie chart
  const CustomPieTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div style={{
          backgroundColor: 'rgba(255, 255, 255, 0.95)',
          border: '1px solid #ccc',
          borderRadius: '5px',
          padding: '10px',
          boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)'
        }}>
          <p style={{ margin: '0 0 5px 0', fontWeight: 'bold' }}>
            {data.name}
          </p>
          <p style={{ margin: '0', color: '#2a5298' }}>
            Events: {data.count}
          </p>
          <p style={{ margin: '0', color: data.avg_impact > 0 ? '#4caf50' : '#f44336' }}>
            Avg Impact: {data.avg_impact.toFixed(2)}%
          </p>
          <p style={{ margin: '0', fontSize: '12px', color: '#666' }}>
            Total Impact: {data.value.toFixed(2)}%
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <div style={{ width: '100%', height: '400px' }}>
      <ResponsiveContainer width="100%" height="100%">
        <div style={{ display: 'flex', height: '100%' }}>
          {/* Bar Chart - Top Events by Impact */}
          <div style={{ flex: '1', height: '100%' }}>
            <h4 style={{ textAlign: 'center', marginBottom: '10px', color: '#2a5298' }}>
              Top Events by Impact
            </h4>
            <BarChart data={barChartData} layout="horizontal" height={300}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
              <XAxis type="number" tick={{ fontSize: 12 }} />
              <YAxis 
                type="category" 
                dataKey="name" 
                tick={{ fontSize: 10 }}
                width={120}
              />
              <Tooltip content={<CustomBarTooltip />} />
              <Bar 
                dataKey="impact" 
                fill="#2a5298"
                radius={[0, 4, 4, 0]}
              />
            </BarChart>
          </div>

          {/* Pie Chart - Impact by Category */}
          <div style={{ flex: '1', height: '100%' }}>
            <h4 style={{ textAlign: 'center', marginBottom: '10px', color: '#2a5298' }}>
              Impact by Category
            </h4>
            <PieChart height={300}>
              <Pie
                data={pieChartData}
                cx="50%"
                cy="50%"
                outerRadius={80}
                dataKey="value"
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                labelLine={false}
              >
                {pieChartData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={colors[index % colors.length]} />
                ))}
              </Pie>
              <Tooltip content={<CustomPieTooltip />} />
            </PieChart>
          </div>
        </div>
      </ResponsiveContainer>

      {/* Summary Statistics */}
      <div style={{ marginTop: '20px', padding: '15px', backgroundColor: '#f8f9fa', borderRadius: '5px' }}>
        <h5 style={{ marginBottom: '10px', color: '#2a5298' }}>Summary Statistics</h5>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', gap: '10px' }}>
          <div>
            <strong>Total Events:</strong> {filteredData.length}
          </div>
          <div>
            <strong>Avg Impact:</strong> {(filteredData.reduce((sum, item) => sum + item.price_change_pct, 0) / filteredData.length).toFixed(2)}%
          </div>
          <div>
            <strong>Max Positive:</strong> {Math.max(...filteredData.map(item => item.price_change_pct)).toFixed(2)}%
          </div>
          <div>
            <strong>Max Negative:</strong> {Math.min(...filteredData.map(item => item.price_change_pct)).toFixed(2)}%
          </div>
        </div>
      </div>
    </div>
  );
};

export default ImpactAnalysis; 