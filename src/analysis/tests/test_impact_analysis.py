"""
Tests for Impact Analysis Module
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime
import sys
import os

# Add parent directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from analysis.impact_analysis import ImpactAnalyzer
from analysis.event_research import EventResearch


class TestImpactAnalyzer:
    """Test cases for ImpactAnalyzer class."""
    
    def setup_method(self):
        """Set up test data."""
        # Create sample data
        dates = pd.date_range('2020-01-01', periods=100, freq='D')
        prices = np.random.normal(50, 10, 100)
        self.test_data = pd.DataFrame({
            'Date': dates,
            'Price': prices
        })
        self.event_research = EventResearch()
        self.analyzer = ImpactAnalyzer(self.test_data, self.event_research)
    
    def test_initialization(self):
        """Test that the analyzer initializes correctly."""
        assert self.analyzer.oil_data is not None
        assert self.analyzer.event_research is not None
        assert len(self.analyzer.oil_data) == 100
    
    def test_analyze_event_impact(self):
        """Test event impact analysis."""
        impact = self.analyzer.analyze_event_impact('2020-02-01', window_days=10)
        assert 'event_date' in impact
        assert 'price_change' in impact
        assert 'price_change_pct' in impact
        assert 'before_stats' in impact
        assert 'after_stats' in impact
    
    def test_analyze_all_events(self):
        """Test analysis of all events."""
        impacts = self.analyzer.analyze_all_events()
        assert isinstance(impacts, pd.DataFrame)
        assert not impacts.empty
    
    def test_get_impact_summary(self):
        """Test impact summary generation."""
        summary = self.analyzer.get_impact_summary()
        assert 'total_events' in summary
        assert 'average_price_change' in summary


if __name__ == '__main__':
    pytest.main([__file__])
