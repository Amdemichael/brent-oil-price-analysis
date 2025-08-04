"""
Event Research Module

This module compiles and manages key geopolitical and economic events that have impacted
Brent oil prices over the past decades.
"""

import pandas as pd
from datetime import datetime
from typing import List, Dict, Any


class EventResearch:
    """
    A class to manage and research key events that have impacted Brent oil prices.
    """
    
    def __init__(self):
        self.events = self._compile_events()
    
    def _compile_events(self) -> pd.DataFrame:
        """
        Compile a comprehensive list of key events affecting oil prices.
        
        Returns:
            pd.DataFrame: DataFrame with event information
        """
        events_data = [
            # Gulf War (1990-1991)
            {
                'date': '1990-08-02',
                'event': 'Iraq invades Kuwait',
                'category': 'Military Conflict',
                'description': 'Iraq invades Kuwait, leading to the Gulf War and significant oil supply disruptions',
                'expected_impact': 'Price Increase',
                'region': 'Middle East'
            },
            {
                'date': '1991-01-17',
                'event': 'Operation Desert Storm begins',
                'category': 'Military Conflict',
                'description': 'US-led coalition begins military operations against Iraq',
                'expected_impact': 'Price Volatility',
                'region': 'Middle East'
            },
            
            # Asian Financial Crisis (1997-1998)
            {
                'date': '1997-07-02',
                'event': 'Asian Financial Crisis begins',
                'category': 'Economic Crisis',
                'description': 'Financial crisis in Asia leads to reduced oil demand',
                'expected_impact': 'Price Decrease',
                'region': 'Asia'
            },
            
            # OPEC Production Cuts (1998-1999)
            {
                'date': '1998-03-30',
                'event': 'OPEC production cuts',
                'category': 'OPEC Policy',
                'description': 'OPEC agrees to cut production by 2.5 million barrels per day',
                'expected_impact': 'Price Increase',
                'region': 'Global'
            },
            
            # 9/11 Attacks (2001)
            {
                'date': '2001-09-11',
                'event': '9/11 Terrorist Attacks',
                'category': 'Terrorism',
                'description': 'Terrorist attacks on US soil create market uncertainty',
                'expected_impact': 'Price Increase',
                'region': 'North America'
            },
            
            # Iraq War (2003)
            {
                'date': '2003-03-20',
                'event': 'US invasion of Iraq begins',
                'category': 'Military Conflict',
                'description': 'US-led invasion of Iraq creates supply uncertainty',
                'expected_impact': 'Price Increase',
                'region': 'Middle East'
            },
            
            # Global Financial Crisis (2008)
            {
                'date': '2008-09-15',
                'event': 'Lehman Brothers bankruptcy',
                'category': 'Economic Crisis',
                'description': 'Global financial crisis leads to economic recession and reduced oil demand',
                'expected_impact': 'Price Decrease',
                'region': 'Global'
            },
            
            # Arab Spring (2011)
            {
                'date': '2011-01-25',
                'event': 'Arab Spring begins',
                'category': 'Political Unrest',
                'description': 'Political unrest in Middle East and North Africa affects oil production',
                'expected_impact': 'Price Increase',
                'region': 'Middle East/North Africa'
            },
            
            # Libyan Civil War (2011)
            {
                'date': '2011-02-17',
                'event': 'Libyan Civil War begins',
                'category': 'Military Conflict',
                'description': 'Civil war in Libya disrupts oil production',
                'expected_impact': 'Price Increase',
                'region': 'North Africa'
            },
            
            # US Shale Revolution (2012-2014)
            {
                'date': '2012-01-01',
                'event': 'US Shale Revolution accelerates',
                'category': 'Technology',
                'description': 'Increased US shale oil production changes global supply dynamics',
                'expected_impact': 'Price Decrease',
                'region': 'North America'
            },
            
            # OPEC Price War (2014)
            {
                'date': '2014-11-27',
                'event': 'OPEC maintains production despite oversupply',
                'category': 'OPEC Policy',
                'description': 'OPEC refuses to cut production despite falling prices',
                'expected_impact': 'Price Decrease',
                'region': 'Global'
            },
            
            # COVID-19 Pandemic (2020)
            {
                'date': '2020-03-11',
                'event': 'COVID-19 declared pandemic',
                'category': 'Pandemic',
                'description': 'Global pandemic leads to unprecedented demand destruction',
                'expected_impact': 'Price Decrease',
                'region': 'Global'
            },
            
            # Russia-Ukraine War (2022)
            {
                'date': '2022-02-24',
                'event': 'Russia invades Ukraine',
                'category': 'Military Conflict',
                'description': 'Russian invasion of Ukraine creates energy supply uncertainty',
                'expected_impact': 'Price Increase',
                'region': 'Europe'
            },
            
            # OPEC+ Production Cuts (2022)
            {
                'date': '2022-10-05',
                'event': 'OPEC+ announces major production cuts',
                'category': 'OPEC Policy',
                'description': 'OPEC+ agrees to cut production by 2 million barrels per day',
                'expected_impact': 'Price Increase',
                'region': 'Global'
            }
        ]
        
        df = pd.DataFrame(events_data)
        df['date'] = pd.to_datetime(df['date'])
        return df
    
    def get_events_by_date_range(self, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Get events within a specific date range.
        
        Args:
            start_date (str): Start date in 'YYYY-MM-DD' format
            end_date (str): End date in 'YYYY-MM-DD' format
            
        Returns:
            pd.DataFrame: Filtered events
        """
        start = pd.to_datetime(start_date)
        end = pd.to_datetime(end_date)
        
        mask = (self.events['date'] >= start) & (self.events['date'] <= end)
        return self.events[mask]
    
    def get_events_by_category(self, category: str) -> pd.DataFrame:
        """
        Get events by category.
        
        Args:
            category (str): Event category to filter by
            
        Returns:
            pd.DataFrame: Filtered events
        """
        return self.events[self.events['category'] == category]
    
    def get_events_by_region(self, region: str) -> pd.DataFrame:
        """
        Get events by region.
        
        Args:
            region (str): Region to filter by
            
        Returns:
            pd.DataFrame: Filtered events
        """
        return self.events[self.events['region'] == region]
    
    def get_all_events(self) -> pd.DataFrame:
        """
        Get all events.
        
        Returns:
            pd.DataFrame: All events
        """
        return self.events.copy()
    
    def add_event(self, date: str, event: str, category: str, description: str, 
                  expected_impact: str, region: str) -> None:
        """
        Add a new event to the database.
        
        Args:
            date (str): Event date in 'YYYY-MM-DD' format
            event (str): Event name
            category (str): Event category
            description (str): Event description
            expected_impact (str): Expected price impact
            region (str): Affected region
        """
        new_event = {
            'date': pd.to_datetime(date),
            'event': event,
            'category': category,
            'description': description,
            'expected_impact': expected_impact,
            'region': region
        }
        
        self.events = pd.concat([self.events, pd.DataFrame([new_event])], 
                               ignore_index=True)
    
    def export_events(self, filepath: str) -> None:
        """
        Export events to CSV file.
        
        Args:
            filepath (str): Path to save the CSV file
        """
        self.events.to_csv(filepath, index=False)
    
    def get_event_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about the events database.
        
        Returns:
            Dict[str, Any]: Statistics about events
        """
        stats = {
            'total_events': len(self.events),
            'categories': self.events['category'].value_counts().to_dict(),
            'regions': self.events['region'].value_counts().to_dict(),
            'expected_impacts': self.events['expected_impact'].value_counts().to_dict(),
            'date_range': {
                'start': self.events['date'].min().strftime('%Y-%m-%d'),
                'end': self.events['date'].max().strftime('%Y-%m-%d')
            }
        }
        return stats
