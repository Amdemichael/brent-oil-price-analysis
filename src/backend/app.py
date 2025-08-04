"""
Flask Backend for Brent Oil Price Analysis Dashboard

This module provides the main Flask application that serves the API endpoints
for the interactive dashboard.
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import numpy as np
import json
import sys
import os
from datetime import datetime, timedelta

# Add the parent directory to the path to import analysis modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from analysis.event_research import EventResearch
from analysis.change_point import ChangePointAnalyzer
from analysis.impact_analysis import ImpactAnalyzer

app = Flask(__name__)
CORS(app)

# Global variables to store analysis results
oil_data = None
event_research = None
impact_analyzer = None
change_point_analyzer = None

def load_data():
    """Load and initialize all data and analysis objects."""
    global oil_data, event_research, impact_analyzer, change_point_analyzer
    
    # Load oil price data
    data_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'raw', 'BrentOilPrices.csv')
    oil_data = pd.read_csv(data_path)
    
    # Handle mixed date formats in the data
    def parse_date(date_str):
        """Parse dates with mixed formats"""
        if pd.isna(date_str):
            return pd.NaT
        
        # Remove quotes if present
        date_str = str(date_str).strip().strip('"')
        
        try:
            # Try the original format first (dd-MMM-yy)
            return pd.to_datetime(date_str, format='%d-%b-%y')
        except ValueError:
            try:
                # Try the newer format (MMM dd, yyyy)
                return pd.to_datetime(date_str, format='%b %d, %Y')
            except ValueError:
                # If both fail, let pandas try to infer
                return pd.to_datetime(date_str)
    
    oil_data['Date'] = oil_data['Date'].apply(parse_date)
    oil_data = oil_data.sort_values('Date').reset_index(drop=True)
    
    # Initialize analysis objects
    event_research = EventResearch()
    change_point_analyzer = ChangePointAnalyzer(oil_data)
    impact_analyzer = ImpactAnalyzer(oil_data, event_research)
    
    print("Data loaded successfully!")
    print(f"Date range: {oil_data['Date'].min()} to {oil_data['Date'].max()}")
    print(f"Total records: {len(oil_data)}")

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'message': 'Brent Oil Analysis API is running'})

@app.route('/api/data/summary', methods=['GET'])
def get_data_summary():
    """Get summary statistics of the oil price data."""
    if oil_data is None:
        load_data()
    
    summary = {
        'total_records': len(oil_data),
        'date_range': {
            'start': oil_data['Date'].min().strftime('%Y-%m-%d'),
            'end': oil_data['Date'].max().strftime('%Y-%m-%d')
        },
        'price_stats': {
            'min': float(oil_data['Price'].min()),
            'max': float(oil_data['Price'].max()),
            'mean': float(oil_data['Price'].mean()),
            'median': float(oil_data['Price'].median()),
            'std': float(oil_data['Price'].std())
        }
    }
    
    return jsonify(summary)

@app.route('/api/data/prices', methods=['GET'])
def get_price_data():
    """Get oil price data with optional date filtering."""
    if oil_data is None:
        load_data()
    
    # Get query parameters
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # Filter data if dates provided
    filtered_data = oil_data.copy()
    
    if start_date:
        start_dt = pd.to_datetime(start_date)
        filtered_data = filtered_data[filtered_data['Date'] >= start_dt]
    
    if end_date:
        end_dt = pd.to_datetime(end_date)
        filtered_data = filtered_data[filtered_data['Date'] <= end_dt]
    
    # Convert to JSON-serializable format
    price_data = []
    for _, row in filtered_data.iterrows():
        price_data.append({
            'date': row['Date'].strftime('%Y-%m-%d'),
            'price': float(row['Price'])
        })
    
    return jsonify(price_data)

@app.route('/api/events', methods=['GET'])
def get_events():
    """Get all events or filter by parameters."""
    if event_research is None:
        load_data()
    
    # Get query parameters
    category = request.args.get('category')
    region = request.args.get('region')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    events = event_research.get_all_events()
    
    # Apply filters
    if category:
        events = events[events['category'] == category]
    
    if region:
        events = events[events['region'] == region]
    
    if start_date:
        start_dt = pd.to_datetime(start_date)
        events = events[events['date'] >= start_dt]
    
    if end_date:
        end_dt = pd.to_datetime(end_date)
        events = events[events['date'] <= end_dt]
    
    # Convert to JSON-serializable format
    events_data = []
    for _, event in events.iterrows():
        events_data.append({
            'date': event['date'].strftime('%Y-%m-%d'),
            'event': event['event'],
            'category': event['category'],
            'description': event['description'],
            'expected_impact': event['expected_impact'],
            'region': event['region']
        })
    
    return jsonify(events_data)

@app.route('/api/events/categories', methods=['GET'])
def get_event_categories():
    """Get all event categories."""
    if event_research is None:
        load_data()
    
    events = event_research.get_all_events()
    categories = events['category'].unique().tolist()
    
    return jsonify(categories)

@app.route('/api/events/regions', methods=['GET'])
def get_event_regions():
    """Get all event regions."""
    if event_research is None:
        load_data()
    
    events = event_research.get_all_events()
    regions = events['region'].unique().tolist()
    
    return jsonify(regions)

@app.route('/api/analysis/change-points', methods=['GET'])
def get_change_points():
    """Get change point analysis results."""
    if change_point_analyzer is None:
        load_data()
    
    # Check if model has been fitted
    if change_point_analyzer.trace is None:
        return jsonify({'error': 'Change point model not fitted. Run analysis first.'}), 400
    
    # Get change point results
    change_points = change_point_analyzer.change_points
    
    if change_points is None:
        return jsonify({'error': 'Change point analysis not completed.'}), 400
    
    result = {
        'change_point_date': change_points['change_point_date'].strftime('%Y-%m-%d'),
        'price_change_usd': float(change_points['price_change']),
        'price_change_pct': float(change_points['price_change_pct']),
        'volatility_change': float(change_points['volatility_change']),
        'before_stats': {
            'mean_price': float(change_points['before_stats']['mean_price']),
            'volatility': float(change_points['before_stats']['mean_volatility'])
        },
        'after_stats': {
            'mean_price': float(change_points['after_stats']['mean_price']),
            'volatility': float(change_points['after_stats']['mean_volatility'])
        }
    }
    
    return jsonify(result)

@app.route('/api/analysis/event-impacts', methods=['GET'])
def get_event_impacts():
    """Get event impact analysis results."""
    if impact_analyzer is None:
        load_data()
    
    # Get all event impacts
    impacts = impact_analyzer.analyze_all_events()
    
    # Convert to JSON-serializable format
    impacts_data = []
    for _, impact in impacts.iterrows():
        impacts_data.append({
            'event_date': impact['event_date'].strftime('%Y-%m-%d'),
            'event_name': impact['event_name'],
            'event_category': impact['event_category'],
            'expected_impact': impact['expected_impact'],
            'region': impact['region'],
            'price_change_usd': float(impact['price_change_usd']),
            'price_change_pct': float(impact['price_change_pct']),
            'volatility_change': float(impact['volatility_change']),
            'before_mean_price': float(impact['before_mean_price']),
            'after_mean_price': float(impact['after_mean_price'])
        })
    
    return jsonify(impacts_data)

@app.route('/api/analysis/impact-summary', methods=['GET'])
def get_impact_summary():
    """Get summary statistics of event impacts."""
    if impact_analyzer is None:
        load_data()
    
    summary = impact_analyzer.get_impact_summary()
    
    return jsonify(summary)

@app.route('/api/analysis/run-change-point', methods=['POST'])
def run_change_point_analysis():
    """Run change point analysis with specified parameters."""
    if change_point_analyzer is None:
        load_data()
    
    try:
        # Get parameters from request
        data = request.get_json()
        n_changepoints = data.get('n_changepoints', 1)
        draws = data.get('draws', 1000)
        tune = data.get('tune', 500)
        chains = data.get('chains', 2)
        
        # Run analysis
        trace = change_point_analyzer.fit_model(
            n_changepoints=n_changepoints,
            draws=draws,
            tune=tune,
            chains=chains
        )
        
        # Analyze results
        change_points = change_point_analyzer.analyze_change_points()
        
        result = {
            'status': 'success',
            'message': 'Change point analysis completed successfully',
            'converged': change_point_analyzer.check_convergence(),
            'change_point_date': change_points['change_point_date'].strftime('%Y-%m-%d'),
            'price_change_pct': float(change_points['price_change_pct'])
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analysis/event-impact/<event_date>', methods=['GET'])
def get_specific_event_impact(event_date):
    """Get impact analysis for a specific event."""
    if impact_analyzer is None:
        load_data()
    
    try:
        # Get window size from query parameters
        window_days = int(request.args.get('window_days', 30))
        
        # Analyze event impact
        impact = impact_analyzer.analyze_event_impact(event_date, window_days)
        
        result = {
            'event_date': impact['event_date'],
            'analysis_window': impact['analysis_window'],
            'price_change': float(impact['price_change']),
            'price_change_pct': float(impact['price_change_pct']),
            'volatility_change': float(impact['volatility_change']),
            'before_stats': {
                'mean_price': float(impact['before_stats']['mean_price']),
                'std_price': float(impact['before_stats']['std_price']),
                'min_price': float(impact['before_stats']['min_price']),
                'max_price': float(impact['before_stats']['max_price'])
            },
            'after_stats': {
                'mean_price': float(impact['after_stats']['mean_price']),
                'std_price': float(impact['after_stats']['std_price']),
                'min_price': float(impact['after_stats']['min_price']),
                'max_price': float(impact['after_stats']['max_price'])
            }
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/events/statistics', methods=['GET'])
def get_event_statistics():
    """Get statistics about the events database."""
    if event_research is None:
        load_data()
    
    stats = event_research.get_event_statistics()
    
    return jsonify(stats)

if __name__ == '__main__':
    # Load data on startup
    load_data()
    
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)
