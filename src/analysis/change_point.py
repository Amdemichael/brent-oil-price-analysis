"""
Change Point Analysis Module

This module implements Bayesian change point analysis using PyMC3 to identify
structural breaks in Brent oil price time series.
"""

import pandas as pd
import numpy as np
import pymc as pm
import arviz as az
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')


class ChangePointAnalyzer:
    """
    A class for performing Bayesian change point analysis on Brent oil price data.
    """
    
    def __init__(self, data: pd.DataFrame):
        """
        Initialize the change point analyzer.
        
        Args:
            data (pd.DataFrame): DataFrame with 'Date' and 'Price' columns
        """
        self.data = data.copy()
        
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
        
        self.data['Date'] = self.data['Date'].apply(parse_date)
        self.data = self.data.sort_values('Date').reset_index(drop=True)
        
        # Calculate log returns for better modeling
        self.data['log_returns'] = np.log(self.data['Price'] / self.data['Price'].shift(1))
        self.data = self.data.dropna().reset_index(drop=True)
        
        # Model results storage
        self.trace = None
        self.model = None
        self.change_points = None
        
    def build_model(self, n_changepoints: int = 1) -> pm.Model:
        """
        Build a Bayesian change point model using PyMC3.
        
        Args:
            n_changepoints (int): Number of change points to detect
            
        Returns:
            pm.Model: PyMC3 model
        """
        n_data = len(self.data)
        
        with pm.Model() as model:
            # Prior for change point locations
            if n_changepoints == 1:
                tau = pm.DiscreteUniform('tau', lower=0, upper=n_data-1)
            else:
                tau = pm.DiscreteUniform('tau', lower=0, upper=n_data-1, shape=n_changepoints)
            
            # Priors for means before and after change points
            mu_1 = pm.Normal('mu_1', mu=0, sigma=1)
            mu_2 = pm.Normal('mu_2', mu=0, sigma=1)
            
            # Prior for standard deviation
            sigma = pm.HalfNormal('sigma', sigma=1)
            
            # Define the mean function with change points
            if n_changepoints == 1:
                mu = pm.math.switch(tau >= np.arange(n_data), mu_1, mu_2)
            else:
                # For multiple change points, we need a more complex switch function
                mu = mu_1  # Simplified for now
            
            # Likelihood
            returns = self.data['log_returns'].values
            likelihood = pm.Normal('likelihood', mu=mu, sigma=sigma, observed=returns)
            
        self.model = model
        return model
    
    def fit_model(self, n_changepoints: int = 1, draws: int = 2000, 
                  tune: int = 1000, chains: int = 2) -> az.InferenceData:
        """
        Fit the change point model using MCMC sampling.
        
        Args:
            n_changepoints (int): Number of change points to detect
            draws (int): Number of posterior samples
            tune (int): Number of tuning steps
            chains (int): Number of MCMC chains
            
        Returns:
            az.InferenceData: ArviZ inference data object
        """
        print("Building model...")
        model = self.build_model(n_changepoints)
        
        print("Running MCMC sampling...")
        with model:
            self.trace = pm.sample(draws=draws, tune=tune, chains=chains, 
                                 return_inferencedata=True)
        
        print("Model fitting completed!")
        return self.trace
    
    def analyze_change_points(self, window_days: int = 30) -> Dict:
        """
        Analyze the detected change points and their characteristics.
        
        Args:
            window_days (int): Number of days to analyze around change points
            
        Returns:
            Dict: Analysis results
        """
        if self.trace is None:
            raise ValueError("Model must be fitted before analyzing change points")
        
        # Get posterior samples of change point location
        tau_samples = self.trace.posterior['tau'].values.flatten()
        
        # Calculate most probable change point
        tau_most_probable = int(np.median(tau_samples))
        change_point_date = self.data.iloc[tau_most_probable]['Date']
        
        # Calculate credible interval
        tau_ci = np.percentile(tau_samples, [5, 95])
        change_point_ci = [
            self.data.iloc[int(tau_ci[0])]['Date'],
            self.data.iloc[int(tau_ci[1])]['Date']
        ]
        
        # Analyze price behavior before and after change point
        before_window = self.data.iloc[max(0, tau_most_probable-window_days):tau_most_probable]
        after_window = self.data.iloc[tau_most_probable:min(len(self.data), tau_most_probable+window_days)]
        
        # Calculate statistics
        before_stats = {
            'mean_price': before_window['Price'].mean(),
            'std_price': before_window['Price'].std(),
            'mean_volatility': before_window['log_returns'].std(),
            'trend': np.polyfit(range(len(before_window)), before_window['Price'], 1)[0]
        }
        
        after_stats = {
            'mean_price': after_window['Price'].mean(),
            'std_price': after_window['Price'].std(),
            'mean_volatility': after_window['log_returns'].std(),
            'trend': np.polyfit(range(len(after_window)), after_window['Price'], 1)[0]
        }
        
        # Calculate impact metrics
        price_change = after_stats['mean_price'] - before_stats['mean_price']
        price_change_pct = (price_change / before_stats['mean_price']) * 100
        volatility_change = after_stats['mean_volatility'] - before_stats['mean_volatility']
        
        self.change_points = {
            'change_point_date': change_point_date,
            'change_point_index': tau_most_probable,
            'credible_interval': change_point_ci,
            'before_stats': before_stats,
            'after_stats': after_stats,
            'price_change': price_change,
            'price_change_pct': price_change_pct,
            'volatility_change': volatility_change,
            'tau_samples': tau_samples
        }
        
        return self.change_points
    
    def plot_change_point_analysis(self, save_path: Optional[str] = None) -> None:
        """
        Create comprehensive plots for change point analysis.
        
        Args:
            save_path (Optional[str]): Path to save the plot
        """
        if self.change_points is None:
            raise ValueError("Must run analyze_change_points() first")
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Plot 1: Price series with change point
        axes[0, 0].plot(self.data['Date'], self.data['Price'], alpha=0.7, linewidth=1)
        cp_date = self.change_points['change_point_date']
        cp_price = self.data[self.data['Date'] == cp_date]['Price'].iloc[0]
        axes[0, 0].axvline(x=cp_date, color='red', linestyle='--', alpha=0.8, 
                           label=f'Change Point: {cp_date.strftime("%Y-%m-%d")}')
        axes[0, 0].scatter(cp_date, cp_price, color='red', s=100, zorder=5)
        axes[0, 0].set_title('Brent Oil Price with Detected Change Point')
        axes[0, 0].set_xlabel('Date')
        axes[0, 0].set_ylabel('Price (USD/barrel)')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # Plot 2: Posterior distribution of change point
        tau_samples = self.change_points['tau_samples']
        axes[0, 1].hist(tau_samples, bins=50, alpha=0.7, density=True)
        axes[0, 1].axvline(np.median(tau_samples), color='red', linestyle='--', 
                           label='Median')
        axes[0, 1].set_title('Posterior Distribution of Change Point Location')
        axes[0, 1].set_xlabel('Data Point Index')
        axes[0, 1].set_ylabel('Density')
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)
        
        # Plot 3: Price comparison before/after
        before_price = self.change_points['before_stats']['mean_price']
        after_price = self.change_points['after_stats']['mean_price']
        price_change = self.change_points['price_change_pct']
        
        bars = axes[1, 0].bar(['Before', 'After'], [before_price, after_price], 
                              color=['lightblue', 'lightcoral'], alpha=0.7)
        axes[1, 0].set_title(f'Price Comparison\nChange: {price_change:.2f}%')
        axes[1, 0].set_ylabel('Average Price (USD/barrel)')
        axes[1, 0].grid(True, alpha=0.3)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            axes[1, 0].text(bar.get_x() + bar.get_width()/2., height,
                           f'{height:.2f}', ha='center', va='bottom')
        
        # Plot 4: Volatility comparison
        before_vol = self.change_points['before_stats']['mean_volatility']
        after_vol = self.change_points['after_stats']['mean_volatility']
        vol_change = self.change_points['volatility_change']
        
        bars = axes[1, 1].bar(['Before', 'After'], [before_vol, after_vol], 
                              color=['lightgreen', 'lightyellow'], alpha=0.7)
        axes[1, 1].set_title(f'Volatility Comparison\nChange: {vol_change:.4f}')
        axes[1, 1].set_ylabel('Volatility (log returns std)')
        axes[1, 1].grid(True, alpha=0.3)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            axes[1, 1].text(bar.get_x() + bar.get_width()/2., height,
                           f'{height:.4f}', ha='center', va='bottom')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def get_model_summary(self) -> Dict:
        """
        Get a summary of the model results.
        
        Returns:
            Dict: Model summary
        """
        if self.trace is None:
            raise ValueError("Model must be fitted before getting summary")
        
        summary = az.summary(self.trace)
        
        return {
            'summary_table': summary,
            'diagnostics': {
                'r_hat': summary['r_hat'].to_dict(),
                'effective_sample_size': summary['ess_bulk'].to_dict()
            }
        }
    
    def check_convergence(self) -> bool:
        """
        Check if the MCMC chains have converged.
        
        Returns:
            bool: True if converged, False otherwise
        """
        if self.trace is None:
            raise ValueError("Model must be fitted before checking convergence")
        
        summary = az.summary(self.trace)
        r_hat_values = summary['r_hat'].values
        
        # Check if all R-hat values are close to 1.0 (convergence criterion)
        converged = np.all(r_hat_values < 1.1)
        
        return converged
    
    def export_results(self, filepath: str) -> None:
        """
        Export analysis results to CSV.
        
        Args:
            filepath (str): Path to save the results
        """
        if self.change_points is None:
            raise ValueError("Must run analyze_change_points() first")
        
        results_df = pd.DataFrame([{
            'change_point_date': self.change_points['change_point_date'],
            'price_change_usd': self.change_points['price_change'],
            'price_change_pct': self.change_points['price_change_pct'],
            'volatility_change': self.change_points['volatility_change'],
            'before_mean_price': self.change_points['before_stats']['mean_price'],
            'after_mean_price': self.change_points['after_stats']['mean_price'],
            'before_volatility': self.change_points['before_stats']['mean_volatility'],
            'after_volatility': self.change_points['after_stats']['mean_volatility']
        }])
        
        results_df.to_csv(filepath, index=False)
