# Air Prediction Modelling Pipeline

## Phase 1: Library Dependencies & Project Structure

### 1.1 Core Libraries Installation

**Purpose**: Install essential libraries for data manipulation, analysis, and modeling

```bash
# Data manipulation and analysis
pip install pandas numpy scipy

# Machine learning
pip install scikit-learn

# Visualization
pip install matplotlib seaborn plotly

# Geospatial analysis
pip install geopandas folium shapely

# API requests and web scraping
pip install requests beautifulsoup4 lxml

# Time series and datetime
pip install pytz

# Progress bars and utilities
pip install tqdm

# Jupyter notebook extensions (if using notebooks)
pip install ipywidgets
```

**Why these libraries?**

- **pandas/numpy**: Core data manipulation - you'll spend 60% of your time cleaning and reshaping data
- **scikit-learn**: Contains all the ML algorithms mentioned in your proposal (Random Forest, SVM, etc.)
- **geopandas/folium**: Essential for London borough mapping and spatial analysis
- **requests**: Critical for API calls to LAQN, TfL, Met Office
- **plotly**: Interactive visualizations will make your thesis more compelling

### 1.2 Project Directory Structure

**Purpose**: Organize your code for maintainability and reproducibility

```
your_thesis_project/
├── data/
│   ├── raw/                    # Original API responses
│   ├── processed/              # Cleaned datasets
│   └── external/              # Reference data (borough boundaries, etc.)
├── src/
│   ├── data_extraction.py
│   ├── data_cleaning.py
│   ├── feature_engineering.py
│   ├── models.py
│   └── visualization.py
├── notebooks/                 # Jupyter notebooks for exploration
├── config/
│   └── config.py             # API keys, parameters
├── tests/                    # Unit tests (recommended)
├── results/                  # Model outputs, figures
└── requirements.txt
```

## Phase 2: Data Sources & API Understanding

### 2.1 London Air Quality Network (LAQN) - Primary Data Source

**Purpose**: This is your main pollution data source - understand it thoroughly

**Key API Endpoints to Explore:**

- Site information: `https://api.erg.ic.ac.uk/AirQuality/Information/MonitoringSites/`
- Historical data: `https://api.erg.ic.ac.uk/AirQuality/Data/SiteSpecies/`

**What you need to understand:**

- **Site codes**: Each monitoring station has a unique code (e.g., "MY1" for Marylebone Road)
- **Species codes**: Pollutants have codes (NO2=NO2, PM2.5=PM25, etc.)
- **Data format**: Usually hourly measurements with timestamps
- **Geographic coverage**: ~100+ sites across London with varying pollutant coverage

**Critical questions to answer:**

```python
# Create this analysis first
def analyze_laqn_coverage():
    """
    - How many sites monitor NO2 vs PM2.5?
    - Which sites have the longest historical records?
    - What's the typical data completeness (% missing values)?
    - Which boroughs are under-represented?
    """
```

### 2.2 Transport for London (TfL) Data

**Purpose**: Traffic data correlation with pollution levels

**Key datasets:**

- Traffic counts by road segment
- Traffic flow data
- Road network data

**Implementation note**: TfL data might be more complex to integrate spatially - start with borough-level aggregations

### 2.3 Met Office Weather Data

**Purpose**: Weather conditions strongly influence pollution dispersion

**Critical variables:**

- Temperature (affects chemical reactions)
- Wind speed/direction (dispersion)
- Humidity (particle formation)
- Atmospheric pressure (inversion layers)

## Phase 3: Data Extraction Implementation

### 3.1 Create Robust Data Fetchers

**Purpose**: Build reliable, error-handling data extraction functions

```python
# Example structure for data_extraction.py
class LAQNDataFetcher:
    def __init__(self, base_url, rate_limit_delay=1):
        """
        Rate limiting is crucial - LAQN API has limits
        Caching prevents re-downloading same data
        Error handling for network issues
        """
    
    def get_site_list(self):
        """Get all monitoring sites with their coordinates and pollutants"""
    
    def get_historical_data(self, site_code, species, start_date, end_date):
        """Fetch pollution measurements for specific site and time period"""
    
    def batch_download(self, sites, species_list, date_range):
        """Download multiple sites/pollutants efficiently"""
```

**Why this structure matters:**

- APIs fail - you need retry logic
- Rate limits exist - respect them or get blocked
- Data is large - implement caching to avoid re-downloads
- Reproducibility - same inputs should give same outputs

### 3.2 Data Validation During Extraction

**Purpose**: Catch data quality issues early

```python
def validate_pollution_data(df):
    """
    Check for:
    - Negative pollution values (impossible)
    - Values exceeding physical limits (NO2 > 1000 µg/m³ is suspicious)
    - Timestamp gaps
    - Duplicate timestamps
    - Missing coordinate information
    """
```

