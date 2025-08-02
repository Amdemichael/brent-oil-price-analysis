# Brent Oil Price Analysis

## Project Overview

This project analyzes how major geopolitical events, economic shocks, and policy changes affect Brent oil prices using Bayesian change point analysis. The analysis covers daily Brent oil prices from May 20, 1987, to September 30, 2022.

## Business Objective

The main goal is to study how important events affect Brent oil prices, focusing on:
- Political decisions and conflicts in oil-producing regions
- Global economic sanctions
- OPEC policy changes
- Economic shocks and market volatility

This analysis provides insights for investors, analysts, and policymakers to better understand and react to oil price changes.

## Project Structure

```
brent-oil-price-analysis/
├── data/
│   └── raw/
│       └── BrentOilPrices.csv          # Historical Brent oil prices
├── notebooks/
│   ├── 01_data_exploration.ipynb      # Initial data exploration
│   ├── 02_change_point_analysis.ipynb  # Bayesian change point analysis
│   └── 03_event_correlation.ipynb     # Event correlation analysis
├── src/
│   ├── analysis/                       # Core analysis modules
│   │   ├── change_point.py            # Change point detection
│   │   ├── event_research.py          # Event data compilation
│   │   └── impact_analysis.py         # Impact quantification
│   ├── backend/                       # Flask API backend
│   └── frontend/                      # React dashboard frontend
└── requirements.txt                   # Python dependencies
```

## Key Features

- **Bayesian Change Point Analysis**: Using PyMC3 for robust statistical modeling
- **Event Correlation**: Linking price changes to specific geopolitical events
- **Interactive Dashboard**: Real-time visualization of analysis results
- **Statistical Validation**: Comprehensive model diagnostics and validation

## Methodology

1. **Data Preparation**: Clean and preprocess historical price data
2. **Exploratory Analysis**: Identify trends, seasonality, and volatility patterns
3. **Change Point Detection**: Apply Bayesian models to identify structural breaks
4. **Event Correlation**: Map detected changes to historical events
5. **Impact Quantification**: Measure the magnitude of event impacts
6. **Visualization**: Create interactive dashboards for stakeholder communication

## Getting Started

1. Install dependencies: `pip install -r requirements.txt`
2. Run Jupyter notebooks for analysis: `jupyter notebook notebooks/`
3. Start the dashboard: `docker-compose up`

## Key Insights

- Identifies statistically significant structural breaks in oil prices
- Quantifies the impact of major geopolitical events
- Provides probabilistic assessments of price changes
- Supports data-driven decision making for energy sector stakeholders