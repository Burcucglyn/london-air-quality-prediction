# LAQN Air Quality Data Analysis Report

## Executive Summary

This report documents the collection, quality assessment, and validation of air pollution measurements from the London Air Quality Network (LAQN) monitoring infrastructure across Greater London. The analysis covered January 2023 through November 2025 (35 months), with overall 3,446,208 hourly measurements from 78 monitoring stations tracking 6 different pollutants.

| Metric                                                   | LAQN Dataset | Percentage/Explanation                                       |
| -------------------------------------------------------- | ------------ | ------------------------------------------------------------ |
| Total number of files                                    | 4,932        |                                                              |
| Total number of each hourly measurement across all files | 3,446,208    | 87.13% measurement value record completeness in LAQN dataset. |
| Total missing value measurements across all files        | 443,658      | 12.87% missing value measurements.                           |
| Number of monitoring stations/sites in London            | 78           |                                                              |
| Number of collected station/pollutant combinations       | 141          |                                                              |
| Number of pollutants measured                            | 6            | NO₂, PM10, PM2.5, O₃, SO₂, CO                                |
| Total number of measurement files 2023                   | 1,689        | Files from 2023 represent 34.25% of the dataset.             |
| Total number of each hourly measurement for 2023         | 1,192,464    | 86.98% of 2023 values are complete.                          |
| Number of missing value measurements in 2023             | 155,312      | 13.02% of 2023 values are missing.                           |
| Total number of measurement files 2024                   | 1,692        | Files from 2024 represent 34.31% of the dataset.             |
| Total number of each hourly measurement for 2024         | 1,197,936    | 88.12% of 2024 values are complete.                          |
| Number of missing value measurements in 2024             | 142,335      | 11.88% of 2024 values are missing.                           |
| Total number of measurement files 2025                   | 1,551        | Files from 2025 represent 31.45% of the dataset.             |
| Total number of each hourly measurement for 2025         | 1,055,808    | 86.17% of 2025 values are complete.                          |
| Number of missing value measurements in 2025             | 146,011      | 13.83% value measurements missing in 2025.                   |

(data/laqn/report/laqn_stats.csv file)

LAQN dataset showed 12.87% missing values after the cleaning period. Missing data patterns varied by pollutant, with O3 and PM2.5 showing higher gaps compared to NO2 and CO measurements.

## 1. Dataset Overview

### 1.1 Collection Scope

The LAQN dataset was systematically collected through to `https://api.erg.ic.ac.uk/AirQuality/help` documentation link. Nitrogen dioxide receives the most extensive coverage, given its direct link to vehicle exhaust and its role as a key indicator for urban air quality management.

**Primary regulatory pollutants:** NO₂, PM10, PM2.5, O₃, SO₂, CO (6 pollutants)

