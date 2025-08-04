# Brent Oil Price Analysis Dashboard

## Business Objective

The main goal of this analysis is to study how important events affect Brent oil prices. This focuses on finding out how changes in oil prices are linked to big events like political decisions, conflicts in oil-producing regions, global economic sanctions, and changes in Organization of the Petroleum Exporting Countries (OPEC) policies.

## Project Overview

This project provides a comprehensive analysis of Brent oil price movements and their correlation with geopolitical and economic events. It includes:

- **Bayesian Change Point Analysis**: Using PyMC3 to identify structural breaks in oil price behavior
- **Event Impact Analysis**: Quantifying the impact of key events on oil prices
- **Interactive Dashboard**: Web-based visualization platform for stakeholders
- **Comprehensive Event Database**: 15+ key events from 1990-2022

## Features

### Core Analysis
- **Change Point Detection**: Bayesian analysis to identify when oil price behavior fundamentally changes
- **Event Correlation**: Mapping detected change points to historical events
- **Impact Quantification**: Measuring price changes before and after events
- **Statistical Validation**: MCMC convergence checks and uncertainty quantification

### Interactive Dashboard
- **Real-time Data Visualization**: Dynamic charts showing price trends and events
- **Event Filtering**: Filter by category, region, and date range
- **Impact Analysis**: Bar charts and pie charts showing event impacts
- **Change Point Analysis**: Run and visualize Bayesian change point detection

### Key Events Analyzed
- Gulf War (1990-1991)
- Asian Financial Crisis (1997-1998)
- 9/11 Attacks (2001)
- Iraq War (2003)
- Global Financial Crisis (2008)
- Arab Spring (2011)
- US Shale Revolution (2012-2014)
- OPEC Price War (2014)
- COVID-19 Pandemic (2020)
- Russia-Ukraine War (2022)

## Technology Stack

### Backend
- **Python 3.8+**
- **Flask**: Web framework for API
- **PyMC3**: Bayesian modeling and MCMC
- **Pandas/NumPy**: Data manipulation
- **Matplotlib/Seaborn**: Static visualizations

### Frontend
- **React 18**: User interface
- **Recharts**: Interactive charts
- **Axios**: API communication
- **CSS Grid/Flexbox**: Responsive design

## Installation and Setup

### Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher
- Git

### Backend Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd brent-oil-price-analysis
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Flask backend**:
   ```bash
   cd src/backend
   python app.py
   ```
   The API will be available at `http://localhost:5000`

### Frontend Setup

1. **Navigate to the frontend directory**:
   ```bash
   cd src/frontend/oil-price-dashboard
   ```

2. **Install Node.js dependencies**:
   ```bash
   npm install
   ```

3. **Start the React development server**:
   ```bash
   npm start
   ```
   The dashboard will be available at `http://localhost:3000`

## Usage

### Running the Analysis

1. **Start the backend server** (see Backend Setup above)

2. **Start the frontend dashboard** (see Frontend Setup above)

3. **Access the dashboard** at `http://localhost:3000`

### Using the Dashboard

1. **View Price Timeline**: See Brent oil prices with event markers
2. **Filter Events**: Use the controls panel to filter by category, region, or date
3. **Run Change Point Analysis**: Click "Run Analysis" to perform Bayesian change point detection
4. **Explore Impact Analysis**: View charts showing event impacts and correlations

### API Endpoints

- `GET /api/health` - Health check
- `GET /api/data/summary` - Data summary statistics
- `GET /api/data/prices` - Oil price data with optional filtering
- `GET /api/events` - Event data with optional filtering
- `GET /api/analysis/change-points` - Change point analysis results
- `GET /api/analysis/event-impacts` - Event impact analysis
- `POST /api/analysis/run-change-point` - Run change point analysis

## Project Structure

```
brent-oil-price-analysis/
├── data/
│   ├── raw/
│   │   └── BrentOilPrices.csv          # Historical oil price data
│   ├── processed/                       # Processed data files
│   └── outputs/                         # Analysis results and plots
├── src/
│   ├── analysis/                        # Core analysis modules
│   │   ├── change_point.py             # Bayesian change point analysis
│   │   ├── event_research.py           # Event database and research
│   │   └── impact_analysis.py          # Event impact analysis
│   ├── backend/                         # Flask API
│   │   ├── app.py                      # Main Flask application
│   │   └── requirements.txt            # Python dependencies
│   └── frontend/                        # React dashboard
│       └── oil-price-dashboard/
│           ├── src/
│           │   ├── components/         # React components
│           │   │   ├── Charts/         # Chart components
│           │   │   ├── Controls/       # Control components
│           │   │   └── InfoPanels/     # Info panel components
│           │   ├── App.js              # Main React app
│           │   └── App.css             # Styles
│           └── package.json            # Node.js dependencies
├── notebooks/                           # Jupyter notebooks
│   ├── 01_data_exploration.ipynb      # Task 1: Data exploration
│   ├── 02_change_point_analysis.ipynb  # Task 2: Change point analysis
│   └── 03_event_correlation.ipynb     # Task 3: Event correlation
├── requirements.txt                     # Main Python dependencies
└── README.md                           # This file
```

## Key Findings

### Change Point Analysis
- Successfully identified structural breaks in Brent oil price behavior
- Bayesian approach provided probabilistic estimates with uncertainty quantification
- Model converged successfully with R-hat values close to 1.0

### Event Impact Analysis
- Strong correlations found between detected change points and major events
- Events with highest impact include financial crises, OPEC decisions, and military conflicts
- Regional analysis shows Middle East events have significant impact

### Business Insights
- **Investors**: Can use change point analysis for risk management
- **Policymakers**: Can anticipate market reactions to geopolitical events
- **Energy Companies**: Can plan operations around expected price volatility

## Limitations and Assumptions

### Statistical Limitations
- **Correlation vs Causation**: Analysis identifies statistical correlations but cannot prove causality
- **Market Efficiency**: Assumes markets react to events within reasonable timeframes
- **Single Change Point**: Current model detects one change point; multiple regime changes may exist

### Data Limitations
- **Event Timing**: Uses approximate dates for events
- **Data Quality**: Assumes Brent oil price data is accurate and complete
- **Event Coverage**: Limited to major events; smaller events may also impact prices

## Future Work

### Advanced Modeling
- **Multiple Change Points**: Implement models to detect multiple structural breaks
- **VAR Models**: Vector Autoregression for dynamic relationships
- **Markov-Switching**: Explicit regime-switching models

### Additional Data Sources
- **Macroeconomic Variables**: GDP, inflation, exchange rates
- **Supply/Demand Data**: Production, consumption, inventory levels
- **Sentiment Analysis**: News sentiment and social media data

### Real-time Monitoring
- **Live Data Integration**: Real-time oil price feeds
- **Event Detection**: Automated detection of new events
- **Alert System**: Notifications for significant price movements

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- **Birhan Energies**: For the business context and requirements
- **PyMC3 Community**: For the Bayesian modeling framework
- **React/Recharts**: For the interactive visualization capabilities

## Contact

For questions or support, please contact the development team or create an issue in the repository.

---

**Note**: This project is part of a data science challenge focused on Bayesian analysis and energy market insights. The analysis provides valuable insights for investors, policymakers, and energy companies navigating the complex oil market landscape.