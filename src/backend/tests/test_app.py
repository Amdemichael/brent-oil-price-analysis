"""
Tests for Flask Application
"""

import pytest
import sys
import os
from flask import Flask

# Add parent directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app import app


class TestFlaskApp:
    """Test cases for Flask application."""
    
    def setup_method(self):
        """Set up test client."""
        self.client = app.test_client()
        self.client.testing = True
    
    def test_health_endpoint(self):
        """Test health check endpoint."""
        response = self.client.get('/api/health')
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'healthy'
    
    def test_data_summary_endpoint(self):
        """Test data summary endpoint."""
        response = self.client.get('/api/data/summary')
        assert response.status_code == 200
        data = response.get_json()
        assert 'total_records' in data
        assert 'date_range' in data
        assert 'price_stats' in data
    
    def test_events_endpoint(self):
        """Test events endpoint."""
        response = self.client.get('/api/events')
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
    
    def test_event_categories_endpoint(self):
        """Test event categories endpoint."""
        response = self.client.get('/api/events/categories')
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
    
    def test_event_regions_endpoint(self):
        """Test event regions endpoint."""
        response = self.client.get('/api/events/regions')
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)


if __name__ == '__main__':
    pytest.main([__file__])
