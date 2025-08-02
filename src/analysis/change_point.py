#!/usr/bin/env python3
"""
Bayesian Change Point Analysis for Brent Oil Prices

This module implements Bayesian change point detection using PyMC to identify
structural breaks in Brent oil price time series and correlate them with
geopolitical events.

Author: Birhan Energies Data Science Team
Date: August 2, 2025
"""

import numpy as np
import pandas as pd
import pytensor.tensor as pt
import matplotlib.pyplot as plt
import seaborn as sns
import pymc as pm
import arviz as az
from scipy import stats
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

class BayesianChangePointAnalysis:
    """
    Bayesian change point analysis for Brent oil prices using PyMC.
    
    This class implements multiple change point models:
    1. Single change point model
    2. Multiple change points model
    3. Hierarchical change point model
    4. Event-correlated change point model
    """
    
    def __init__(self, data: pd.DataFrame, events: pd.DataFrame):
        """
        Initialize the change point analysis.
        
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
        self.models = {}
        self.traces = {}
        self.results = {}
        
    def single_change_point_model(self, n_changepoints: int = 1) -> pm.Model:
        """
        Implement single change point model using PyMC.
        
        Parameters:
        -----------
        n_changepoints : int
            Number of change points to detect (default: 1)
            
        Returns:
        --------
        pm.Model
            PyMC model for change point analysis
        """
        n_data = len(self.log_returns)
        
        with pm.Model() as model:
            # Prior for change point locations
            changepoint_prior = pm.Uniform('changepoint_prior', 
                                         lower=0.1, upper=0.9, shape=n_changepoints)
            changepoints = pm.Deterministic('changepoints', 
                                          (changepoint_prior * n_data).astype(int))
            
            # Prior for segment means
            segment_means = pm.Normal('segment_means', mu=0, sigma=1, shape=n_changepoints + 1)
            
            # Prior for segment standard deviations
            segment_sds = pm.HalfNormal('segment_sds', sigma=1, shape=n_changepoints + 1)
            
            # Likelihood
            segment_idx = pm.Deterministic('segment_idx', 
                                         self._get_segment_indices(changepoints, n_data))
            
            likelihood = pm.Normal('likelihood', 
                                 mu=segment_means[segment_idx], 
                                 sigma=segment_sds[segment_idx], 
                                 observed=self.log_returns)
            
        return model
    
    def multiple_change_points_model(self, max_changepoints: int = 5) -> pm.Model:
        """
        Implement multiple change points model with variable number of change points.
        
        Parameters:
        -----------
        max_changepoints : int
            Maximum number of change points to consider
            
        Returns:
        --------
        pm.Model
            PyMC model for multiple change point analysis
        """
        n_data = len(self.log_returns)
        
        with pm.Model() as model:
            # Prior for number of change points
            n_changepoints = pm.DiscreteUniform('n_changepoints', 
                                              lower=0, upper=max_changepoints)
            
            # Prior for change point locations (conditional on number)
            changepoint_prior = pm.Uniform('changepoint_prior', 
                                         lower=0.1, upper=0.9, shape=max_changepoints)
            
            # Only use the first n_changepoints
            changepoints = pm.Deterministic('changepoints', 
                                          (changepoint_prior[:n_changepoints] * n_data).astype(int))
            
            # Prior for segment parameters
            segment_means = pm.Normal('segment_means', mu=0, sigma=1, shape=max_changepoints + 1)
            segment_sds = pm.HalfNormal('segment_sds', sigma=1, shape=max_changepoints + 1)
            
            # Likelihood
            segment_idx = pm.Deterministic('segment_idx', 
                                         self._get_segment_indices(changepoints, n_data))
            
            likelihood = pm.Normal('likelihood', 
                                 mu=segment_means[segment_idx], 
                                 sigma=segment_sds[segment_idx], 
                                 observed=self.log_returns)
            
        return model
    
    def event_correlated_model(self) -> pm.Model:
        """
        Implement change point model that incorporates event information.
        
        Returns:
        --------
        pm.Model
            PyMC model for event-correlated change point analysis
        """
        n_data = len(self.log_returns)
        
        # Create event indicators
        event_indicators = self._create_event_indicators()
        
        with pm.Model() as model:
            # Base change point model
            changepoint_prior = pm.Uniform('changepoint_prior', lower=0.1, upper=0.9)
            changepoint = pm.Deterministic('changepoint', 
                                         (changepoint_prior * n_data).astype(int))
            
            # Segment parameters
            pre_mean = pm.Normal('pre_mean', mu=0, sigma=1)
            post_mean = pm.Normal('post_mean', mu=0, sigma=1)
            pre_sd = pm.HalfNormal('pre_sd', sigma=1)
            post_sd = pm.HalfNormal('post_sd', sigma=1)
            
            # Event effect parameters
            event_effect = pm.Normal('event_effect', mu=0, sigma=0.1)
            
            # Likelihood with event correlation
            segment_idx = pm.Deterministic('segment_idx', 
                                         (np.arange(n_data) >= changepoint).astype(int))
            
            mu = pm.Deterministic('mu', 
                                pm.math.switch(segment_idx, post_mean, pre_mean) + 
                                event_effect * event_indicators)
            sigma = pm.Deterministic('sigma', 
                                   pm.math.switch(segment_idx, post_sd, pre_sd))
            
            likelihood = pm.Normal('likelihood', mu=mu, sigma=sigma, observed=self.log_returns)
            
        return model
    
    def hierarchical_model(self) -> pm.Model:
        """
        Implement hierarchical change point model for multiple time periods.
        
        Returns:
        --------
        pm.Model
            PyMC hierarchical model for change point analysis
        """
        n_data = len(self.log_returns)
        
        # Split data into periods (e.g., decades)
        periods = self._split_into_periods()
        
        with pm.Model() as model:
            # Global parameters
            global_changepoint_prior = pm.Uniform('global_changepoint_prior', 
                                                lower=0.1, upper=0.9)
            global_changepoint = pm.Deterministic('global_changepoint', 
                                                (global_changepoint_prior * n_data).astype(int))
            
            # Period-specific parameters
            period_means = pm.Normal('period_means', mu=0, sigma=1, shape=len(periods))
            period_sds = pm.HalfNormal('period_sds', sigma=1, shape=len(periods))
            
            # Hierarchical structure
            global_mean = pm.Normal('global_mean', mu=0, sigma=1)
            global_sd = pm.HalfNormal('global_sd', sigma=1)
            
            # Period effects
            period_effects = pm.Normal('period_effects', mu=global_mean, sigma=global_sd, 
                                     shape=len(periods))
            
            # Likelihood
            segment_idx = pm.Deterministic('segment_idx', 
                                         (np.arange(n_data) >= global_changepoint).astype(int))
            
            likelihood = pm.Normal('likelihood', 
                                 mu=period_effects[segment_idx], 
                                 sigma=period_sds[segment_idx], 
                                 observed=self.log_returns)
            
        return model
    
    def fit_model(self, model: pm.Model, model_name: str, 
                  n_samples: int = 2000, n_tune: int = 1000) -> Dict:
        """
        Fit a PyMC model using MCMC sampling.
        
        Parameters:
        -----------
        model : pm.Model
            PyMC model to fit
        model_name : str
            Name for the model
        n_samples : int
            Number of MCMC samples
        n_tune : int
            Number of tuning steps
            
        Returns:
        --------
        Dict
            Dictionary containing model results and diagnostics
        """
        print(f"Fitting {model_name}...")
        
        with model:
            trace = pm.sample(n_samples, tune=n_tune, return_inferencedata=True)
            
        # Model diagnostics
        summary = az.summary(trace)
        diagnostics = self._compute_diagnostics(trace)
        
        # Store results
        self.models[model_name] = model
        self.traces[model_name] = trace
        self.results[model_name] = {
            'summary': summary,
            'diagnostics': diagnostics,
            'trace': trace
        }
        
        return self.results[model_name]
    
    def analyze_change_points(self, model_name: str) -> Dict:
        """
        Analyze detected change points and correlate with events.
        
        Parameters:
        -----------
        model_name : str
            Name of the model to analyze
            
        Returns:
        --------
        Dict
            Analysis results including change points and event correlations
        """
        if model_name not in self.results:
            raise ValueError(f"Model {model_name} not found. Run fit_model first.")
        
        trace = self.traces[model_name]
        data = self.data
        
        # Extract change points
        if 'changepoint' in trace.posterior:
            changepoints = trace.posterior['changepoint'].values.flatten()
        elif 'changepoints' in trace.posterior:
            changepoints = trace.posterior['changepoints'].values.flatten()
        else:
            changepoints = []
        
        # Convert to dates
        change_point_dates = []
        if len(changepoints) > 0:
            for cp in changepoints:
                if cp < len(data):
                    change_point_dates.append(data.index[int(cp)])
        
        # Find nearby events
        event_correlations = self._find_event_correlations(change_point_dates)
        
        # Compute impact measures
        impact_analysis = self._compute_impact_measures(change_point_dates)
        
        return {
            'change_points': change_point_dates,
            'event_correlations': event_correlations,
            'impact_analysis': impact_analysis,
            'model_diagnostics': self.results[model_name]['diagnostics']
        }
    
    def plot_results(self, model_name: str, save_path: Optional[str] = None):
        """
        Create comprehensive visualization of change point analysis results.
        
        Parameters:
        -----------
        model_name : str
            Name of the model to plot
        save_path : Optional[str]
            Path to save the plot
        """
        if model_name not in self.results:
            raise ValueError(f"Model {model_name} not found. Run fit_model first.")
        
        analysis = self.analyze_change_points(model_name)
        
        fig, axes = plt.subplots(3, 2, figsize=(20, 15))
        
        # Plot 1: Time series with change points
        axes[0, 0].plot(self.data.index, self.data['price'], alpha=0.7, linewidth=0.5)
        for cp in analysis['change_points']:
            axes[0, 0].axvline(x=cp, color='red', linestyle='--', alpha=0.8)
        axes[0, 0].set_title('Brent Oil Prices with Detected Change Points')
        axes[0, 0].set_xlabel('Date')
        axes[0, 0].set_ylabel('Price (USD/barrel)')
        
        # Plot 2: Log returns with change points
        axes[0, 1].plot(self.log_returns.index, self.log_returns, alpha=0.7, linewidth=0.5)
        for cp in analysis['change_points']:
            if cp in self.log_returns.index:
                axes[0, 1].axvline(x=cp, color='red', linestyle='--', alpha=0.8)
        axes[0, 1].set_title('Log Returns with Detected Change Points')
        axes[0, 1].set_xlabel('Date')
        axes[0, 1].set_ylabel('Log Returns')
        
        # Plot 3: Event correlations
        if analysis['event_correlations']:
            event_data = pd.DataFrame(analysis['event_correlations'])
            axes[1, 0].scatter(event_data['distance_days'], event_data['event_impact'], alpha=0.7)
            axes[1, 0].set_title('Event Correlation with Change Points')
            axes[1, 0].set_xlabel('Days from Change Point')
            axes[1, 0].set_ylabel('Event Impact')
        
        # Plot 4: Impact analysis
        if analysis['impact_analysis']:
            impact_data = pd.DataFrame(analysis['impact_analysis'])
            axes[1, 1].bar(range(len(impact_data)), impact_data['price_change'])
            axes[1, 1].set_title('Price Changes Around Change Points')
            axes[1, 1].set_xlabel('Change Point Index')
            axes[1, 1].set_ylabel('Price Change (%)')
        
        # Plot 5: Model diagnostics
        trace = self.traces[model_name]
        az.plot_trace(trace, axes=axes[2, :])
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def _get_segment_indices(self, changepoints, n_data):
        idxs = pt.arange(n_data)
        # For each data point, count how many changepoints are <= idx
        segment_idx = pt.sum(idxs[None, :] >= changepoints[:, None], axis=0)
        return segment_idx
    
    def _create_event_indicators(self) -> np.ndarray:
        """Create event indicators for event-correlated model."""
        event_indicators = np.zeros(len(self.log_returns))
        
        for _, event in self.events.iterrows():
            if event['date'] in self.log_returns.index:
                event_idx = self.log_returns.index.get_loc(event['date'])
                if event_idx < len(event_indicators):
                    event_indicators[event_idx] = 1
        
        return event_indicators
    
    def _split_into_periods(self) -> List[pd.DataFrame]:
        """Split data into periods for hierarchical model."""
        # Split by decades
        periods = []
        for decade in range(1980, 2030, 10):
            period_data = self.data[self.data.index.year >= decade]
            period_data = period_data[period_data.index.year < decade + 10]
            if len(period_data) > 0:
                periods.append(period_data)
        
        return periods
    
    def _find_event_correlations(self, change_point_dates: List) -> List[Dict]:
        """Find events that correlate with detected change points."""
        correlations = []
        
        for cp_date in change_point_dates:
            for _, event in self.events.iterrows():
                days_diff = abs((cp_date - event['date']).days)
                
                if days_diff <= 30:  # Within 30 days
                    # Calculate price change around event
                    event_idx = self.data.index.get_loc(event['date'])
                    pre_period = self.data.iloc[max(0, event_idx-30):event_idx]['price'].mean()
                    post_period = self.data.iloc[event_idx:min(len(self.data), event_idx+30)]['price'].mean()
                    
                    price_change = ((post_period - pre_period) / pre_period) * 100
                    
                    correlations.append({
                        'change_point_date': cp_date,
                        'event_date': event['date'],
                        'event_type': event['event_type'],
                        'event_description': event['description'],
                        'distance_days': days_diff,
                        'event_impact': price_change
                    })
        
        return correlations
    
    def _compute_impact_measures(self, change_point_dates: List) -> List[Dict]:
        """Compute impact measures for detected change points."""
        impacts = []
        
        for cp_date in change_point_dates:
            cp_idx = self.data.index.get_loc(cp_date)
            
            # Pre and post period analysis
            pre_period = self.data.iloc[max(0, cp_idx-30):cp_idx]['price']
            post_period = self.data.iloc[cp_idx:min(len(self.data), cp_idx+30)]['price']
            
            if len(pre_period) > 0 and len(post_period) > 0:
                price_change = ((post_period.mean() - pre_period.mean()) / pre_period.mean()) * 100
                volatility_change = (post_period.std() - pre_period.std()) / pre_period.std() * 100
                
                impacts.append({
                    'change_point_date': cp_date,
                    'price_change': price_change,
                    'volatility_change': volatility_change,
                    'pre_mean': pre_period.mean(),
                    'post_mean': post_period.mean(),
                    'pre_std': pre_period.std(),
                    'post_std': post_period.std()
                })
        
        return impacts
    
    def _compute_diagnostics(self, trace) -> Dict:
        """Compute model diagnostics."""
        return {
            'r_hat': az.rhat(trace),
            'effective_sample_size': az.ess(trace),
            'divergences': trace.sample_stats.diverging.sum().values
        }


def main():
    """Demonstrate the change point analysis."""
    # Load data
    data = pd.read_csv('../data/processed/brent_oil_prices_processed.csv', index_col=0)
    data.index = pd.to_datetime(data.index)
    
    events = pd.read_csv('../data/processed/major_events.csv')
    events['date'] = pd.to_datetime(events['date'])
    
    # Initialize analysis
    cpa = BayesianChangePointAnalysis(data, events)
    
    # Fit different models
    print("Fitting single change point model...")
    single_model = cpa.single_change_point_model()
    single_results = cpa.fit_model(single_model, 'single_change_point')
    
    print("Fitting event-correlated model...")
    event_model = cpa.event_correlated_model()
    event_results = cpa.fit_model(event_model, 'event_correlated')
    
    # Analyze results
    single_analysis = cpa.analyze_change_points('single_change_point')
    event_analysis = cpa.analyze_change_points('event_correlated')
    
    print("Single Change Point Analysis:")
    print(f"Detected change points: {single_analysis['change_points']}")
    print(f"Event correlations: {len(single_analysis['event_correlations'])}")
    
    print("\nEvent-Correlated Analysis:")
    print(f"Detected change points: {event_analysis['change_points']}")
    print(f"Event correlations: {len(event_analysis['event_correlations'])}")
    
    # Plot results
    cpa.plot_results('single_change_point', 'docs/single_change_point_analysis.png')
    cpa.plot_results('event_correlated', 'docs/event_correlated_analysis.png')
    
    return cpa


if __name__ == "__main__":
    main()
