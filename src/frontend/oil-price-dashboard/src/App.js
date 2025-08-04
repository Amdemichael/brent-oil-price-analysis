import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import PriceChart from './components/Charts/PriceChart';
import EventTimeline from './components/Charts/EventTimeline';
import ImpactAnalysis from './components/Charts/ImpactAnalysis';
import Controls from './components/Controls/Controls';
import InfoPanels from './components/InfoPanels/InfoPanels';

function App() {
  const [priceData, setPriceData] = useState([]);
  const [events, setEvents] = useState([]);
  const [eventImpacts, setEventImpacts] = useState([]);
  const [changePoints, setChangePoints] = useState(null);
  const [dataSummary, setDataSummary] = useState(null);
  const [impactSummary, setImpactSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({
    startDate: null,
    endDate: null,
    category: '',
    region: ''
  });

  // API base URL
  const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

  // Fetch data from API
  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);

      // Fetch all data in parallel
      const [
        summaryResponse,
        pricesResponse,
        eventsResponse,
        impactsResponse,
        impactSummaryResponse
      ] = await Promise.all([
        axios.get(`${API_BASE}/data/summary`),
        axios.get(`${API_BASE}/data/prices`),
        axios.get(`${API_BASE}/events`),
        axios.get(`${API_BASE}/analysis/event-impacts`),
        axios.get(`${API_BASE}/analysis/impact-summary`)
      ]);

      setDataSummary(summaryResponse.data);
      setPriceData(pricesResponse.data);
      setEvents(eventsResponse.data);
      setEventImpacts(impactsResponse.data);
      setImpactSummary(impactSummaryResponse.data);

    } catch (err) {
      console.error('Error fetching data:', err);
      setError('Failed to load data. Please check if the backend server is running.');
    } finally {
      setLoading(false);
    }
  };

  // Fetch filtered data
  const fetchFilteredData = async () => {
    try {
      const params = new URLSearchParams();
      if (filters.startDate) params.append('start_date', filters.startDate);
      if (filters.endDate) params.append('end_date', filters.endDate);
      if (filters.category) params.append('category', filters.category);
      if (filters.region) params.append('region', filters.region);

      const [pricesResponse, eventsResponse] = await Promise.all([
        axios.get(`${API_BASE}/data/prices?${params.toString()}`),
        axios.get(`${API_BASE}/events?${params.toString()}`)
      ]);

      setPriceData(pricesResponse.data);
      setEvents(eventsResponse.data);

    } catch (err) {
      console.error('Error fetching filtered data:', err);
      setError('Failed to apply filters.');
    }
  };

  // Run change point analysis
  const runChangePointAnalysis = async (parameters) => {
    try {
      setLoading(true);
      const response = await axios.post(`${API_BASE}/analysis/run-change-point`, parameters);
      
      if (response.data.status === 'success') {
        // Fetch updated change point results
        const cpResponse = await axios.get(`${API_BASE}/analysis/change-points`);
        setChangePoints(cpResponse.data);
      }
      
      return response.data;
    } catch (err) {
      console.error('Error running change point analysis:', err);
      setError('Failed to run change point analysis.');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Handle filter changes
  const handleFilterChange = (newFilters) => {
    setFilters(newFilters);
  };

  // Load data on component mount
  useEffect(() => {
    fetchData();
  }, []);

  // Apply filters when they change
  useEffect(() => {
    if (!loading) {
      fetchFilteredData();
    }
  }, [filters]);

  if (loading && !priceData.length) {
    return (
      <div className="App">
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>Loading Brent Oil Price Analysis Dashboard...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="App">
        <div className="error-container">
          <h2>Error</h2>
          <p>{error}</p>
          <button onClick={fetchData}>Retry</button>
        </div>
      </div>
    );
  }

  return (
    <div className="App">
      <header className="app-header">
        <h1>Brent Oil Price Analysis Dashboard</h1>
        <p>Analyzing the impact of geopolitical and economic events on oil prices</p>
      </header>

      <main className="app-main">
        <div className="dashboard-grid">
          {/* Controls Section */}
          <div className="controls-section">
            <Controls 
              filters={filters}
              onFilterChange={handleFilterChange}
              onRunAnalysis={runChangePointAnalysis}
              loading={loading}
            />
          </div>

          {/* Info Panels */}
          <div className="info-section">
            <InfoPanels 
              dataSummary={dataSummary}
              impactSummary={impactSummary}
              changePoints={changePoints}
            />
          </div>

          {/* Charts Section */}
          <div className="charts-section">
            <div className="chart-container">
              <h3>Brent Oil Price Timeline</h3>
              <PriceChart 
                data={priceData}
                events={events}
                changePoints={changePoints}
              />
            </div>

            <div className="chart-container">
              <h3>Event Impact Analysis</h3>
              <ImpactAnalysis 
                data={eventImpacts}
                filters={filters}
              />
            </div>

            <div className="chart-container">
              <h3>Key Events Timeline</h3>
              <EventTimeline 
                events={events}
                priceData={priceData}
              />
            </div>
          </div>
        </div>
      </main>

      <footer className="app-footer">
        <p>Birhan Energies - Data-Driven Energy Market Analysis</p>
        <p>© 2025 Brent Oil Price Analysis Project</p>
      </footer>
    </div>
  );
}

export default App;