| Pollutant | Count | Percentage | Site Names                                                   |
| --------- | ----- | ---------- | ------------------------------------------------------------ |
| NO₂       | 60    | 34.68%     | Barking and Dagenham - Rush Green, Barking and Dagenham - Scrattons Farm, Bexley - Belvedere, Bexley - Belvedere West, Bexley - Slade Green, Brent - ARK Franklin Primary Academy, Brent - Ikea, Brent - John Keble Primary School, Brent - Neasden Lane, Bromley - Harwood Avenue, Camden - Swiss Cottage, Croydon - Norbury, Croydon - Purley Way A23, Ealing - Hanger Lane Gyratory, Ealing - Horn Lane, Ealing - Western Avenue, Enfield - Bowes Primary School, Enfield - Bush Hill Park, Enfield - Derby Road, Enfield - Prince of Wales School, Greenwich - A206 Burrage Grove, Greenwich - Blackheath, Greenwich - Plumstead High Street, Greenwich - Trafalgar Road (Hoskins St), Greenwich - Tunnel Avenue, Greenwich - Westhorne Avenue, Greenwich - Woolwich Flyover, Haringey - Priory Park South, Haringey - Haringey Town Hall, Havering - Rainham, Havering - Romford, Islington - Arsenal, Islington - Holloway Road, Kensington and Chelsea - North Ken, Lambeth - Brixton Road, Lambeth - Streatham Green, Lewisham - Honor Oak Park, Newham - Britannia Gate, Newham - Hoola Tower, Regent Street (The Crown Estate), Richmond Upon Thames - Barnes Wetlands, Richmond Upon Thames - Castelnau, Southwark - A2 Old Kent Road, Tower Hamlets - Blackwall, Tower Hamlets - Jubilee Park, Tower Hamlets - Mile End Road, Wandsworth - Battersea, Wandsworth - Putney High Street, Wandsworth - Tooting High Street, Waterloo Place (The Crown Estate), Westminster - Covent Garden, Westminster - Elizabeth Bridge, Westminster - Marylebone Road, Westminster - Oxford Street |
| PM2.5     | 53    | 30.64%     | Bexley - Belvedere, Bexley - Belvedere West, Bexley - Slade Green Fidas, Brent - ARK Franklin Primary Academy, Brent - Ikea, Brent - John Keble Primary School, Brent - Neasden Lane, Bromley - Harwood Avenue, Camden - Bloomsbury, Camden - Swiss Cottage, Croydon - Norbury Manor, Ealing - Horn Lane TEOM, Enfield - Bowes Primary School, Greenwich - A206 Burrage Grove, Greenwich - Blackheath, Greenwich - Eltham, Greenwich - Falconwood FDMS, Greenwich - John Harrison Way, Greenwich - Plumstead High Street, Greenwich - Westhorne Avenue, Greenwich - Woolwich Flyover, Hackney - Old Street, Haringey - Haringey Town Hall, Havering - Rainham, Havering - Romford, Hillingdon - Harlington, Islington - Arsenal, Islington - Holloway Road, Kensington and Chelsea - North Ken, Kensington and Chelsea - Station Walk, Lambeth - Brixton Road, Lambeth - Streatham Green, Lavender Hill, Lewisham - Honor Oak Park, London Teddington Bushy Park , Merton - Merton Road, Merton - Mitcham, Merton - Plough Lane Wimbledon, Newham - Britannia Gate, Regent Street (The Crown Estate), Richmond Upon Thames - Barnes Wetlands, Richmond Upon Thames - Richmond, Southwark - A2 Old Kent Road, Tower Hamlets - Blackwall, Tower Hamlets - Jubilee Park, Tower Hamlets - King Edward Memorial Park, Tower Hamlets - Mile End Road, Tower Hamlets - Victoria Park, Wandsworth - Battersea, Wandsworth - Putney, Wandsworth - Putney High Street, Wandsworth - Tooting High Street, Waterloo Place (The Crown Estate), Westminster - Covent Garden, Westminster - Elizabeth Bridge, Westminster - Horseferry Road, Westminster - Oxford Street, Westminster - Queens Park Gardens |
| PM10      | 43    | 24.86%     | Barking and Dagenham - Scrattons Farm, Bexley - Belvedere, Bexley - Belvedere West, Bexley - Slade Green, Brent - ARK Franklin Primary Academy, Brent - Ikea, Brent - John Keble Primary School, Brent - Neasden Lane, Bromley - Harwood Avenue, Camden - Swiss Cottage, Ealing - Hanger Lane Gyratory, Ealing - Horn Lane, Ealing - Horn Lane TEOM, Ealing - Western Avenue, Greenwich - A206 Burrage Grove, Greenwich - Blackheath, Greenwich - Falconwood, Greenwich - Fiveways Sidcup Rd A20, Greenwich - John Harrison Way, Greenwich - Plumstead High Street, Greenwich - Trafalgar Road (Hoskins St), Greenwich - Westhorne Avenue, Greenwich - Woolwich Flyover, Haringey - Haringey Town Hall, Havering - Romford, Islington - Arsenal, Islington - Holloway Road, Lambeth - Brixton Road, Lambeth - Streatham Green, Lavender Hill, Lewisham - Honor Oak Park, Newham - Britannia Gate, Regent Street (The Crown Estate), Richmond Upon Thames - Barnes Wetlands, Richmond Upon Thames - Castelnau, Southwark - A2 Old Kent Road, Tower Hamlets - Blackwall, Tower Hamlets - Jubilee Park, Wandsworth - Battersea, Wandsworth - Putney, Wandsworth - Putney High Street, Wandsworth - Tooting High Street, Waterloo Place (The Crown Estate), Westminster - Oxford Street |
| O₃        | 11    | 6.36%      | Bexley - Belvedere West, Bexley - Slade Green, Greenwich - Falconwood, Greenwich - Plumstead High Street, Haringey - Priory Park South, Kensington and Chelsea - North Ken, Lewisham - Honor Oak Park, Regent Street (The Crown Estate), Richmond Upon Thames - Barnes Wetlands, Tower Hamlets - Blackwall, Waterloo Place (The Crown Estate), Westminster - Marylebone Road |
| SO₂       | 4     | 2.31%      | Barking and Dagenham - Rush Green, Bexley - Slade Green, Kensington and Chelsea - North Ken, Westminster - Marylebone Road |
| CO        | 2     | 1.16%      | Kensington and Chelsea - North Ken, Westminster - Marylebone Road |