## Phase 4: Data Cleaning & Quality Assessment

### 4.1 Missing Data Strategy

**Purpose**: Air quality data commonly has 10-30% missing values

**Approach by missing data type:**

- **Random missing**: Linear interpolation for short gaps (<3 hours)
- **Systematic missing**: Equipment maintenance periods - flag but don't interpolate
- **Seasonal missing**: Some pollutants not measured in winter - document limitations

```python
def handle_missing_data(df, max_gap_hours=3):
    """
    1. Identify missing data patterns
    2. Short gaps: interpolate
    3. Long gaps: leave as NaN, flag in metadata
    4. Document data completeness by site/pollutant
    """
```

### 4.2 Outlier Detection and Treatment

**Purpose**: Environmental sensors malfunction, creating extreme values

**Multi-stage approach:**

1. **Physical limits**: NO2 can't be negative or >2000 µg/m³ in London
2. **Statistical outliers**: Values >3 standard deviations from site mean
3. **Temporal outliers**: Sudden spikes not correlated with nearby sites
4. **Spatial outliers**: Site readings very different from neighbors

**Important**: Don't just remove outliers - pollution spikes are real events you want to predict

### 4.3 Timestamp Standardization

**Purpose**: Different data sources use different time zones and formats

```python
def standardize_timestamps(df):
    """
    - Convert all to UTC
    - Ensure hourly intervals
    - Handle daylight saving transitions
    - Create consistent datetime index
    """
```

## Phase 5: Feature Engineering - The Core of Your Model

### 5.1 Temporal Features (High Impact)

**Purpose**: Pollution has strong time-based patterns

**Essential features:**

```python
def create_temporal_features(df):
    """
    Hour of day (0-23): Rush hour patterns
    Day of week (0-6): Weekend effects
    Month (1-12): Seasonal variations
    Season (categorical): Heating season vs summer
    Is_weekend (binary): Different activity patterns
    Is_rush_hour (binary): Traffic correlation
    Holiday indicators: Reduced emissions
    """
```

**Why these matter:**

- NO2 peaks at 8am and 6pm (rush hours)
- PM2.5 higher in winter (heating)
- Weekends have different patterns
- Bank holidays = lower pollution

### 5.2 Lagged Features (Critical for Prediction)

**Purpose**: Previous pollution levels predict future levels

```python
def create_lagged_features(df, pollutant_cols):
    """
    Previous 1, 3, 6, 12, 24 hours: Direct correlation
    Rolling means (3h, 6h, 12h): Smoothed trends
    Rolling std (6h): Variability measures
    First differences: Rate of change
    """
```

**Implementation note**: Be careful about data leakage - only use past information to predict future

### 5.3 Weather Integration

**Purpose**: Weather strongly influences pollution dispersion

**Key transformations:**

```python
def create_weather_features(weather_df):
    """
    Wind components: u_wind = speed * cos(direction)
                    v_wind = speed * sin(direction)
    Temperature categories: Cold (<5°C), Mild (5-20°C), Warm (>20°C)
    Precipitation binary: Rain affects particle washout
    Pressure trends: Rising/falling pressure
    Atmospheric stability indicators
    """
```

### 5.4 Spatial Features

**Purpose**: Location determines pollution sources and dispersion

```python
def create_spatial_features(df):
    """
    Distance to major roads: Traffic influence
    Borough classification: Different emission patterns
    Population density: Proxy for emission intensity
    Land use type: Residential vs industrial vs commercial
    Elevation: Affects dispersion patterns
    """
```

## Phase 6: Exploratory Data Analysis (EDA) - Critical Insights

### 6.1 Temporal Pattern Analysis

**Purpose**: Understand the data before modeling

```python
def analyze_temporal_patterns(df):
    """
    Hourly cycles: Create heatmaps showing hour vs day-of-week
    Seasonal trends: Month-by-month box plots
    Weekend effects: Compare weekday vs weekend distributions
    Holiday impacts: Before/during/after major holidays
    """
```

**What to look for:**

- Rush hour spikes in NO2
- Winter peaks in PM2.5
- Sunday morning lows
- Christmas/New Year drops

### 6.2 Spatial Analysis

**Purpose**: Understand pollution geography

```python
def analyze_spatial_patterns(df):
    """
    Site clustering: Which sites behave similarly?
    Borough comparisons: Central vs outer London
    Traffic correlation: Sites near major roads vs background
    Hotspot identification: Consistently high pollution areas
    """
```

### 6.3 Weather Correlations

**Purpose**: Quantify meteorological influences

