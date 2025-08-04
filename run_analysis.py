#!/usr/bin/env python3
"""
Analysis Pipeline Script

This script runs the complete Brent oil price analysis pipeline.
"""

import sys
import os

# Add src to path
sys.path.append('src')

from analysis.event_research import EventResearch
from analysis.change_point import ChangePointAnalyzer
from analysis.impact_analysis import ImpactAnalyzer
import pandas as pd

def main():
    """Run the complete analysis pipeline."""
    
    print('Loading data...')
    data = pd.read_csv('data/raw/BrentOilPrices.csv')
    
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
    
    data['Date'] = data['Date'].apply(parse_date)
    
    print('Initializing analysis...')
    event_research = EventResearch()
    change_point_analyzer = ChangePointAnalyzer(data)
    impact_analyzer = ImpactAnalyzer(data, event_research)
    
    print('Running change point analysis...')
    trace = change_point_analyzer.fit_model(draws=1000, tune=500, chains=2)
    change_points = change_point_analyzer.analyze_change_points()
    
    print('Running impact analysis...')
    impacts = impact_analyzer.analyze_all_events()
    
    print('Exporting results...')
    # Create outputs directory if it doesn't exist
    os.makedirs('data/outputs', exist_ok=True)
    
    change_point_analyzer.export_results('data/outputs/change_point_results.csv')
    impact_analyzer.export_impact_analysis('data/outputs/event_impacts.csv')
    
    print('Analysis complete! Results saved to data/outputs/')

if __name__ == '__main__':
    main() 