(data/laqn/report/pollutant_distribution.csv file merged with metadata /data/laqn/optimased_siteSpecies.csv)

### 1.2 File Organisation

The collected data maintained consistent monthly organisation across the three-year period:

```bash
data/laqn/
├── actv_sites_species.csv
├── missing/
│ ├── affected_sites_species_counts.csv
│ ├── ***
│ └── removal_quality_report/  		#last removal quality logs
├── monthly_data/									# raw fetched data folder.
│ └── [2023_apr/, 2023_aug/, ..., 2025_sep/]
├── optimased/                              # Optimased validated measurements folder, will be use this folder's files for ML.
│   ├── 2023_jan/                           # Monthly folders.
│   ├── 2023_feb/
│   ├── ...
│   └── 2025_nov/
│       └── {SiteCode}_{SpeciesCode}_{StartDate}_{EndDate}.csv #structure of the optimased data
├── processed/
│ └── [2023_apr/, 2023_aug/, ..., 2025_sep/] 		# First round of processed files.
├── optimased_siteSpecies.csv		#Cleaned site/species metadata
│
├── report/                                 # Quality metrics, statistical analysis reports
│ 	├── detailed_analysis/	# output of seasonal analyse at laqn_analyse- last func.			
│   │   ├── seasonal_averages.csv           # Seasonaly pollutant patterns 
│   │   ├── yearly_averages.csv		# Annual trends
│   │		└─── distrubition_of_each_pollutants.png
│		│						└─── Visulation of daily avg/distrubition/hourly avg/monthly distrubition
│		│
│   ├── laqn_stats.csv                      # Dataset summary, record.
│   ├── quality_metrics.csv                 # Detailed data quality metrics.
│   ├── seasonal_averages.csv               # Seasonal pollutant patterns.
│   ├── yearly_averages.csv                 # Annual trends.
│   ├── chi_square_tests.csv                # Year-wise distribution validation.
│   ├── limit_exceedances.csv               # UK regulatory compliance.
│   ├── nan_values_by_pollutant.csv         # Pollutant-level missing data.
│   ├── nan_values_by_station_pollutant.csv # Station-pollutant combinations.
│   ├── pollutant_distribution.csv          # 6 pollutant distribution according to sites.
│   └── laqn_negative_value_summary.csv     # Sensor error documentation.
│
├─ optimased_sitesSpecies.csv 
│
data/defra
│
├── capabilities/                           #API endpoints capabilities documentation
	   └── uk_pollutant_limits.csv             #UK legal pollutant limits documentation csv.
```

**File structure:** Each CSV file contains 

`@MeasurementDateGMT, @Value, @SiteCode, and @SpeciesCode `columns.

**Naming convention:** `{SiteCode}_{SpeciesCode}_{YYYY-MM-DD}_{YYYY-MM-DD}.csv` within monthly subdirectories.

The stable file counts across years (1,689 in 2023, 1,692 in 2024, 1,551 in 2025) reflected consistent network operation. The 2025 reduction represents the partial-year dataset (January through November) rather than equipment failures, a distinction confirmed through temporal analysis.

### 1.3 Metadata Validation

The LAQN collection process began by parsing data/laqn/actv_sites_species.csv, which contained metadata for all active station-pollutant combinations identified through the API. Updated metadata used for this analysis `optimased_siteSpecies.csv`.

Later on first data analysis process realised that, metadata species/site pairs were not correct, and almost half of them removed with validation. `laqn_check.ipynb` file, `laqn_exploration.ipynb` file, `laqn_remove.ipynb`, and `laqn_update.ipynb` file represents how they removed and what what the underlaying reasoning. For data cleaning process `/docs/LAQN_data_quality_cleaning.md` file explains why, how.

**Metadata contents:**

**Station identification:** SiteCode, SiteName, SiteType, geographic coordinates (Latitude, Longitude)

