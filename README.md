# London Air Pollution Prediction

Machine learning project for predicting NO2 and PM2.5 air pollution levels in London using historical air quality data, meteorological conditions, and traffic patterns. This research aims to create accurate, interpretable models that can assist in environmental policy planning and public health protection.

## Project Overview

This project develops predictive models using time series analysis and ensemble machine learning approaches to forecast air pollution concentrations across London. The methodology integrates multiple data sources including air quality monitoring networks, weather observations, and traffic data to capture the complex relationships affecting urban air pollution.

**Academic Context**: MSc Thesis Project - Data Science  
**Approach**: Time series prediction using ensemble machine learning methods  
**Target Variables**: NO2 and PM2.5 concentrations  

## Project Structure

```
air-pollution-levels/
├── data/                       # Data storage
│   ├── LAQN/              # Reference data
│   ├──--├─external/              # Reference data
│   ├──--├ processed/             # Cleaned datasets
│   └──--├ raw/                   # Original API responses
├── docs/                      # Documentation
│   └── api_guide.md          # How to use API?
├── results/                   # Model outputs and figures
│   ├── figures/              # Visualizations
│   └── models/               # Trained models
├── src/                      # Source code modules
│   └── __init__.py
│   └──LAQN_get/              #LAQN Api Code files
│   ├──--| get.py              # Getting data from LAQN API points         
├── tests/                    # Testing framework
│   ├── __init__.py          
│   └── laqn_test.py          # laqn_test
├── config.py                 # Project configuration
├── main.py                   # Main execution script
├── requirements.txt          # Python dependencies
└── todo.md                   # Task tracking
```

## Data Sources

**London Air Quality Network (LAQN)**
- Primary source for pollution monitoring data
- Over 100 monitoring sites across Greater London
- Hourly measurements of NO2, PM2.5, PM10, and other pollutants
- API endpoint: https://api.erg.ic.ac.uk/AirQuality

**Open-Meteo Weather API**
- Historical meteorological data for London
- Hourly weather observations including temperature, humidity, wind conditions
- Geographic coverage: London metropolitan area
- API endpoint: https://api.open-meteo.com/v1

**Transport for London (TfL) API**
- Traffic flow and congestion data
- Public transport usage statistics
- Road network information
- Planned integration for advanced modeling

## Technical Setup

### Requirements

The project requires Python 3.8 or higher with the following core dependencies:

```
pandas>=1.5.0
numpy>=1.21.0
scikit-learn>=1.2.0
matplotlib>=3.6.0
seaborn>=0.12.0
plotly>=5.15.0
requests>=2.28.0
geopandas>=0.12.0
folium>=0.14.0
statsmodels>=0.13.0
```

### Installation

Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

**Note**: The virtual environment is integrated as `api venv`. Running `ap venv` will automatically activate this project's virtual environment.

### Configuration

The project uses centralized configuration management through `config.py`:

```python
# Key configuration parameters
POLLUTANTS = ['NO2', 'PM25']
START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2024, 6, 30)
LONDON_CENTER = {'lat': 51.5074, 'lon': -0.1278}
PRIORITY_SITES = ['MY1', 'BG1', 'CT1', 'RB1', 'TD1']
```

### API Testing

Verify API connectivity before data collection:

```bash
python tests/test_api.py
```

Expected output shows successful connection to both LAQN and weather APIs with site information retrieval and sample data access.

### Running the Application

Execute the main application:

```bash
python main.py
```

## Methodology

### Data Collection
- Automated retrieval from multiple APIs
- Quality validation and error handling
- Temporal alignment of datasets
- Geographic coordinate mapping

### Feature Engineering
- Temporal features: hour, day, season, holiday indicators
- Meteorological features: temperature, wind, humidity, pressure
- Spatial features: distance from roads, borough classification
- Lag features: previous pollution levels, rolling averages

### Modeling Approach
- Baseline models: persistence, seasonal naive, linear regression
- Advanced algorithms: Random Forest, Support Vector Regression
- Deep learning: LSTM networks for temporal patterns
- Ensemble methods: weighted averaging and stacking

### Evaluation Framework
- Time-based train/validation/test splits
- Multiple performance metrics: RMSE, MAE, R-squared
- Statistical significance testing
- Error analysis and model interpretation

## Data Processing Pipeline

The analysis follows a structured workflow:

1. **Data Collection**: Retrieve historical data from APIs
2. **Quality Assessment**: Validate completeness and identify outliers  
3. **Preprocessing**: Clean and standardize temporal resolution
4. **Feature Engineering**: Create predictive features from raw data
5. **Model Training**: Implement and tune multiple algorithms
6. **Evaluation**: Compare performance and select best approaches
7. **Interpretation**: Analyze feature importance and model behavior

## Geographic Scope

The project focuses on Greater London with particular attention to:
- Central London monitoring sites with high data completeness
- Major traffic corridors and pollution hotspots
- Representative sites across different borough types
- Coastal vs inland location differences

Priority monitoring sites include Marylebone Road (MY1), Bloomsbury (BG1), Camden Town (CT1), Richmond (RB1), and Tower Hamlets (TD1).

## Expected Outcomes

The research aims to produce:
- Accurate pollution prediction models for policy planning
- Understanding of key factors driving air pollution variations
- Spatial and temporal pattern analysis across London
- Recommendations for monitoring network optimization
- Open source tools for environmental data analysis

## Development Environment

The project is developed using:
- Python 3.9 with scientific computing libraries
- Jupyter notebooks for exploratory analysis
- Git version control with structured commit history
- Modular code organization for maintainability and testing

## API Integration

All external data sources are accessed through RESTful APIs with comprehensive error handling, rate limiting, and retry mechanisms. The system is designed to handle temporary service interruptions and data quality issues gracefully.

Configuration parameters allow easy switching between development and production environments, with different data sampling strategies for testing versus full analysis.

## Reproducibility

The complete analysis pipeline is designed for reproducibility with:
- Fixed random seeds for model training
- Versioned dependency management
- Documented API endpoints and parameters
- Automated testing of data collection processes

All code follows Python best practices with comprehensive documentation, type hints where appropriate, and modular design for easy extension and modification.
=======
# london-air-quality-prediction
MSc dissertation project predicting air pollution levels across London using machine learning. Combines environmental data from LAQN, TfL traffic data, and meteorological APIs to forecast NO2 and PM2.5 concentrations with seasonal pattern analysis.
>>>>>>> 81c0db85f01978b8b4a4201cddb5b87db8f3b774
