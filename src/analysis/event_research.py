"""
Event Research Module for Brent Oil Price Analysis

This module compiles and structures major geopolitical events that have affected
Brent oil prices from 1987-2022. It provides functions to load, validate, and
analyze event data for correlation with price changes.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EventResearch:
    """
    Class for managing and analyzing geopolitical events affecting oil prices.
    """
    
    def __init__(self):
        """Initialize the EventResearch class."""
        self.events_df = None
        self.event_categories = {
            'OPEC': 'OPEC decisions and meetings',
            'CONFLICT': 'Geopolitical conflicts and wars',
            'SANCTIONS': 'Economic sanctions',
            'ECONOMIC': 'Economic shocks and crises',
            'INFRASTRUCTURE': 'Infrastructure and supply chain events',
            'POLITICAL': 'Political decisions and elections'
        }
    
    def compile_historical_events(self) -> pd.DataFrame:
        """
        Compile a comprehensive dataset of major events affecting oil prices.
        
        Returns:
            pd.DataFrame: Structured event dataset with dates and descriptions
        """
        events_data = [
            # Gulf War and Middle East Conflicts
            {'date': '1990-08-02', 'event_type': 'CONFLICT', 'description': 'Iraq invades Kuwait', 
             'region': 'Middle East', 'impact_expected': 'POSITIVE', 'source': 'Historical Records'},
            {'date': '1991-01-17', 'event_type': 'CONFLICT', 'description': 'Gulf War begins', 
             'region': 'Middle East', 'impact_expected': 'POSITIVE', 'source': 'Historical Records'},
            {'date': '1991-02-28', 'event_type': 'CONFLICT', 'description': 'Gulf War ends', 
             'region': 'Middle East', 'impact_expected': 'NEGATIVE', 'source': 'Historical Records'},
            
            # OPEC Decisions
            {'date': '1998-03-30', 'event_type': 'OPEC', 'description': 'OPEC production cut agreement', 
             'region': 'Global', 'impact_expected': 'POSITIVE', 'source': 'OPEC Records'},
            {'date': '2000-03-29', 'event_type': 'OPEC', 'description': 'OPEC increases production', 
             'region': 'Global', 'impact_expected': 'NEGATIVE', 'source': 'OPEC Records'},
            {'date': '2001-01-17', 'event_type': 'OPEC', 'description': 'OPEC cuts production by 1.5M bpd', 
             'region': 'Global', 'impact_expected': 'POSITIVE', 'source': 'OPEC Records'},
            {'date': '2008-09-10', 'event_type': 'OPEC', 'description': 'OPEC cuts production by 520K bpd', 
             'region': 'Global', 'impact_expected': 'POSITIVE', 'source': 'OPEC Records'},
            {'date': '2014-11-27', 'event_type': 'OPEC', 'description': 'OPEC maintains production despite oversupply', 
             'region': 'Global', 'impact_expected': 'NEGATIVE', 'source': 'OPEC Records'},
            {'date': '2016-11-30', 'event_type': 'OPEC', 'description': 'OPEC+ agrees to cut production by 1.2M bpd', 
             'region': 'Global', 'impact_expected': 'POSITIVE', 'source': 'OPEC Records'},
            {'date': '2020-04-12', 'event_type': 'OPEC', 'description': 'OPEC+ agrees to cut production by 9.7M bpd', 
             'region': 'Global', 'impact_expected': 'POSITIVE', 'source': 'OPEC Records'},
            
            # Economic Crises
            {'date': '2008-09-15', 'event_type': 'ECONOMIC', 'description': 'Lehman Brothers bankruptcy', 
             'region': 'Global', 'impact_expected': 'NEGATIVE', 'source': 'Financial Records'},
            {'date': '2008-10-03', 'event_type': 'ECONOMIC', 'description': 'US financial crisis deepens', 
             'region': 'Global', 'impact_expected': 'NEGATIVE', 'source': 'Financial Records'},
            {'date': '2020-03-11', 'event_type': 'ECONOMIC', 'description': 'COVID-19 declared pandemic', 
             'region': 'Global', 'impact_expected': 'NEGATIVE', 'source': 'WHO Records'},
            {'date': '2020-03-20', 'event_type': 'ECONOMIC', 'description': 'Global lockdowns begin', 
             'region': 'Global', 'impact_expected': 'NEGATIVE', 'source': 'Government Records'},
            
            # Iraq War and Middle East Tensions
            {'date': '2003-03-20', 'event_type': 'CONFLICT', 'description': 'Iraq War begins', 
             'region': 'Middle East', 'impact_expected': 'POSITIVE', 'source': 'Historical Records'},
            {'date': '2003-05-01', 'event_type': 'CONFLICT', 'description': 'Iraq War major combat ends', 
             'region': 'Middle East', 'impact_expected': 'NEGATIVE', 'source': 'Historical Records'},
            {'date': '2011-02-15', 'event_type': 'CONFLICT', 'description': 'Arab Spring begins', 
             'region': 'Middle East', 'impact_expected': 'POSITIVE', 'source': 'Historical Records'},
            {'date': '2014-06-29', 'event_type': 'CONFLICT', 'description': 'ISIS declares caliphate', 
             'region': 'Middle East', 'impact_expected': 'POSITIVE', 'source': 'Historical Records'},
            
            # Sanctions
            {'date': '2012-07-01', 'event_type': 'SANCTIONS', 'description': 'EU oil embargo on Iran', 
             'region': 'Middle East', 'impact_expected': 'POSITIVE', 'source': 'EU Records'},
            {'date': '2014-07-17', 'event_type': 'SANCTIONS', 'description': 'US sanctions on Russia', 
             'region': 'Europe', 'impact_expected': 'POSITIVE', 'source': 'US Records'},
            {'date': '2018-05-08', 'event_type': 'SANCTIONS', 'description': 'US withdraws from Iran nuclear deal', 
             'region': 'Middle East', 'impact_expected': 'POSITIVE', 'source': 'US Records'},
            {'date': '2019-01-28', 'event_type': 'SANCTIONS', 'description': 'US sanctions on Venezuela', 
             'region': 'South America', 'impact_expected': 'POSITIVE', 'source': 'US Records'},
            
            # Infrastructure and Supply Chain
            {'date': '2005-08-29', 'event_type': 'INFRASTRUCTURE', 'description': 'Hurricane Katrina hits Gulf Coast', 
             'region': 'North America', 'impact_expected': 'POSITIVE', 'source': 'Weather Records'},
            {'date': '2010-04-20', 'event_type': 'INFRASTRUCTURE', 'description': 'Deepwater Horizon oil spill', 
             'region': 'North America', 'impact_expected': 'POSITIVE', 'source': 'Environmental Records'},
            {'date': '2019-09-14', 'event_type': 'INFRASTRUCTURE', 'description': 'Drone attack on Saudi oil facilities', 
             'region': 'Middle East', 'impact_expected': 'POSITIVE', 'source': 'News Records'},
            
            # Political Events
            {'date': '2016-11-08', 'event_type': 'POLITICAL', 'description': 'US Presidential election', 
             'region': 'North America', 'impact_expected': 'MIXED', 'source': 'Election Records'},
            {'date': '2020-11-03', 'event_type': 'POLITICAL', 'description': 'US Presidential election', 
             'region': 'North America', 'impact_expected': 'MIXED', 'source': 'Election Records'},
            
            # Recent Conflicts
            {'date': '2022-02-24', 'event_type': 'CONFLICT', 'description': 'Russia invades Ukraine', 
             'region': 'Europe', 'impact_expected': 'POSITIVE', 'source': 'News Records'},
            {'date': '2022-03-08', 'event_type': 'SANCTIONS', 'description': 'US bans Russian oil imports', 
             'region': 'Europe', 'impact_expected': 'POSITIVE', 'source': 'US Records'},
        ]
        
        # Convert to DataFrame
        self.events_df = pd.DataFrame(events_data)
        self.events_df['date'] = pd.to_datetime(self.events_df['date'])
        
        # Add additional metadata
        self.events_df['year'] = self.events_df['date'].dt.year
        self.events_df['month'] = self.events_df['date'].dt.month
        self.events_df['day_of_week'] = self.events_df['date'].dt.dayofweek
        
        logger.info(f"Compiled {len(self.events_df)} historical events")
        return self.events_df
    
    def validate_event_data(self) -> Dict[str, any]:
        """
        Validate the compiled event data for completeness and consistency.
        
        Returns:
            Dict: Validation results and statistics
        """
        if self.events_df is None:
            raise ValueError("Event data not compiled. Run compile_historical_events() first.")
        
        validation_results = {
            'total_events': len(self.events_df),
            'date_range': {
                'start': self.events_df['date'].min(),
                'end': self.events_df['date'].max()
            },
            'event_types': self.events_df['event_type'].value_counts().to_dict(),
            'regions': self.events_df['region'].value_counts().to_dict(),
            'impact_distribution': self.events_df['impact_expected'].value_counts().to_dict(),
            'missing_values': self.events_df.isnull().sum().to_dict(),
            'duplicate_dates': self.events_df['date'].duplicated().sum()
        }
        
        logger.info("Event data validation completed")
        return validation_results
    
    def get_events_by_type(self, event_type: str) -> pd.DataFrame:
        """
        Filter events by type.
        
        Args:
            event_type: Type of event to filter by
            
        Returns:
            pd.DataFrame: Filtered events
        """
        if self.events_df is None:
            raise ValueError("Event data not compiled. Run compile_historical_events() first.")
        
        return self.events_df[self.events_df['event_type'] == event_type]
    
    def get_events_by_date_range(self, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Filter events by date range.
        
        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            
        Returns:
            pd.DataFrame: Filtered events
        """
        if self.events_df is None:
            raise ValueError("Event data not compiled. Run compile_historical_events() first.")
        
        start_dt = pd.to_datetime(start_date)
        end_dt = pd.to_datetime(end_date)
        
        mask = (self.events_df['date'] >= start_dt) & (self.events_df['date'] <= end_dt)
        return self.events_df[mask]
    
    def calculate_event_density(self, window_days: int = 30) -> pd.DataFrame:
        """
        Calculate event density over time windows.
        
        Args:
            window_days: Number of days for rolling window
            
        Returns:
            pd.DataFrame: Event density over time
        """
        if self.events_df is None:
            raise ValueError("Event data not compiled. Run compile_historical_events() first.")
        
        # Create date range for the entire period
        date_range = pd.date_range(
            start=self.events_df['date'].min(),
            end=self.events_df['date'].max(),
            freq='D'
        )
        
        # Count events in rolling windows
        event_counts = []
        for date in date_range:
            window_start = date - timedelta(days=window_days//2)
            window_end = date + timedelta(days=window_days//2)
            
            events_in_window = self.events_df[
                (self.events_df['date'] >= window_start) & 
                (self.events_df['date'] <= window_end)
            ]
            
            event_counts.append({
                'date': date,
                'event_count': len(events_in_window),
                'conflict_events': len(events_in_window[events_in_window['event_type'] == 'CONFLICT']),
                'opec_events': len(events_in_window[events_in_window['event_type'] == 'OPEC']),
                'economic_events': len(events_in_window[events_in_window['event_type'] == 'ECONOMIC'])
            })
        
        return pd.DataFrame(event_counts)
    
    def export_events_to_csv(self, filepath: str) -> None:
        """
        Export events data to CSV file.
        
        Args:
            filepath: Path to save the CSV file
        """
        if self.events_df is None:
            raise ValueError("Event data not compiled. Run compile_historical_events() first.")
        
        self.events_df.to_csv(filepath, index=False)
        logger.info(f"Events data exported to {filepath}")


def main():
    """Main function to demonstrate event research functionality."""
    # Initialize event research
    event_research = EventResearch()
    
    # Compile historical events
    events_df = event_research.compile_historical_events()
    
    # Validate the data
    validation_results = event_research.validate_event_data()
    print("Validation Results:")
    for key, value in validation_results.items():
        print(f"  {key}: {value}")
    
    # Export to CSV
    event_research.export_events_to_csv('data/processed/major_events.csv')
    
    # Show sample events
    print("\nSample Events:")
    print(events_df.head(10))
    
    # Calculate event density
    density_df = event_research.calculate_event_density()
    print(f"\nEvent density calculated for {len(density_df)} time periods")


if __name__ == "__main__":
    main()