**Pollutant information:** SpeciesCode, SpeciesName

**Expected combinations:**  unique station-pollutant pairs

The year coverage analysis confirmed stable network composition throughout the study period, with 141 site-species combinations maintained consistently across 2023, 2024, and 2025 with no lost or new combinations.

## 2. UK Air Quality Standards Framework

### 2.1 Regulatory Context

The UK Air Quality Standards Regulations 2010 (SI 2010/1001) implement EU air quality directives and establish legally binding limits for pollutant concentrations. These standards define thresholds above which air quality is considered harmful to human health and the environment.

### 2.2 Legal Limits Summary

The UK Air Quality Standards pollutant threshold data used for validation:

| Pollutant | Limit     | Averaging Period          | Permitted Exceedances |
| --------- | --------- | ------------------------- | --------------------- |
| NO₂       | 40 µg/m³  | Annual mean               | None                  |
| NO₂       | 200 µg/m³ | 1-hour mean               | 18 per year           |
| PM10      | 40 µg/m³  | Annual mean               | None                  |
| PM10      | 50 µg/m³  | 24-hour mean              | 35 per year           |
| PM2.5     | 20 µg/m³  | Annual mean               | None                  |
| O₃        | 100 µg/m³ | 8-hour running mean       | 10 per year           |
| SO₂       | 125 µg/m³ | 24-hour mean              | 3 per year            |
| SO₂       | 350 µg/m³ | 1-hour mean               | 24 per year           |
| CO        | 10 mg/m³  | Maximum daily 8-hour mean | None                  |

(National Air Quality Objectives - UK-air, 15.12.2025)

#### UK Air Quality Objectives Averaging Period Calculations:

**Annual mean limits** (NO₂, PM10, PM2.5) calculated yearly means then averaged across all available years. For a measurement to be valid, the year needed at least 75% data capture (273 days).

**24-hour mean limits** (PM10, SO₂) took daily means calculated from hourly values, then counted exceedances per calendar year. Compliance meant staying under the permitted exceedance limit.

**8-hour running mean** (O₃, CO) used a continuous rolling 8-hour average updated hourly. Each hour's mean comprised that hour plus the previous 7 hours, with exceedances counted per year.

**1-hour mean limits** (NO₂, SO₂) compared hourly values directly against thresholds and counted how many hours per year exceeded the limit.

## 3. Data Quality Validation

### 3.1 Quality Assessment Methodology

The quality metrics validation function checks uk_pollutant_limits against LAQN measurements for available pollutants matching threshold limitations. The function calculates average period detection.

- Loads all measurement files for the years 2023, 2024, and 2025.
- Reads the official UK pollutant limits from a CSV file.
- For each pollutant, it checks:
  - If any values are negative (which is not possible in reality).
  - If any values are extremely high (likely sensor errors).
  - If the measurements exceed the UK legal limits (for different averaging periods, like annual mean or 24-hour mean).

quality_metrics.csv each csv file followed this format:

```bash
pollutant,total_measurements,mean_hourly,min,max,p95,negative_values,zero_values,out_of_range,uk_annual_limit,mean_annual,exceeds_annual,uk_24hour_limit,daily_exceedances,o3_exceedance_days,co_max_daily_8h_mean
```

- It calculates basic statistics (mean, median, standard deviation, min, max, percentiles) for each pollutant.
- It reports how many measurements are negative, zero, or out of range.
- It checks if the annual or daily averages exceed the UK limits.
- As output creates a report quality_metrics.csv

##### Quality Metric Result Table for LAQN

