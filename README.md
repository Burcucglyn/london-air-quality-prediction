# **Air Pollution Predictive Modelling in London**

Machine learning project predicting PM2.5, PM10, O₃, NO₂, SO₂, CO air pollution levels across London using historical monitoring data, meteorological observations, and traffic patterns. This research develops interpretable models to support environmental policy planning and public health protection.

## Project Overview

This research builds predictive models using time series analysis and machine learning to forecast air pollution concentrations across Greater London. The approach combines data from multiple monitoring networks with weather observations to capture the relationships affecting urban air quality.

## Data Preparation Summary

### LAQN Dataset (Completed)

The London Air Quality Network dataset required extensive preparation through three systematic cleaning stages:

**Initial Collection:**

- 8,709 CSV files from 84 monitoring sites
- January 2023 to November 2025 (35 months)
- 6.09 million hourly measurements
- 47.5% files flagged with quality issues (over 20% missing values)

**Stage 1: Metadata Validation**

- Cross-referenced API endpoints to verify equipment existence
- Identified 38 permanently non-active combinations (equipment never installed)
- Corrected reference metadata: 252 to 216 validated combinations
- Preserved files for audit trail

**Stage 2: Year-Specific Removal**

- Removed 104 combinations showing complete year-long failures
- Deleted 1,248 files representing systematic equipment failures
- Improved issue rate: 47.5% to 26.0%
- Remaining files: 6,179

**Stage 3: Cross-Year Consistency**

- Identified 53 combinations with temporal gaps across years
- Removed 1,247 files (benefit ratio 1.54:1) to ensure ML compatibility
- Final issue rate: 17.2%
- Remaining files: 4,932

**Final Validated Dataset:**

- 4,932 files (43.4% reduction from initial collection)
- 17.2% issue rate (63.8% improvement from baseline)
- 170 validated combinations across 78 sites
- 100% cross-year temporal consistency
- 111 NO₂ and PM2.5 combinations (65.3% of total)
- Complete 35-month coverage for all validated combinations

The dataset transformation from a problematic 47.5% issue rate to an ML-ready 17.2% rate while maintaining 92.9% site retention represents a significant quality improvement. Complete documentation available in `/docs/LAQN_Data_Preparation_Report.md`.

### DEFRA Dataset (In Progress)

Data collection complete for UK Department for Environment, Food and Rural Affairs monitoring network, focused on London bounding box. Initial assessment indicates substantially cleaner data structure compared to LAQN. Detailed preparation documentation forthcoming.

**Current Status:**

- Monthly measurements collected for 2023-2025
- Station metadata validated
- Pollutant mapping complete
- Quality assessment underway

### Meteorological Data (Completed)

Historical weather data from Open-Meteo API covering study period.

**Coverage:**

- Monthly files for 2023, 2024, 2025
- Hourly temporal resolution
- Variables: temperature, wind speed/direction, humidity, pressure, precipitation, cloud cover
- Geographic focus: Greater London area

## Project Structure

