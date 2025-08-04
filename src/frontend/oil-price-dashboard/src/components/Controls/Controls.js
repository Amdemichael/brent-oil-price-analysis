import React, { useState, useEffect } from 'react';
import axios from 'axios';
import DatePicker from 'react-datepicker';
import Select from 'react-select';
import 'react-datepicker/dist/react-datepicker.css';

const Controls = ({ filters, onFilterChange, onRunAnalysis, loading }) => {
  const [categories, setCategories] = useState([]);
  const [regions, setRegions] = useState([]);
  const [analysisParams, setAnalysisParams] = useState({
    n_changepoints: 1,
    draws: 1000,
    tune: 500,
    chains: 2
  });

  const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

  // Fetch filter options
  useEffect(() => {
    const fetchOptions = async () => {
      try {
        const [categoriesRes, regionsRes] = await Promise.all([
          axios.get(`${API_BASE}/events/categories`),
          axios.get(`${API_BASE}/events/regions`)
        ]);
        
        setCategories(categoriesRes.data.map(cat => ({ value: cat, label: cat })));
        setRegions(regionsRes.data.map(region => ({ value: region, label: region })));
      } catch (error) {
        console.error('Error fetching filter options:', error);
      }
    };

    fetchOptions();
  }, [API_BASE]);

  // Handle date changes
  const handleStartDateChange = (date) => {
    onFilterChange({
      ...filters,
      startDate: date ? date.toISOString().split('T')[0] : null
    });
  };

  const handleEndDateChange = (date) => {
    onFilterChange({
      ...filters,
      endDate: date ? date.toISOString().split('T')[0] : null
    });
  };

  // Handle select changes
  const handleCategoryChange = (selected) => {
    onFilterChange({
      ...filters,
      category: selected ? selected.value : ''
    });
  };

  const handleRegionChange = (selected) => {
    onFilterChange({
      ...filters,
      region: selected ? selected.value : ''
    });
  };

  // Handle analysis parameter changes
  const handleAnalysisParamChange = (param, value) => {
    setAnalysisParams({
      ...analysisParams,
      [param]: parseInt(value)
    });
  };

  // Run change point analysis
  const handleRunAnalysis = async () => {
    try {
      await onRunAnalysis(analysisParams);
    } catch (error) {
      console.error('Error running analysis:', error);
    }
  };

  // Clear all filters
  const clearFilters = () => {
    onFilterChange({
      startDate: null,
      endDate: null,
      category: '',
      region: ''
    });
  };

  return (
    <div className="controls">
      <h3 style={{ marginBottom: '20px', color: '#2a5298' }}>Controls</h3>
      
      {/* Date Range Filters */}
      <div style={{ marginBottom: '20px' }}>
        <h4 style={{ marginBottom: '10px', fontSize: '14px', color: '#666' }}>Date Range</h4>
        <div style={{ marginBottom: '10px' }}>
          <label style={{ display: 'block', marginBottom: '5px', fontSize: '12px' }}>
            Start Date:
          </label>
          <DatePicker
            selected={filters.startDate ? new Date(filters.startDate) : null}
            onChange={handleStartDateChange}
            dateFormat="yyyy-MM-dd"
            placeholderText="Select start date"
            className="date-picker"
            style={{ width: '100%', padding: '8px', border: '1px solid #ddd', borderRadius: '4px' }}
          />
        </div>
        <div style={{ marginBottom: '10px' }}>
          <label style={{ display: 'block', marginBottom: '5px', fontSize: '12px' }}>
            End Date:
          </label>
          <DatePicker
            selected={filters.endDate ? new Date(filters.endDate) : null}
            onChange={handleEndDateChange}
            dateFormat="yyyy-MM-dd"
            placeholderText="Select end date"
            className="date-picker"
            style={{ width: '100%', padding: '8px', border: '1px solid #ddd', borderRadius: '4px' }}
          />
        </div>
      </div>

      {/* Category Filter */}
      <div style={{ marginBottom: '20px' }}>
        <h4 style={{ marginBottom: '10px', fontSize: '14px', color: '#666' }}>Event Category</h4>
        <Select
          value={categories.find(cat => cat.value === filters.category)}
          onChange={handleCategoryChange}
          options={categories}
          placeholder="Select category"
          isClearable
          styles={{
            control: (provided) => ({
              ...provided,
              minHeight: '35px',
              fontSize: '12px'
            })
          }}
        />
      </div>

      {/* Region Filter */}
      <div style={{ marginBottom: '20px' }}>
        <h4 style={{ marginBottom: '10px', fontSize: '14px', color: '#666' }}>Region</h4>
        <Select
          value={regions.find(region => region.value === filters.region)}
          onChange={handleRegionChange}
          options={regions}
          placeholder="Select region"
          isClearable
          styles={{
            control: (provided) => ({
              ...provided,
              minHeight: '35px',
              fontSize: '12px'
            })
          }}
        />
      </div>

      {/* Clear Filters Button */}
      <div style={{ marginBottom: '30px' }}>
        <button
          onClick={clearFilters}
          style={{
            width: '100%',
            padding: '8px',
            backgroundColor: '#6c757d',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
            fontSize: '12px'
          }}
        >
          Clear All Filters
        </button>
      </div>

      {/* Change Point Analysis Controls */}
      <div style={{ marginBottom: '20px' }}>
        <h4 style={{ marginBottom: '10px', fontSize: '14px', color: '#666' }}>
          Change Point Analysis
        </h4>
        
        <div style={{ marginBottom: '10px' }}>
          <label style={{ display: 'block', marginBottom: '5px', fontSize: '12px' }}>
            Number of Change Points:
          </label>
          <select
            value={analysisParams.n_changepoints}
            onChange={(e) => handleAnalysisParamChange('n_changepoints', e.target.value)}
            style={{ width: '100%', padding: '8px', border: '1px solid #ddd', borderRadius: '4px', fontSize: '12px' }}
          >
            <option value={1}>1</option>
            <option value={2}>2</option>
            <option value={3}>3</option>
          </select>
        </div>

        <div style={{ marginBottom: '10px' }}>
          <label style={{ display: 'block', marginBottom: '5px', fontSize: '12px' }}>
            MCMC Draws:
          </label>
          <select
            value={analysisParams.draws}
            onChange={(e) => handleAnalysisParamChange('draws', e.target.value)}
            style={{ width: '100%', padding: '8px', border: '1px solid #ddd', borderRadius: '4px', fontSize: '12px' }}
          >
            <option value={500}>500 (Fast)</option>
            <option value={1000}>1000 (Standard)</option>
            <option value={2000}>2000 (Accurate)</option>
          </select>
        </div>

        <div style={{ marginBottom: '10px' }}>
          <label style={{ display: 'block', marginBottom: '5px', fontSize: '12px' }}>
            Tune Steps:
          </label>
          <select
            value={analysisParams.tune}
            onChange={(e) => handleAnalysisParamChange('tune', e.target.value)}
            style={{ width: '100%', padding: '8px', border: '1px solid #ddd', borderRadius: '4px', fontSize: '12px' }}
          >
            <option value={250}>250</option>
            <option value={500}>500</option>
            <option value={1000}>1000</option>
          </select>
        </div>

        <div style={{ marginBottom: '20px' }}>
          <label style={{ display: 'block', marginBottom: '5px', fontSize: '12px' }}>
            MCMC Chains:
          </label>
          <select
            value={analysisParams.chains}
            onChange={(e) => handleAnalysisParamChange('chains', e.target.value)}
            style={{ width: '100%', padding: '8px', border: '1px solid #ddd', borderRadius: '4px', fontSize: '12px' }}
          >
            <option value={2}>2</option>
            <option value={4}>4</option>
          </select>
        </div>

        <button
          onClick={handleRunAnalysis}
          disabled={loading}
          style={{
            width: '100%',
            padding: '12px',
            backgroundColor: loading ? '#ccc' : '#2a5298',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: loading ? 'not-allowed' : 'pointer',
            fontSize: '14px',
            fontWeight: 'bold'
          }}
        >
          {loading ? 'Running Analysis...' : 'Run Change Point Analysis'}
        </button>
      </div>

      {/* Information Panel */}
      <div style={{ 
        padding: '15px', 
        backgroundColor: '#f8f9fa', 
        borderRadius: '5px',
        fontSize: '12px',
        color: '#666'
      }}>
        <h5 style={{ marginBottom: '10px', color: '#2a5298' }}>Analysis Info</h5>
        <p style={{ marginBottom: '8px' }}>
          <strong>Change Point Analysis:</strong> Uses Bayesian inference to identify when oil price behavior fundamentally changes.
        </p>
        <p style={{ marginBottom: '8px' }}>
          <strong>MCMC Sampling:</strong> Monte Carlo Markov Chain sampling for robust parameter estimation.
        </p>
        <p style={{ marginBottom: '8px' }}>
          <strong>Convergence:</strong> Model checks for convergence using R-hat diagnostics.
        </p>
        <p style={{ marginBottom: '0' }}>
          <strong>Note:</strong> Analysis may take several minutes depending on parameters.
        </p>
      </div>
    </div>
  );
};

export default Controls; 