"""
Impact Analysis Module

This module analyzes the impact of key events on Brent oil prices by correlating
change points with historical events and quantifying their effects.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta
from .event_research import EventResearch
from .change_point import ChangePointAnalyzer


class ImpactAnalyzer:
    """
    A class for analyzing the impact of key events on Brent oil prices.
    """
    
    def __init__(self, oil_data: pd.DataFrame, event_research: EventResearch):
        """
        Initialize the impact analyzer.
        
        Args:
            oil_data (pd.DataFrame): Brent oil price data
            event_research (EventResearch): Event research object
        """
        self.oil_data = oil_data.copy()
        
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
        
        self.oil_data['Date'] = self.oil_data['Date'].apply(parse_date)
        self.oil_data = self.oil_data.sort_values('Date').reset_index(drop=True)
        
        self.event_research = event_research
        self.change_point_analyzer = ChangePointAnalyzer(oil_data)
        
        # Analysis results storage
        self.event_impacts = None
        self.correlation_analysis = None
        
    def analyze_event_impact(self, event_date: str, window_days: int = 30) -> Dict:
        """
        Analyze the impact of a specific event on oil prices.
        
        Args:
            event_date (str): Event date in 'YYYY-MM-DD' format
            window_days (int): Number of days to analyze around the event
            
        Returns:
            Dict: Impact analysis results
        """
        event_dt = pd.to_datetime(event_date)
        
        # Find the closest data point to the event date
        date_diff = abs(self.oil_data['Date'] - event_dt)
        closest_idx = date_diff.idxmin()
        event_idx = closest_idx
        
        # Define windows before and after the event
        before_start = max(0, event_idx - window_days)
        after_end = min(len(self.oil_data), event_idx + window_days)
        
        before_data = self.oil_data.iloc[before_start:event_idx]
        after_data = self.oil_data.iloc[event_idx:after_end]
        
        # Calculate impact metrics
        before_stats = {
            'mean_price': before_data['Price'].mean(),
            'std_price': before_data['Price'].std(),
            'min_price': before_data['Price'].min(),
            'max_price': before_data['Price'].max(),
            'trend': np.polyfit(range(len(before_data)), before_data['Price'], 1)[0]
        }
        
        after_stats = {
            'mean_price': after_data['Price'].mean(),
            'std_price': after_data['Price'].std(),
            'min_price': after_data['Price'].min(),
            'max_price': after_data['Price'].max(),
            'trend': np.polyfit(range(len(after_data)), after_data['Price'], 1)[0]
        }
        
        # Calculate impact measures
        price_change = after_stats['mean_price'] - before_stats['mean_price']
        price_change_pct = (price_change / before_stats['mean_price']) * 100
        volatility_change = after_stats['std_price'] - before_stats['std_price']
        trend_change = after_stats['trend'] - before_stats['trend']
        
        # Calculate maximum and minimum impacts
        max_price_change = after_data['Price'].max() - before_data['Price'].mean()
        min_price_change = after_data['Price'].min() - before_data['Price'].mean()
        
        impact_analysis = {
            'event_date': event_date,
            'analysis_window': window_days,
            'before_stats': before_stats,
            'after_stats': after_stats,
            'price_change': price_change,
            'price_change_pct': price_change_pct,
            'volatility_change': volatility_change,
            'trend_change': trend_change,
            'max_price_change': max_price_change,
            'min_price_change': min_price_change,
            'before_data': before_data,
            'after_data': after_data
        }
        
        return impact_analysis
    
    def correlate_events_with_change_points(self, change_points: List[Dict], 
                                         tolerance_days: int = 30) -> List[Dict]:
        """
        Correlate detected change points with known events.
        
        Args:
            change_points (List[Dict]): List of detected change points
            tolerance_days (int): Number of days to consider for correlation
            
        Returns:
            List[Dict]: Correlated events and change points
        """
        events = self.event_research.get_all_events()
        correlations = []
        
        for cp in change_points:
            cp_date = cp['change_point_date']
            
            # Find events within tolerance window
            for _, event in events.iterrows():
                event_date = event['date']
                days_diff = abs((cp_date - event_date).days)
                
                if days_diff <= tolerance_days:
                    correlation = {
                        'change_point_date': cp_date,
                        'event_date': event_date,
                        'event_name': event['event'],
                        'event_category': event['category'],
                        'event_description': event['description'],
                        'expected_impact': event['expected_impact'],
                        'region': event['region'],
                        'days_difference': days_diff,
                        'change_point_impact': cp,
                        'correlation_strength': 1.0 / (1.0 + days_diff)  # Simple correlation measure
                    }
                    correlations.append(correlation)
        
        # Sort by correlation strength
        correlations.sort(key=lambda x: x['correlation_strength'], reverse=True)
        
        return correlations
    
    def analyze_all_events(self, window_days: int = 30) -> pd.DataFrame:
        """
        Analyze the impact of all events in the database.
        
        Args:
            window_days (int): Number of days to analyze around each event
            
        Returns:
            pd.DataFrame: Analysis results for all events
        """
        events = self.event_research.get_all_events()
        results = []
        
        for _, event in events.iterrows():
            try:
                impact = self.analyze_event_impact(event['date'].strftime('%Y-%m-%d'), window_days)
                
                result = {
                    'event_date': event['date'],
                    'event_name': event['event'],
                    'event_category': event['category'],
                    'expected_impact': event['expected_impact'],
                    'region': event['region'],
                    'price_change_usd': impact['price_change'],
                    'price_change_pct': impact['price_change_pct'],
                    'volatility_change': impact['volatility_change'],
                    'trend_change': impact['trend_change'],
                    'max_price_change': impact['max_price_change'],
                    'min_price_change': impact['min_price_change'],
                    'before_mean_price': impact['before_stats']['mean_price'],
                    'after_mean_price': impact['after_stats']['mean_price']
                }
                results.append(result)
                
            except Exception as e:
                print(f"Error analyzing event {event['event']}: {e}")
                continue
        
        self.event_impacts = pd.DataFrame(results)
        return self.event_impacts
    
    def plot_event_impact(self, event_date: str, save_path: Optional[str] = None) -> None:
        """
        Create a comprehensive plot showing the impact of a specific event.
        
        Args:
            event_date (str): Event date in 'YYYY-MM-DD' format
            save_path (Optional[str]): Path to save the plot
        """
        impact = self.analyze_event_impact(event_date)
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Plot 1: Price series with event marker
        full_data = pd.concat([impact['before_data'], impact['after_data']])
        axes[0, 0].plot(full_data['Date'], full_data['Price'], alpha=0.7, linewidth=1)
        
        event_dt = pd.to_datetime(event_date)
        event_price = self.oil_data[self.oil_data['Date'] == event_dt]['Price'].iloc[0]
        axes[0, 0].axvline(x=event_dt, color='red', linestyle='--', alpha=0.8, 
                           label=f'Event: {event_dt.strftime("%Y-%m-%d")}')
        axes[0, 0].scatter(event_dt, event_price, color='red', s=100, zorder=5)
        axes[0, 0].set_title('Oil Price Around Event')
        axes[0, 0].set_xlabel('Date')
        axes[0, 0].set_ylabel('Price (USD/barrel)')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # Plot 2: Price comparison before/after
        before_price = impact['before_stats']['mean_price']
        after_price = impact['after_stats']['mean_price']
        price_change = impact['price_change_pct']
        
        bars = axes[0, 1].bar(['Before', 'After'], [before_price, after_price], 
                              color=['lightblue', 'lightcoral'], alpha=0.7)
        axes[0, 1].set_title(f'Price Comparison\nChange: {price_change:.2f}%')
        axes[0, 1].set_ylabel('Average Price (USD/barrel)')
        axes[0, 1].grid(True, alpha=0.3)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            axes[0, 1].text(bar.get_x() + bar.get_width()/2., height,
                           f'{height:.2f}', ha='center', va='bottom')
        
        # Plot 3: Volatility comparison
        before_vol = impact['before_stats']['std_price']
        after_vol = impact['after_stats']['std_price']
        vol_change = impact['volatility_change']
        
        bars = axes[1, 0].bar(['Before', 'After'], [before_vol, after_vol], 
                              color=['lightgreen', 'lightyellow'], alpha=0.7)
        axes[1, 0].set_title(f'Volatility Comparison\nChange: {vol_change:.2f}')
        axes[1, 0].set_ylabel('Price Volatility (USD/barrel)')
        axes[1, 0].grid(True, alpha=0.3)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            axes[1, 0].text(bar.get_x() + bar.get_width()/2., height,
                           f'{height:.2f}', ha='center', va='bottom')
        
        # Plot 4: Price range comparison
        before_range = [impact['before_stats']['min_price'], impact['before_stats']['max_price']]
        after_range = [impact['after_stats']['min_price'], impact['after_stats']['max_price']]
        
        axes[1, 1].errorbar(['Before', 'After'], 
                           [before_price, after_price],
                           yerr=[[before_price - before_range[0], after_price - after_range[0]],
                                 [before_range[1] - before_price, after_range[1] - after_price]],
                           fmt='o', capsize=5, capthick=2)
        axes[1, 1].set_title('Price Range Comparison')
        axes[1, 1].set_ylabel('Price (USD/barrel)')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def plot_event_category_analysis(self, save_path: Optional[str] = None) -> None:
        """
        Create plots analyzing events by category.
        
        Args:
            save_path (Optional[str]): Path to save the plot
        """
        if self.event_impacts is None:
            self.analyze_all_events()
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Plot 1: Average impact by event category
        category_impact = self.event_impacts.groupby('event_category')['price_change_pct'].mean().sort_values()
        bars = axes[0, 0].bar(range(len(category_impact)), category_impact.values, 
                              color=plt.cm.Set3(np.linspace(0, 1, len(category_impact))))
        axes[0, 0].set_title('Average Price Impact by Event Category')
        axes[0, 0].set_xlabel('Event Category')
        axes[0, 0].set_ylabel('Average Price Change (%)')
        axes[0, 0].set_xticks(range(len(category_impact)))
        axes[0, 0].set_xticklabels(category_impact.index, rotation=45, ha='right')
        axes[0, 0].grid(True, alpha=0.3)
        
        # Add value labels on bars
        for i, bar in enumerate(bars):
            height = bar.get_height()
            axes[0, 0].text(bar.get_x() + bar.get_width()/2., height,
                           f'{height:.1f}%', ha='center', va='bottom')
        
        # Plot 2: Impact distribution by expected impact
        expected_impact_stats = self.event_impacts.groupby('expected_impact')['price_change_pct'].agg(['mean', 'std'])
        axes[0, 1].bar(expected_impact_stats.index, expected_impact_stats['mean'], 
                       yerr=expected_impact_stats['std'], capsize=5, alpha=0.7)
        axes[0, 1].set_title('Impact by Expected Direction')
        axes[0, 1].set_xlabel('Expected Impact')
        axes[0, 1].set_ylabel('Actual Price Change (%)')
        axes[0, 1].grid(True, alpha=0.3)
        
        # Plot 3: Regional impact analysis
        region_impact = self.event_impacts.groupby('region')['price_change_pct'].mean().sort_values()
        bars = axes[1, 0].bar(range(len(region_impact)), region_impact.values,
                              color=plt.cm.Pastel1(np.linspace(0, 1, len(region_impact))))
        axes[1, 0].set_title('Average Impact by Region')
        axes[1, 0].set_xlabel('Region')
        axes[1, 0].set_ylabel('Average Price Change (%)')
        axes[1, 0].set_xticks(range(len(region_impact)))
        axes[1, 0].set_xticklabels(region_impact.index, rotation=45, ha='right')
        axes[1, 0].grid(True, alpha=0.3)
        
        # Add value labels on bars
        for i, bar in enumerate(bars):
            height = bar.get_height()
            axes[1, 0].text(bar.get_x() + bar.get_width()/2., height,
                           f'{height:.1f}%', ha='center', va='bottom')
        
        # Plot 4: Time series of event impacts
        self.event_impacts['event_date'] = pd.to_datetime(self.event_impacts['event_date'])
        time_series = self.event_impacts.sort_values('event_date')
        
        axes[1, 1].scatter(time_series['event_date'], time_series['price_change_pct'], 
                           alpha=0.7, s=50)
        axes[1, 1].axhline(y=0, color='black', linestyle='--', alpha=0.5)
        axes[1, 1].set_title('Event Impacts Over Time')
        axes[1, 1].set_xlabel('Date')
        axes[1, 1].set_ylabel('Price Change (%)')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def get_impact_summary(self) -> Dict:
        """
        Get a summary of all event impacts.
        
        Returns:
            Dict: Summary statistics
        """
        if self.event_impacts is None:
            self.analyze_all_events()
        
        summary = {
            'total_events': int(len(self.event_impacts)),
            'average_price_change': float(self.event_impacts['price_change_pct'].mean()),
            'median_price_change': float(self.event_impacts['price_change_pct'].median()),
            'price_change_std': float(self.event_impacts['price_change_pct'].std()),
            'max_positive_impact': float(self.event_impacts['price_change_pct'].max()),
            'max_negative_impact': float(self.event_impacts['price_change_pct'].min()),
            'events_with_positive_impact': int((self.event_impacts['price_change_pct'] > 0).sum()),
            'events_with_negative_impact': int((self.event_impacts['price_change_pct'] < 0).sum()),
            'category_breakdown': {str(k): int(v) for k, v in self.event_impacts['event_category'].value_counts().to_dict().items()},
            'region_breakdown': {str(k): int(v) for k, v in self.event_impacts['region'].value_counts().to_dict().items()}
        }
        
        return summary
    
    def export_impact_analysis(self, filepath: str) -> None:
        """
        Export impact analysis results to CSV.
        
        Args:
            filepath (str): Path to save the results
        """
        if self.event_impacts is None:
            self.analyze_all_events()
        
        self.event_impacts.to_csv(filepath, index=False)