```
air-pollution-levels/
├── data/
│   ├── defra/
│   │   ├── 2023measurements/      # Monthly DEFRA data 2023
│   │   ├── 2024measurements/      # Monthly DEFRA data 2024
│   │   ├── 2025measurements/      # Monthly DEFRA data 2025
│   │   ├── optimised/             # Cleaned DEFRA files
│   │   ├── capabilities/          # API metadata
│   │   ├── pollutant_mapping.csv  # Pollutant code reference
│   │   └── test/
│   │       └── london_stations_clean.csv  # DEFRA station metadata
│   │
│   ├── laqn/
│   │   ├── optimased/             # Validated LAQN files (4,932)
│   │   ├── optimased_siteSpecies.csv  # Final metadata (170 combinations)
│   │   ├── missing/               # Quality audit trail
│   │   ├── monthly_data/          # Raw monthly collections
│   │   └── year_2023/             # 2023 annual data
│   │
│   ├── meteo/
│   │   ├── raw/
│   │   │   ├── monthly2023/       # Weather data 2023
│   │   │   ├── monthly2024/       # Weather data 2024
│   │   │   └── monthly2025/       # Weather data 2025
│   │   └── test/
│   │
│   └── inventory_test/            # Dataset inventories
│       ├── laqn_inventory.csv
│       ├── defra_inventory.csv
│       ├── meteo_inventory.csv
│       └── inventory_summary.json
│
├── docs/
│   ├── LAQN_data_quality_cleaning.md  # Complete LAQN preparation process
│   ├── 1Progress-Report.md            # Project progress tracking
│   └── reports.md                     # Analysis reports
│
├── notebooks/
│   ├── laqn/
│   │   ├── laqn_exploration.ipynb     # Initial data discovery
│   │   ├── laqn_check.ipynb           # Quality assessment
│   │   ├── laqn_update.ipynb          # Cleaning implementation
│   │   └── laqn_remove.ipynb          # File removal execution
│   ├── defra/
│   │   └── defra_check.ipynb          # DEFRA quality checks
│   └── cross_check_DEFRA_LAQN.ipynb   # Dataset comparison
│
├── src/
│   ├── getData/
│   │   ├── laqn_get.py            # LAQN API collection
│   │   ├── defra_get.py           # DEFRA API collection
│   │   └── meteo_get.py           # Weather API collection
│   ├── dataset_discovery/
│   │   ├── laqn_analyse.py        # LAQN quality analysis
│   │   └── defra_analyse.py       # DEFRA quality analysis
│   └── data_prep/
│       ├── data_inventory.py      # Dataset cataloguing
│       ├── pollutant_mapps.py     # Pollutant standardisation
│       └── stations.py            # Station metadata handling
│
├── tests/
│   └── raw_data/
│       ├── laqn_test.py           # LAQN pipeline tests
│       ├── defra_test.py          # DEFRA pipeline tests
│       └── meteo_test.py          # Weather pipeline tests
│
├── config.py                       # Project configuration
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## Data Sources

### Primary Air Quality Monitoring

**London Air Quality Network (LAQN)**

- Status: Complete (4,932 validated files)
- Coverage: 78 sites, 170 validated combinations
- Period: January 2023 to November 2025 (35 months)
- Pollutants: NO₂ (58 combinations), PM2.5 (53), PM10 (42), O₃ (11), SO₂ (4), CO (2)
- Quality: 17.2% remaining operational gaps, 100% temporal consistency
- API: https://api.erg.ic.ac.uk/AirQuality

**DEFRA UK-AIR Network**

- Status: Data collected, preparation in progress
- Coverage: London bounding box subset
- Period: January 2023 to November 2025
- Quality: Preliminary assessment shows minimal missing data
- Pollutants: NO₂, PM2.5, PM10, O₃, SO₂, CO, NO
- API: https://uk-air.defra.gov.uk/sos-ukair/api/v1

### Supporting Meteorological Data

**Open-Meteo API**

- Status: Complete (monthly files 2023-2025)
- Variables: Temperature (2m), wind speed (10m, 100m), wind direction, humidity, pressure, precipitation, cloud cover
- Temporal resolution: Hourly
- Geographic coverage: Greater London metropolitan area
- API: https://api.open-meteo.com/v1

**Transport for London (TfL) API**

- Status: Planned for advanced modelling phase
- Data types: Traffic flow, congestion levels, public transport usage
- Integration: Under consideration based on initial model performance

## Technical Setup

### Requirements

Python 3.8 or higher with core dependencies:

```
pandas>=2.0.0
numpy>=1.25.0
scikit-learn>=1.2.0
matplotlib>=3.6.0
seaborn>=0.12.0
plotly>=5.15.0
requests>=2.28.0
geopandas>=0.12.0
folium>=0.14.0
statsmodels>=0.13.0
openmeteo-requests
requests-cache
retry-requests
```

### Installation

bash

```bash
git clone https://github.com/yourusername/air-pollution-levels.git
cd air-pollution-levels

python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

### Configuration

Edit `config.py` for project parameters :

This part will be updated once I start training.

```python
# Air quality settings
POLLUTANTS = ['PM2.5', 'PM10', 'O₃', 'NO₂', 'SO₂', 'CO' ]
START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2025, 11, 19)
LONDON_BBOX = [-0.5, 51.3, 0.3, 51.7]  # [minLon, minLat, maxLon, maxLat]

# Modelling settings
TRAIN_SPLIT = 0.7      # 2023-2024 training
VAL_SPLIT = 0.15       # 2025 Jan-Aug validation
TEST_SPLIT = 0.15      # 2025 Sep-Nov test
MISSING_THRESHOLD = 0.20  # File quality threshold
```