| Metric                      | NO2       | PM2.5   | PM10    | SO2    | O3      | CO     |
| --------------------------- | --------- | ------- | ------- | ------ | ------- | ------ |
| Total measurements          | 1,267,018 | 482,559 | 896,146 | 71,217 | 220,912 | 43,565 |
| Hourly Mean                 | 23.34     | 9.25    | 17.23   | 1.47   | 47.71   | 0.20   |
| Minimum Value Recorded      | 0.00      | 0.00    | 0.00    | 0.00   | 0.00    | 0.00   |
| Maximum Value Recorded      | 376.30    | 909.00  | 759.00  | 271.40 | 198.60  | 4.90   |
| 95th Percentile value       | 57.10     | 23.90   | 39.00   | 4.20   | 85.60   | 0.50   |
| Negative Values             | 0         | 0       | 0       | 0      | 0       | 0      |
| Number of Zero Measurements | 632       | 2,090   | 835     | 2,348  | 260     | 6,773  |
| Possible Sensor Errors      | 0         | 11      | 3       | 0      | 0       | 0      |
| UK Legal Limit Annual mean  | 40.0      | 20.0    | 40.0    | —      | —       | —      |
| Annual Mean                 | 23.30     | 9.29    | 17.32   | —      | —       | —      |
| Annual Mean Exceeds         | no        | no      | no      | —      | —       | —      |
| UK Legal 24 Hour Limit      | —         | —       | 50.0    | 125.0  | —       | —      |
| Daily Exceedances           | —         | —       | 3       | 0      | —       | —      |
| O3 Exceedance Days          | —         | —       | —       | —      | 70      | —      |
| CO Max Daily 8h Mean        | —         | —       | —       | —      | —       | 2.14   |

(data/laqn/report/quality_metrics.csv file)

### Explanation of Output Headers

- **mean_hourly**: Average value of all hourly measurements.
- **min**: Minimum value recorded.
- **max**: Maximum value recorded.
- **p95**: 95th percentile value (value below which 95% of data falls). It helps understand the upper range of typical measurements, filtering out the most extreme 5% of values, which might be outliers or rare events. It gives a sense of the normal high values at LAQN data, without being skewed by rare spikes or errors.
- **negative_values**: Number of negative measurements (should be zero in good data).
- **zero_values**: Number of zero measurements.
- **out_of_range**: Number of values that are extremely high likely sensor errors.
- **uk_annual_limit**: The UK legal limit for the annual mean.
- **mean_annual**: The actual annual mean calculated from the data.
- **exceeds_annual**: Whether the annual mean exceeds the UK limit (yes/no).
- **uk_24hour_limit**: The UK legal limit for the 24-hour mean (if defined).
- **daily_exceedances**: Number of days where the daily mean exceeded the UK 24-hour limit.

### 3.2 Missing Data Assessment

| Pollutant | Total Records | Missing | Percentage Missing |
| --------- | ------------- | ------- | ------------------ |
| O3        | 268,320       | 47,056  | 17.54%             |
| PM2.5     | 586,944       | 100,755 | 17.17%             |
| SO2       | 97,824        | 15,803  | 16.15%             |
| PM10      | 1,026,456     | 126,749 | 12.35%             |
| NO2       | 1,417,752     | 148,803 | 10.50%             |
| CO        | 48,912        | 4,492   | 9.18%              |

(data/laqn/report/nan_values_by_pollutant.csv file)

Missing data percentages range from 9.18% (CO) to 17.54% (O3). The higher gaps in O3 and PM2.5 records reflect the technical complexity of these measurements and the smaller number of monitoring sites.

### 3.3 Data Anomalies

The dataset contains 1,377 documented instances of negative values across various site-pollutant combinations in the optimased folde. Negative values occur most frequently in PM10 and SO2 readings.

Such anomalies are flagged and documented in `laqn_negative_value_summary.csv`. Downstream analysis should apply appropriate filtering or imputation depending on the specific use case. Ended up changing all of the negative values to NaN.

## 4. Chi-Square Test for Data Uniformity

To verify the consistency of the LAQN data collection throughout the year, a chi-square test used. This test compares the number of files collected each month to what would be expected if the data were evenly spread out.

For this dataset, the chi-square statistic was 0.0035 and the p-value was 0.9983. This p-value is much greater than 0.05, which means the data are evenly distributed across the months. In other words, the files are spread consistently throughout the collection period.



| Year | Observed Files | Expected Files |
| ---- | -------------- | -------------- |
| 2023 | 1,689          | 1,691.0        |
| 2024 | 1,692          | 1,691.0        |
| 2025 | 1,551          | 1,550.1        |

(data/laqn/report/chi_square_tests.csv file)

This result confirms that data collection remained consistent across the study period without systematic gaps or biases. The extremely high p-value (0.9983) indicates file counts match expected values almost exactly.

In summary, the chi-square test shows that the data are evenly distributed over the year, providing confidence in the temporal reliability of the dataset for trend analysis and seasonal comparisons(M. Sridhar Reddy (2023) “Chi-square Test and Its Utility in Forest Ecology Studies”).

## 5. Seasonal Trend Analysis

### 5.1 Data Overview

#### Pollutant Coverage

