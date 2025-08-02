#!/usr/bin/env python3
"""
Impact Analysis for Brent Oil Prices

This module implements comprehensive impact analysis to quantify the effects
of geopolitical events on Brent oil prices using statistical methods.

Author: Birhan Energies Data Science Team
Date: August 2, 2025
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import ttest_ind, mannwhitneyu
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

class ImpactAnalysis:
    """
    Comprehensive impact analysis for Brent oil prices.
    
    This class implements multiple impact analysis methods:
    1. Event Study Analysis
    2. Regression Analysis
    3. Volatility Analysis
    4. Cumulative Impact Analysis
    5. Statistical Significance Testing
    """
    
    def __init__(self, data: pd.DataFrame, events: pd.DataFrame):
        """
        Initialize the impact analysis.
        
        Parameters:
        -----------
        data : pd.DataFrame
            Time series data with 'price' column and datetime index
        events : pd.DataFrame
            Event data with 'date' and 'event_type' columns
        """
        self.data = data
        self.events = events
        self.log_returns = np.log(data['price'] / data['price'].shift(1)).dropna()
        self.results = {}
        
    def event_study_analysis(self, event_window: int = 30) -> Dict:
        """
        Perform event study analysis around each event.
        
        Parameters:
        -----------
        event_window : int
            Number of days before and after event to analyze
            
        Returns:
        --------
        Dict
            Event study results
        """
        event_results = []
        
        for _, event in self.events.iterrows():
            event_date = event['date']
            
            if event_date in self.data.index:
                event_idx = self.data.index.get_loc(event_date)
                
                # Define pre and post event windows
                pre_start = max(0, event_idx - event_window)
                pre_end = event_idx
                post_start = event_idx
                post_end = min(len(self.data), event_idx + event_window)
                
                # Extract price data
                pre_prices = self.data.iloc[pre_start:pre_end]['price']
                post_prices = self.data.iloc[post_start:post_end]['price']
                
                if len(pre_prices) > 0 and len(post_prices) > 0:
                    # Calculate impact measures
                    pre_mean = pre_prices.mean()
                    post_mean = post_prices.mean()
                    price_change = ((post_mean - pre_mean) / pre_mean) * 100
                    
                    pre_vol = pre_prices.std()
                    post_vol = post_prices.std()
                    vol_change = ((post_vol - pre_vol) / pre_vol) * 100
                    
                    # Statistical significance testing
                    t_stat, p_value = ttest_ind(pre_prices, post_prices)
                    
                    event_results.append({
                        'event_date': event_date,
                        'event_type': event['event_type'],
                        'event_description': event['description'],
                        'pre_mean': pre_mean,
                        'post_mean': post_mean,
                        'price_change_pct': price_change,
                        'pre_volatility': pre_vol,
                        'post_volatility': post_vol,
                        'volatility_change_pct': vol_change,
                        't_statistic': t_stat,
                        'p_value': p_value,
                        'significant': p_value < 0.05
                    })
        
        return {
            'event_study_results': event_results,
            'summary_stats': self._compute_summary_stats(event_results)
        }
    
    def regression_analysis(self) -> Dict:
        """
        Perform regression analysis to quantify event impacts.
        
        Returns:
        --------
        Dict
            Regression analysis results
        """
        # Create event indicators
        event_indicators = self._create_event_indicators()
        
        # Prepare data for regression
        y = self.log_returns.values
        X = np.column_stack([
            np.ones(len(y)),  # Constant
            event_indicators,  # Event indicator
            np.arange(len(y))  # Time trend
        ])
        
        # OLS regression
        beta = np.linalg.lstsq(X, y, rcond=None)[0]
        y_pred = X @ beta
        residuals = y - y_pred
        
        # Calculate R-squared
        ss_res = np.sum(residuals**2)
        ss_tot = np.sum((y - np.mean(y))**2)
        r_squared = 1 - (ss_res / ss_tot)
        
        # Calculate standard errors
        n = len(y)
        p = X.shape[1]
        mse = ss_res / (n - p)
        var_beta = mse * np.linalg.inv(X.T @ X)
        se_beta = np.sqrt(np.diag(var_beta))
        
        # T-statistics and p-values
        t_stats = beta / se_beta
        p_values = 2 * (1 - stats.t.cdf(np.abs(t_stats), n - p))
        
        return {
            'coefficients': beta,
            'standard_errors': se_beta,
            't_statistics': t_stats,
            'p_values': p_values,
            'r_squared': r_squared,
            'event_effect': beta[1],
            'event_effect_se': se_beta[1],
            'event_effect_p': p_values[1]
        }
    
    def volatility_analysis(self, window: int = 30) -> Dict:
        """
        Analyze volatility changes around events.
        
        Parameters:
        -----------
        window : int
            Rolling window size for volatility calculation
            
        Returns:
        --------
        Dict
            Volatility analysis results
        """
        # Calculate rolling volatility
        rolling_vol = self.log_returns.rolling(window=window).std()
        
        volatility_results = []
        
        for _, event in self.events.iterrows():
            event_date = event['date']
            
            if event_date in self.data.index:
                event_idx = self.data.index.get_loc(event_date)
                
                # Pre and post event volatility
                pre_vol = rolling_vol.iloc[max(0, event_idx-window):event_idx].mean()
                post_vol = rolling_vol.iloc[event_idx:min(len(rolling_vol), event_idx+window)].mean()
                
                if not pd.isna(pre_vol) and not pd.isna(post_vol):
                    vol_change = ((post_vol - pre_vol) / pre_vol) * 100
                    
                    volatility_results.append({
                        'event_date': event_date,
                        'event_type': event['event_type'],
                        'pre_volatility': pre_vol,
                        'post_volatility': post_vol,
                        'volatility_change_pct': vol_change
                    })
        
        return {
            'volatility_results': volatility_results,
            'summary_stats': self._compute_volatility_summary(volatility_results)
        }
    
    def cumulative_impact_analysis(self, event_window: int = 30) -> Dict:
        """
        Analyze cumulative impact of events over time.
        
        Parameters:
        -----------
        event_window : int
            Window size for cumulative analysis
            
        Returns:
        --------
        Dict
            Cumulative impact analysis results
        """
        cumulative_results = []
        
        for _, event in self.events.iterrows():
            event_date = event['date']
            
            if event_date in self.data.index:
                event_idx = self.data.index.get_loc(event_date)
                
                # Calculate cumulative returns
                pre_prices = self.data.iloc[max(0, event_idx-event_window):event_idx]['price']
                post_prices = self.data.iloc[event_idx:min(len(self.data), event_idx+event_window)]['price']
                
                if len(pre_prices) > 0 and len(post_prices) > 0:
                    # Cumulative price changes
                    cumulative_changes = []
                    base_price = pre_prices.iloc[-1]
                    
                    for i, price in enumerate(post_prices):
                        cumulative_change = ((price - base_price) / base_price) * 100
                        cumulative_changes.append(cumulative_change)
                    
                    # Find maximum and minimum cumulative impact
                    max_impact = max(cumulative_changes) if cumulative_changes else 0
                    min_impact = min(cumulative_changes) if cumulative_changes else 0
                    final_impact = cumulative_changes[-1] if cumulative_changes else 0
                    
                    cumulative_results.append({
                        'event_date': event_date,
                        'event_type': event['event_type'],
                        'event_description': event['description'],
                        'max_impact': max_impact,
                        'min_impact': min_impact,
                        'final_impact': final_impact,
                        'impact_range': max_impact - min_impact,
                        'cumulative_changes': cumulative_changes
                    })
        
        return {
            'cumulative_results': cumulative_results,
            'summary_stats': self._compute_cumulative_summary(cumulative_results)
        }
    
    def statistical_significance_testing(self) -> Dict:
        """
        Perform comprehensive statistical significance testing.
        
        Returns:
        --------
        Dict
            Statistical significance test results
        """
        # Get event study results
        event_study = self.event_study_analysis()
        event_results = event_study['event_study_results']
        
        if not event_results:
            return {'error': 'No events found for analysis'}
        
        # Extract price changes
        price_changes = [result['price_change_pct'] for result in event_results]
        volatility_changes = [result['volatility_change_pct'] for result in event_results]
        
        # One-sample t-test (test if mean impact is different from zero)
        t_stat_price, p_value_price = stats.ttest_1samp(price_changes, 0)
        t_stat_vol, p_value_vol = stats.ttest_1samp(volatility_changes, 0)
        
        # Wilcoxon signed-rank test (non-parametric alternative)
        w_stat_price, w_p_value_price = stats.wilcoxon(price_changes)
        w_stat_vol, w_p_value_vol = stats.wilcoxon(volatility_changes)
        
        # Test for normality
        _, normality_p_price = stats.normaltest(price_changes)
        _, normality_p_vol = stats.normaltest(volatility_changes)
        
        # Effect size (Cohen's d)
        cohen_d_price = np.mean(price_changes) / np.std(price_changes)
        cohen_d_vol = np.mean(volatility_changes) / np.std(volatility_changes)
        
        return {
            'price_impact_tests': {
                't_statistic': t_stat_price,
                't_p_value': p_value_price,
                'wilcoxon_statistic': w_stat_price,
                'wilcoxon_p_value': w_p_value_price,
                'normality_p_value': normality_p_price,
                'cohen_d': cohen_d_price,
                'mean_impact': np.mean(price_changes),
                'std_impact': np.std(price_changes)
            },
            'volatility_impact_tests': {
                't_statistic': t_stat_vol,
                't_p_value': p_value_vol,
                'wilcoxon_statistic': w_stat_vol,
                'wilcoxon_p_value': w_p_value_vol,
                'normality_p_value': normality_p_vol,
                'cohen_d': cohen_d_vol,
                'mean_impact': np.mean(volatility_changes),
                'std_impact': np.std(volatility_changes)
            }
        }
    
    def plot_impact_analysis(self, save_path: Optional[str] = None):
        """
        Create comprehensive impact analysis visualizations.
        
        Parameters:
        -----------
        save_path : Optional[str]
            Path to save the plot
        """
        # Get all analysis results
        event_study = self.event_study_analysis()
        regression = self.regression_analysis()
        volatility = self.volatility_analysis()
        cumulative = self.cumulative_impact_analysis()
        significance = self.statistical_significance_testing()
        
        # Create comprehensive plot
        fig, axes = plt.subplots(3, 3, figsize=(20, 15))
        
        # Plot 1: Price impact distribution
        if event_study['event_study_results']:
            price_changes = [r['price_change_pct'] for r in event_study['event_study_results']]
            axes[0, 0].hist(price_changes, bins=20, alpha=0.7, edgecolor='black')
            axes[0, 0].axvline(np.mean(price_changes), color='red', linestyle='--', 
                              label=f'Mean: {np.mean(price_changes):.2f}%')
            axes[0, 0].set_title('Distribution of Price Changes')
            axes[0, 0].set_xlabel('Price Change (%)')
            axes[0, 0].set_ylabel('Frequency')
            axes[0, 0].legend()
            axes[0, 0].grid(True, alpha=0.3)
        
        # Plot 2: Volatility impact distribution
        if volatility['volatility_results']:
            vol_changes = [r['volatility_change_pct'] for r in volatility['volatility_results']]
            axes[0, 1].hist(vol_changes, bins=20, alpha=0.7, edgecolor='black')
            axes[0, 1].axvline(np.mean(vol_changes), color='red', linestyle='--', 
                              label=f'Mean: {np.mean(vol_changes):.2f}%')
            axes[0, 1].set_title('Distribution of Volatility Changes')
            axes[0, 1].set_xlabel('Volatility Change (%)')
            axes[0, 1].set_ylabel('Frequency')
            axes[0, 1].legend()
            axes[0, 1].grid(True, alpha=0.3)
        
        # Plot 3: Impact by event type
        if event_study['event_study_results']:
            event_df = pd.DataFrame(event_study['event_study_results'])
            event_type_impact = event_df.groupby('event_type')['price_change_pct'].mean().sort_values(ascending=False)
            bars = axes[0, 2].bar(range(len(event_type_impact)), event_type_impact.values, alpha=0.7)
            axes[0, 2].set_xticks(range(len(event_type_impact)))
            axes[0, 2].set_xticklabels(event_type_impact.index, rotation=45)
            axes[0, 2].set_ylabel('Average Price Change (%)')
            axes[0, 2].set_title('Average Impact by Event Type')
            axes[0, 2].grid(True, alpha=0.3)
        
        # Plot 4: Cumulative impact over time
        if cumulative['cumulative_results']:
            for result in cumulative['cumulative_results'][:5]:  # Show first 5 events
                axes[1, 0].plot(result['cumulative_changes'], alpha=0.7, 
                               label=f"{result['event_date'].strftime('%Y-%m-%d')}: {result['event_type']}")
            axes[1, 0].set_title('Cumulative Impact Over Time')
            axes[1, 0].set_xlabel('Days After Event')
            axes[1, 0].set_ylabel('Cumulative Price Change (%)')
            axes[1, 0].legend()
            axes[1, 0].grid(True, alpha=0.3)
        
        # Plot 5: Statistical significance
        if 'price_impact_tests' in significance:
            price_tests = significance['price_impact_tests']
            vol_tests = significance['volatility_impact_tests']
            
            test_names = ['T-Test', 'Wilcoxon', 'Normality']
            price_p_values = [price_tests['t_p_value'], price_tests['wilcoxon_p_value'], price_tests['normality_p_value']]
            vol_p_values = [vol_tests['t_p_value'], vol_tests['wilcoxon_p_value'], vol_tests['normality_p_value']]
            
            x = np.arange(len(test_names))
            width = 0.35
            
            axes[1, 1].bar(x - width/2, price_p_values, width, label='Price Impact', alpha=0.7)
            axes[1, 1].bar(x + width/2, vol_p_values, width, label='Volatility Impact', alpha=0.7)
            axes[1, 1].set_xticks(x)
            axes[1, 1].set_xticklabels(test_names)
            axes[1, 1].set_ylabel('P-Value')
            axes[1, 1].set_title('Statistical Significance Tests')
            axes[1, 1].legend()
            axes[1, 1].grid(True, alpha=0.3)
        
        # Plot 6: Effect sizes
        if 'price_impact_tests' in significance:
            price_tests = significance['price_impact_tests']
            vol_tests = significance['volatility_impact_tests']
            
            effect_sizes = [price_tests['cohen_d'], vol_tests['cohen_d']]
            effect_labels = ['Price Impact', 'Volatility Impact']
            
            bars = axes[1, 2].bar(effect_labels, effect_sizes, alpha=0.7)
            axes[1, 2].set_ylabel('Cohen\'s d')
            axes[1, 2].set_title('Effect Sizes')
            axes[1, 2].grid(True, alpha=0.3)
        
        # Plot 7: Time series with event impacts
        axes[2, 0].plot(self.data.index, self.data['price'], alpha=0.7, linewidth=0.5)
        
        # Add event markers
        for _, event in self.events.iterrows():
            if event['date'] in self.data.index:
                price_at_event = self.data.loc[event['date'], 'price']
                axes[2, 0].scatter(event['date'], price_at_event, color='red', s=50, alpha=0.8)
        
        axes[2, 0].set_title('Brent Oil Prices with Event Markers')
        axes[2, 0].set_xlabel('Date')
        axes[2, 0].set_ylabel('Price (USD/barrel)')
        axes[2, 0].grid(True, alpha=0.3)
        
        # Plot 8: Regression results
        if 'event_effect' in regression:
            effect = regression['event_effect']
            effect_se = regression['event_effect_se']
            
            axes[2, 1].bar(['Event Effect'], [effect], yerr=[effect_se], alpha=0.7, capsize=10)
            axes[2, 1].set_ylabel('Effect Size')
            axes[2, 1].set_title('Regression Analysis Results')
            axes[2, 1].grid(True, alpha=0.3)
        
        # Plot 9: Summary statistics
        if event_study['event_study_results']:
            summary_stats = event_study['summary_stats']
            
            stats_names = ['Mean', 'Median', 'Std', 'Min', 'Max']
            stats_values = [
                summary_stats['mean_price_change'],
                summary_stats['median_price_change'],
                summary_stats['std_price_change'],
                summary_stats['min_price_change'],
                summary_stats['max_price_change']
            ]
            
            bars = axes[2, 2].bar(stats_names, stats_values, alpha=0.7)
            axes[2, 2].set_ylabel('Price Change (%)')
            axes[2, 2].set_title('Summary Statistics')
            axes[2, 2].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def _create_event_indicators(self) -> np.ndarray:
        """Create event indicators for regression analysis."""
        event_indicators = np.zeros(len(self.log_returns))
        
        for _, event in self.events.iterrows():
            if event['date'] in self.log_returns.index:
                event_idx = self.log_returns.index.get_loc(event['date'])
                if event_idx < len(event_indicators):
                    event_indicators[event_idx] = 1
        
        return event_indicators
    
    def _compute_summary_stats(self, results: List[Dict]) -> Dict:
        """Compute summary statistics for event study results."""
        if not results:
            return {}
        
        price_changes = [r['price_change_pct'] for r in results]
        vol_changes = [r['volatility_change_pct'] for r in results]
        
        return {
            'mean_price_change': np.mean(price_changes),
            'median_price_change': np.median(price_changes),
            'std_price_change': np.std(price_changes),
            'min_price_change': np.min(price_changes),
            'max_price_change': np.max(price_changes),
            'mean_volatility_change': np.mean(vol_changes),
            'median_volatility_change': np.median(vol_changes),
            'std_volatility_change': np.std(vol_changes),
            'significant_events': sum(1 for r in results if r['significant']),
            'total_events': len(results)
        }
    
    def _compute_volatility_summary(self, results: List[Dict]) -> Dict:
        """Compute summary statistics for volatility analysis."""
        if not results:
            return {}
        
        vol_changes = [r['volatility_change_pct'] for r in results]
        
        return {
            'mean_volatility_change': np.mean(vol_changes),
            'median_volatility_change': np.median(vol_changes),
            'std_volatility_change': np.std(vol_changes),
            'min_volatility_change': np.min(vol_changes),
            'max_volatility_change': np.max(vol_changes)
        }
    
    def _compute_cumulative_summary(self, results: List[Dict]) -> Dict:
        """Compute summary statistics for cumulative analysis."""
        if not results:
            return {}
        
        max_impacts = [r['max_impact'] for r in results]
        min_impacts = [r['min_impact'] for r in results]
        final_impacts = [r['final_impact'] for r in results]
        
        return {
            'mean_max_impact': np.mean(max_impacts),
            'mean_min_impact': np.mean(min_impacts),
            'mean_final_impact': np.mean(final_impacts),
            'std_max_impact': np.std(max_impacts),
            'std_min_impact': np.std(min_impacts),
            'std_final_impact': np.std(final_impacts)
        }


def main():
    """Demonstrate the impact analysis."""
    # Load data
    data = pd.read_csv('../data/processed/brent_oil_prices_processed.csv', index_col=0)
    data.index = pd.to_datetime(data.index)
    
    events = pd.read_csv('../data/processed/major_events.csv')
    events['date'] = pd.to_datetime(events['date'])
    
    # Initialize analysis
    ia = ImpactAnalysis(data, events)
    
    # Perform all analyses
    print("Performing comprehensive impact analysis...")
    
    event_study = ia.event_study_analysis()
    regression = ia.regression_analysis()
    volatility = ia.volatility_analysis()
    cumulative = ia.cumulative_impact_analysis()
    significance = ia.statistical_significance_testing()
    
    # Print results
    print("\nImpact Analysis Results:")
    print("=" * 50)
    
    print(f"\nEvent Study Analysis:")
    print(f"  Total events analyzed: {len(event_study['event_study_results'])}")
    print(f"  Significant events: {event_study['summary_stats']['significant_events']}")
    print(f"  Mean price change: {event_study['summary_stats']['mean_price_change']:.2f}%")
    
    print(f"\nRegression Analysis:")
    print(f"  Event effect: {regression['event_effect']:.6f}")
    print(f"  Standard error: {regression['event_effect_se']:.6f}")
    print(f"  P-value: {regression['event_effect_p']:.6f}")
    print(f"  R-squared: {regression['r_squared']:.4f}")
    
    print(f"\nVolatility Analysis:")
    print(f"  Mean volatility change: {volatility['summary_stats']['mean_volatility_change']:.2f}%")
    
    print(f"\nStatistical Significance:")
    price_tests = significance['price_impact_tests']
    print(f"  Price impact t-test p-value: {price_tests['t_p_value']:.6f}")
    print(f"  Price impact effect size (Cohen's d): {price_tests['cohen_d']:.3f}")
    
    # Plot results
    ia.plot_impact_analysis('docs/impact_analysis_results.png')
    
    return ia


if __name__ == "__main__":
    main()