## Methodology

### Data Preparation 

**Three-Stage Cleaning Process:**

1. Metadata Validation: API cross-referencing, equipment existence verification.
2. Temporal Analysis: 35-month consistency checks, year-specific failure identification.
3. ML Optimisation: Cross-year consistency enforcement, benefit ratio analysis.

**Quality Metrics:**

- Baseline: 47.5% issue rate
- Final: 17.2% issue rate
- Improvement: 63.8% relative reduction
- Temporal consistency: 100%

### Feature Engineering (Planned)

**Temporal Features:**

- Hour of day, day of week, month, season.
- Weekend and holiday indicators.
- Rush hour classifications.

**Meteorological Features:**

- Temperature (2m height).
- Wind speed (10m, 100m) and direction.
- Humidity, atmospheric pressure, precipitation.
- Cloud cover.

**Spatial Features:**

- Site type (Roadside, Urban Background, Suburban, Kerbside, Industrial)
- Latitude, longitude, borough
- Distance to major roads

**Lag Features:**

- Previous hour and day pollution levels.
- Rolling averages (3-hour, 24-hour, 7-day windows).
- Year-over-year comparisons.

### Modelling Approach (Planned)

**Traditional Machine Learning: Random Forest**

- Handles missing data robustly (17.2% operational gaps)
- Provides feature importance for interpretability
- Captures non-linear relationships
- Computationally efficient for 170 site-pollutant combinations

**Neural Network: CNN**

- Time-series temporal pattern learning
- Long-term dependency capture
- Proven effectiveness in air quality literature
- Sequential prediction capability

**Evaluation Framework:**

- Temporal train/validation/test split
- Metrics: RMSE, MAE, R²
- Error analysis by pollutant, site type, and temporal period
- Feature importance visualisation

## Current Progress

### Completed

- LAQN data collection (8,709 files)
- LAQN quality assessment and cleaning (to 4,932 validated files)
- Weather data collection (2023-2025)
- DEFRA data collection (2023-2025)
- Comprehensive data preparation documentation
- Complete audit trail and reproducibility logs
- Data inventory system implementation

### In Progress

- DEFRA data quality assessment
- Exploratory data analysis
- Feature engineering design
- Spatial coverage analysis
- Temporal pattern analysis

### Planned

**Modelling Phase:**

- Random Forest baseline implementation
- CNN network development
- Model comparison and selection
- Ensemble methods exploration
- Separate LAQN vs DEFRA model evaluation

**Analysis Phase:**

- Feature importance analysis
- Error analysis by pollutant, site, time
- Spatial prediction mapping
- Temporal forecast validation

**Documentation:**

- Model training documentation
- Results interpretation
- MSc dissertation writing

## Data Quality and Limitations

### LAQN Dataset Characteristics

**Strengths:**

- High spatial density (78 sites across Greater London)
- Long temporal coverage (35 months continuous)
- 100% cross-year consistency for all validated combinations
- Strong NO₂ and PM2.5 representation (65.3% of combinations)
- Complete audit trail ensuring reproducibility

**Limitations:**

- 17.2% operational gaps (normal for environmental monitoring)
- Roadside site bias (54.3% of combinations)
- 32.5% reduction in combinations from initial collection
- Small negative values present in 0.49% of measurements

**Remaining Issues (Normal Operational Variance):**

- Temporary sensor failures: 6-10%
- Scheduled maintenance: 8-12%
- Data transmission problems: 3-5%
- Calibration periods: 2-4%
- Environmental impacts: 1-3%

### Recommended Imputation Strategy

For the remaining 17.2% gaps:

- Short gaps (6 hours or less): Linear interpolation
- Medium gaps (6-24 hours): K-nearest neighbours (k=5, temporal similarity)
- Long gaps (24 hours or more): Missingness indicators in model features

## Geographic Coverage

**Monitoring Network:**

- 78 validated sites (92.9% retention from initial 84)
- All London boroughs represented.
- Higher density in Central and Inner London.
- Good coverage in Outer London boroughs.

**Site Type Distribution:**