Quality metrics collected under the folder `data/laqn/report/quality_metrics.csv`The dataset includes high measurement counts for key pollutants:

- **Nitrogen dioxide (NO₂):** 1,267,018 measurements
- **PM10:** 896,146 measurements
- **PM2.5:** 482,559 measurements
- **Ozone (O₃):** 220,912 measurements
- **Sulphur dioxide (SO₂):** 71,217 measurements
- **Carbon monoxide (CO):** 43,565 measurements

### 5.2 Yearly and Seasonal Trends

#### Yearly Trends

Yearly averages were calculated for each pollutant, revealing how concentrations changed over the three-year period. For example:

- **NO₂:** Mean values decreased from 24.92 µg/m³ in 2023 to 22.19 µg/m³ in 2025.
- **Ozone:** Mean values increased from 46.28 µg/m³ in 2023 to 49.73 µg/m³ in 2025.
- **PM2.5:** Mean values fluctuated, with 8.81 µg/m³ in 2023, 8.42 µg/m³ in 2024, and 10.63 µg/m³ in 2025.

##### Seasonal Variation in Air Pollutant Concentrations

The file seasonal_averages.csv summarises how the average concentrations of various air pollutants change throughout the year. For each pollutant, the mean value is calculated separately for Winter, Spring, Summer, and Autumn.

| Pollutant                         | Winter | Spring | Summer | Autumn |
| --------------------------------- | ------ | ------ | ------ | ------ |
| Carbon monoxide (CO)              | 0.28   | 0.16   | 0.15   | 0.23   |
| Nitrogen dioxide (NO₂)            | 28.14  | 23.01  | 18.25  | 24.69  |
| Ozone (O₃)                        | 39.20  | 57.33  | 53.14  | 39.80  |
| Particulate matter <10µm (PM10)   | 17.10  | 18.74  | 16.13  | 16.91  |
| Particulate matter <2.5µm (PM2.5) | 10.09  | 10.58  | 7.46   | 8.90   |
| Sulphur dioxide (SO₂)             | 1.63   | 1.52   | 1.41   | 1.34   |

(data/laqn/report/seasonal_averages.csv file)

- All values are mean concentrations for the given season and pollutant.
- Units are µg/m³ for most pollutants, mg/m³ for CO.

This seasonal breakdown allows us to identify patterns such as:

- **Ozone (O₃):** levels are highest in spring (57.33) and summer (53.14), and lowest in winter (39.20) and autumn (39.80). This reflects increased sunlight and photochemical activity in warmer months.
- **Nitrogen dioxide (NO₂):** NO₂ is highest in winter (28.14) and autumn (24.69), and lowest in summer (18.25). This likely results from increased emissions from heating and less atmospheric dispersion in colder months.
- **Particulate matter (PM10 and PM2.5):** PM2.5 concentrations are generally higher in winter (10.09) and spring (10.58), and lower in summer (7.46). PM10 peaks in spring (18.74). This may be due to increased combustion and stagnant air during colder seasons.
- **Carbon monoxide (CO):** CO is highest in winter (0.28) and lowest in summer (0.15), consistent with increased heating and reduced atmospheric mixing in winter.
- **Sulphur dioxide (SO₂):** SO₂ is highest in winter (1.63) and decreases through the year to autumn (1.34), reflecting reduced heating demand.

Most pollutants are higher in winter and autumn, reflecting increased emissions and less atmospheric mixing. Ozone is the exception, peaking in spring and summer due to photochemical processes. These seasonal patterns are important for understanding when and why air quality issues are most severe, and for designing effective pollution control strategies.

### 5.3 Annual Summary of Pollutants

The file yearly_averages.csv contains the annual summary statistics for each pollutant in the dataset, broken down by year.

### What does it explain?

- **Annual Trends:** By comparing the mean and median values across years for each pollutant, to see if pollution levels are rising, falling, or staying the same.
- **Data Completeness:** The count column shows how much data was collected for each pollutant each year, which helps assess data coverage and reliability.

| Pollutant              | 2023  | 2024  | 2025  |
| ---------------------- | ----- | ----- | ----- |
| Nitrogen dioxide (NO₂) | 24.92 | 22.78 | 22.19 |
| Ozone (O₃)             | 46.28 | 47.38 | 49.73 |
| PM10                   | 16.69 | 16.32 | 18.94 |
| PM2.5                  | 8.81  | 8.42  | 10.63 |
| Sulphur dioxide (SO₂)  | 1.21  | 1.17  | 2.18  |
| Carbon monoxide (CO)   | 0.24  | 0.16  | 0.20  |