```python
def analyze_weather_correlations(df):
    """
    Wind speed vs pollution: Higher wind = lower pollution
    Temperature effects: Different for different pollutants
    Precipitation impact: Washout effects
    Pressure correlations: Inversion layer formation
    """
```

## Phase 7: Model Development Strategy

### 7.1 Data Splitting Strategy

**Purpose**: Avoid temporal data leakage in time series

```python
def split_time_series_data(df, train_ratio=0.7, val_ratio=0.15):
    """
    Time-based split (NOT random):
    - Training: Oldest 70% of data
    - Validation: Next 15%
    - Test: Most recent 15%
    
    This mimics real prediction scenario
    """
```

### 7.2 Baseline Models Implementation

**Purpose**: Start simple, establish performance benchmarks

```python
class BaselineModels:
    def persistence_model(self, df):
        """Use previous hour's value as prediction"""
    
    def seasonal_naive(self, df):
        """Use same hour from previous week"""
    
    def linear_regression(self, X, y):
        """Simple linear relationships"""
    
    def moving_average(self, df, window=24):
        """Smoothed trend predictions"""
```

**Why baselines matter**: If your complex model doesn't beat simple persistence, something's wrong

### 7.3 Advanced Model Implementation

**Purpose**: Implement the algorithms from your proposal

```python
class PollutionModels:
    def random_forest_model(self, X_train, y_train):
        """
        Hyperparameters to tune:
        - n_estimators: Start with 100
        - max_depth: Prevent overfitting
        - min_samples_split: Minimum samples to split
        - feature subsampling: Reduce correlation
        """
    
    def support_vector_regression(self, X_train, y_train):
        """
        Key parameters:
        - Kernel: RBF for non-linear relationships
        - C: Regularization strength
        - epsilon: Tolerance for errors
        """
    
    def neural_network_model(self, X_train, y_train):
        """Start simple: 1-2 hidden layers"""
```

## Phase 8: Model Evaluation Framework

### 8.1 Evaluation Metrics Implementation

**Purpose**: Multiple metrics reveal different aspects of model performance

```python
def evaluate_model(y_true, y_pred):
    """
    RMSE: Penalizes large errors heavily
    MAE: Average absolute error, more robust to outliers
    R²: Proportion of variance explained
    MAPE: Percentage error, good for interpretation
    Nash-Sutcliffe Efficiency: Hydrology standard
    """
```

### 8.2 Error Analysis

**Purpose**: Understand when and where models fail

```python
def analyze_prediction_errors(y_true, y_pred, features):
    """
    Error by hour: When do predictions fail?
    Error by season: Seasonal model weaknesses?
    Error by pollution level: Worse for high pollution?
    Error by location: Which sites are hardest to predict?
    """
```

## Phase 9: Visualization Strategy

### 9.1 Model Performance Visualization

```python
def create_performance_plots():
    """
    Predicted vs Actual scatter plots
    Residual plots: Check for patterns in errors
    Time series overlay: Show prediction accuracy over time
    Error distribution histograms
    """
```

### 9.2 Spatial Visualization

```python
def create_maps():
    """
    Borough-level pollution maps using folium
    Monitoring site locations
    Prediction accuracy by location
    Traffic density overlays
    """
```

## Current Status Tracking

### Phase Completion Checklist:

- [ ] **Phase 1**: Environment setup ✓ (you mentioned this is done)
- [ ] **Phase 2**: Data source exploration
- [ ] **Phase 3**: Data extraction pipeline
- [ ] **Phase 4**: Data cleaning implementation
- [ ] **Phase 5**: Feature engineering
- [ ] **Phase 6**: EDA and pattern analysis
- [ ] **Phase 7**: Model development
- [ ] **Phase 8**: Evaluation framework
- [ ] **Phase 9**: Visualization

## Implementation Priority Order

### Week 1-2: Data Foundation

1. Explore LAQN API and understand data structure
2. Extract 3 months of NO2 data from 10 London sites
3. Basic data cleaning and validation

### Week 3-4: Feature Engineering

1. Implement temporal features
2. Add weather data integration
3. Create lagged features

### Week 5-6: Baseline Modeling

1. Implement persistence and linear models
2. Add Random Forest
3. Establish evaluation framework

### Week 7+: Advanced Development

1. Add more pollutants and sites
2. Implement neural networks
3. Advanced visualization and interpretation

## Critical Success Factors

1. **Start Small**: 1 pollutant, few sites, short time period
2. **Validate Early**: Check data quality before complex modeling
3. **Document Everything**: Your thesis needs to explain all decisions
4. **Version Control**: Git commit frequently with meaningful messages
5. **Test Assumptions**: Verify that your feature engineering makes sense