| Site Type        | Combinations | Percentage | Use Case                   |
| ---------------- | ------------ | ---------- | -------------------------- |
| Roadside         | 94           | 54.3%      | Traffic pollution exposure |
| Urban Background | 36           | 20.8%      | General urban air quality  |
| Suburban         | 19           | 11.0%      | Residential area exposure  |
| Kerbside         | 18           | 10.4%      | Pedestrian exposure        |
| Industrial       | 6            | 3.5%       | Industrial impact          |

## Reproducibility

### Complete Documentation

All cleaning decisions documented with:

- Quantitative rationale (benefit ratios, issue rates).
- Comprehensive audit logs (12+ quality assessment logs).
- Reversible operations (files preserved, metadata corrected).
- Transparent trade-off analysis.
- Statistical validation approach.

### File Organisation

**Production Files (Use These):**

- `data/laqn/optimased/` — 4,932 validated measurement files
- `data/laqn/optimased_siteSpecies.csv` — 170 validated combinations metadata
- `data/defra/test/london_stations_clean.csv` — DEFRA station metadata

**Documentation Files (Audit Trail):**

- `data/laqn/missing/logs_*.csv` — Complete quality assessment logs
- `data/laqn/missing/removal_quality_report/` — Cross-year analysis
- `data/laqn/missing/notActive_*.csv` — Equipment failure identification

**Deprecated Files (Do Not Use):**

- `data/laqn/actv_sites_species.csv` — Original metadata (contains 38 non-existent combinations)

### Analysis Notebooks

1. `laqn_exploration.ipynb` — Initial dataset discovery
2. `laqn_check.ipynb` — Quality assessment implementation
3. `laqn_update.ipynb` — Complete cleaning process execution
4. `laqn_remove.ipynb` — File removal implementation
5. `defra_check.ipynb` — DEFRA quality validation
6. `cross_check_DEFRA_LAQN.ipynb` — Dataset comparison analysis

## Research Objectives

### Primary Goals

1. Develop accurate PM2.5, PM10, O₃, NO₂, SO₂, CO  prediction models using CNN, RF, SVM,
2. Identify key drivers of air pollution variation (weather, traffic, temporal patterns)
3. Evaluate LAQN versus DEFRA datasets for model performance and data quality.
4. Provide interpretable models suitable for policy planning.

### Research Questions

- Can traditional machine learning (Random Forest) match neurological networks (CNN) for hourly pollution forecasting?
- How do weather conditions influence prediction accuracy?
- Does data quality (LAQN 17.2% versus DEFRA minimal issue rate) significantly affect model performance?
- Which features are most important for NO₂ versus PM2.5 prediction?
- Can models trained on LAQN generalise to DEFRA locations (and vice versa)?

## Expected Outcomes

1. Two validated prediction models (Random Forest and CNN) for PM2.5, PM10, O₃, NO₂, SO₂, CO 
2. Comprehensive comparison of LAQN versus DEFRA data quality and modelling performance.
3. Feature importance analysis identifying key pollution drivers.
4. Spatial prediction maps showing pollution patterns across London.
5. Open-source dataset with complete preparation documentation.
6. MSc dissertation contributing to environmental data science methodology.



## Appendix: Key Decisions

### Why 17.2% Issue Rate is Acceptable

The final 17.2% represents normal operational variance in environmental monitoring:

- Meets European Environment Agency standards (below 20% threshold)
- Slightly exceeds WHO ideal (below 10%) but acceptable for machine learning
- All issues are temporary or operational, not systematic equipment failures
- Comparable to other academic air quality datasets

### Why Cross-Year Consistency Mattered

Removing 1,247 additional files (20.2% of dataset) was justified because:

- Benefit ratio: 1.54:1 (removed more problematic data than good data).
- Machine learning requirement: Time-series models need consistent temporal coverage.
- Feature engineering: Year-over-year comparisons require all years present.
- Cross-validation: Temporal splits require consistent coverage across folds.

### Why Separate LAQN versus DEFRA Models

Different characteristics suggest separate initial modelling:

- Data quality: LAQN 17.2% versus DEFRA minimal issue rate.
- Spatial density: LAQN higher density versus DEFRA broader coverage.
- Site bias: LAQN 54.3% Roadside versus DEFRA more balanced distribution.
- Interpretability: Easier to explain separate model performance differences.

Final decision on combining datasets will be made after initial model comparison.