(data/laqn/report/yearly_averages.csv file)

- NO₂ levels have gradually decreased over the three years, suggesting improvements in air quality from emission controls and ULEZ expansion.
- Ozone (O₃) levels increased steadily from 2023 to 2025, inversely related to NO₂ reductions.
- PM10 and PM2.5 concentrations were lowest in 2024, but increased in 2025.
- SO₂ levels remained low in 2023 and 2024, with higher variability in 2025.
- Carbon monoxide (CO) showed a decrease in 2024, with a slight recovery in 2025, remaining at low concentrations throughout.

Overall, the table provides a clear year-by-year view of air quality trends for the most important pollutants, helping to identify improvements, emerging issues, and areas needing further attention.

### 5.4 UK Air Policy Check

The limit_exceedances.csv table provides a direct assessment of how well the air quality in the dataset complies with official UK air quality standards for key pollutants. Its main purpose is to summarise, transparently and quantitatively, how often pollutant concentrations exceeded the legal limits set to protect public health.

- **Regulatory Compliance:** The table allows for a straightforward check of whether the air pollution levels recorded in the dataset meet or breach the UK's legal requirements for each pollutant.
- **Risk Identification:** By showing the number and percentage of exceedances for each pollutant, the table highlights which pollutants and time periods are most problematic.
- **Transparency and Accountability:** Including this table in the report demonstrates a rigorous, evidence-based approach. It provides clear documentation of where and how often air quality standards are not met.

| Pollutant                       | Code | Objective / Limit Description               | Averaging Period | Limit Value | Unit  | Total Measurements | Exceedances | % Exceedance |
| ------------------------------- | ---- | ------------------------------------------- | ---------------- | ----------- | ----- | ------------------ | ----------- | ------------ |
| Nitrogen dioxide                | NO2  | 40 µg/m³                                    | annual mean      | 40.0        | µg/m³ | 1,267,018          | 194,871     | 15.38        |
| Particulate matter <10µm (PM10) | PM10 | 50 µg/m³ not to be                          | 24 hour mean     | 50.0        | µg/m³ | 896,146            | 18,787      | 2.10         |
| Particulate matter <10µm (PM10) | PM10 | 40 µg/m³                                    | annual mean      | 40.0        | µg/m³ | 896,146            | 40,685      | 4.54         |
| Ozone                           | O3   | 100 µg/m³ not to be exceeded >10 times/year | 8 hour mean      | 100.0       | µg/m³ | 220,912            | 3,677       | 1.66         |
| Sulphur dioxide                 | SO2  | 125 µg/m³ not to be                         | 24 hour mean     | 125.0       | µg/m³ | 71,217             | 14          | 0.02         |
| Carbon monoxide                 | CO   | 10 mg/m³                                    | maximum daily    | 10.0        | mg/m³ | 43,565             | 0           | 0.00         |

(data/laqn/report/limit_exceedances.csv file)

This table summarises the compliance of the measured air pollution data with the uk_pollutant_limits.csv file limits. For each pollutant, the table lists the legal limit (objective), the averaging period over which the limit applies, the total number of measurements, the number of times the limit was exceeded, and the percentage of exceedances.

- If the percentage of exceedances is low or zero, it means the pollutant levels at dataset are generally within the UK legal limits, indicating compliance.
- If the percentage is high, it means the pollutant frequently exceeded the legal limit, suggesting non-compliance and potential air quality concerns.

High exceedance rates highlight pollutants and periods where air quality improvements may be needed.

## Citations:

M. Sridhar Reddy (2023) “Chi-square Test and Its Utility in Forest Ecology Studies”, *Journal of Global Ecology and Environment*, 17(1), pp. 1–5. doi: 10.56557/jogee/2023/v17i18020.

Reddy, M.S. (2023) 'Chi-square test and its utility in forest ecology studies', Journal of global ecology and environment, 17(1), pp. 1-5. Available at: https://doi.org/10.56557/jogee/2023/v17i18020 (Accessed: 15 December 2025).

UK Air (no date) National air quality objectives. Available at: https://uk-air.defra.gov.uk/assets/documents/National_air_quality_objectives.pdf (Accessed: 15 December 2025).