"""
Tests for API Endpoints
"""

import pytest
import sys
import os
import json

# Add parent directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app import app


class TestAPIEndpoints:
    """Test cases for API endpoints."""
    
    def setup_method(self):
        """Set up test client."""
        self.client = app.test_client()
        self.client.testing = True
    
    def test_price_data_endpoint(self):
        """Test price data endpoint."""
        response = self.client.get('/api/data/prices')
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        if len(data) > 0:
            assert 'date' in data[0]
            assert 'price' in data[0]
    
    def test_price_data_with_filters(self):
        """Test price data endpoint with date filters."""
        response = self.client.get('/api/data/prices?start_date=2020-01-01&end_date=2020-12-31')
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
    
    def test_events_with_filters(self):
        """Test events endpoint with filters."""
        response = self.client.get('/api/events?category=Military%20Conflict')
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
    
    def test_impact_summary_endpoint(self):
        """Test impact summary endpoint."""
        response = self.client.get('/api/analysis/impact-summary')
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, dict)
    
    def test_event_statistics_endpoint(self):
        """Test event statistics endpoint."""
        response = self.client.get('/api/events/statistics')
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, dict)
    
    def test_change_point_analysis_endpoint(self):
        """Test change point analysis endpoint (should fail without running analysis first)."""
        response = self.client.get('/api/analysis/change-points')
        # This should return an error since no analysis has been run
        assert response.status_code in [400, 404]


if __name__ == '__main__':
    pytest.main([__file__])
