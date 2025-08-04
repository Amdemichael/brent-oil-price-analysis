"""
Tests for Change Point Analysis Module
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime
import sys
import os

# Add parent directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from analysis.change_point import ChangePointAnalyzer


class TestChangePointAnalyzer:
    """Test cases for ChangePointAnalyzer class."""
    
    def setup_method(self):
        """Set up test data."""
        # Create sample data
        dates = pd.date_range('2020-01-01', periods=100, freq='D')
        prices = np.random.normal(50, 10, 100)
        self.test_data = pd.DataFrame({
            'Date': dates,
            'Price': prices
        })
        self.analyzer = ChangePointAnalyzer(self.test_data)
    
    def test_initialization(self):
        """Test that the analyzer initializes correctly."""
        assert self.analyzer.data is not None
        assert len(self.analyzer.data) == 99  # One row dropped due to log returns calculation
        assert 'log_returns' in self.analyzer.data.columns
    
    def test_build_model(self):
        """Test model building."""
        model = self.analyzer.build_model()
        assert model is not None
    
    def test_data_loading(self):
        """Test that data loads correctly."""
        assert not self.analyzer.data.empty
        assert 'Date' in self.analyzer.data.columns
        assert 'Price' in self.analyzer.data.columns
        assert 'log_returns' in self.analyzer.data.columns


if __name__ == '__main__':
    pytest.main([__file__])
