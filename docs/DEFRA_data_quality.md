# DEFRA Air Quality Data Analysis Report

## Executive Summary

This report documents the collection, quality assessment, and validation of air pollution measurements from the UK Department for Environment, Food and Rural Affairs (DEFRA) monitoring network across London. The analysis covered January 2023 through November 2025 (35 months), with overall 2,525,991 hourly measurements from 18 monitoring stations tracking 37 different pollutants.

| Metric                                                   | DEFRA Dataset | Percentage                                                   |
| -------------------------------------------------------- | ------------- | ------------------------------------------------------------ |
| Total number of files                                    | 3,563         |                                                              |
| Total number of each hourly measurement across all files | 2,525,991     | 91.18% measurement value record completeness in DEFRA dataset. |
| Total missing value measurements across all files        | 222,798       | 8.82% missing value measurements.                            |
| Number of monitoring stations/sites in London            | 18            |                                                              |
| Number of collected station/pollutant combinations       | 141           |                                                              |
| Number of pollutants measured                            | 37            |                                                              |
| Total number of measurement files 2023                   | 1,431         | Files from 2023 represent 40.16% of the dataset.             |
| Total number of each hourly measurement for 2023         | 1,000,126     | 90.98% of 2023 values are complete.                          |
| Number of missing value measurements in 2023             | 90,245        | 9.02% of 2023 values are missing.                            |
| Total number of measurement files 2024                   | 1,193         | Files from 2024 represent 33.48% of the dataset.             |
| Total number of each hourly measurement for 2024         | 868,320       | 88.31% of 2024 values are complete.                          |
| Number of missing value measurements in 2024             | 101,522       | 11.69% of 2024 values are missing.                           |
| Total number of measurement files 2025                   | 939           | Files from 2025 represent 26.36% of the dataset.             |
| Total number of each hourly measurement for 2025         | 657,545       | 95.28% of 2025 values are complete.                          |
| Number of missing value measurements in 2025             | 31,031        | 4.72% value measurements missing in 2025.                    |

(data/defra/report/defra_stats.csv file)

DEFRA dataset showed 8.80% missing values according to their dataset flagging below, -1 and -99 markings shows that, the missing values genuine operational errors. 

- -99 flag: Not valid due to station maintenance or calibration. Data is considered to be invalid due to the regular calibration or the normal maintenance of the instrumentation (only used for primary data). (Data Dictionary - Vocabulary, 15.12.2025)

- -1 flag: Not valid. For primary data, data is considered to be invalid due to other circumstances or data is simply missing. For aggregated data, data is not valid because of insufficient data capture following rules set out in Directive and Guidance.  (Data Dictionary - Vocabulary, 15.12.2025).

  

## 1. Dataset Overview

### 1.1 Collection Scope

The DEFRA dataset was systematically collected using the UK Air archive API, accessing hourly measurements stations located within Greater London. Most monitored pollutants in each site PM10 AND -M2.5 after that Nitrogen compounds. London Eltham and London Marylebone Road are the only two stations monitoring the full BTEX suite and other volatile organic compounds.

**Primary regulatory pollutants:** NO₂, NO, NOₓ, PM10, PM2.5, O₃, SO₂, CO (8 pollutants)

**Volatile organic compounds:** 31 VOCs including benzene, toluene, ethylbenzene, xylene isomers (BTEX compounds), and various alkanes, alkenes, and alkynes.

| Pollutant              | Count | Percentage | Stations                                                     |
| ---------------------- | :---- | ---------- | ------------------------------------------------------------ |
| PM10                   | 15    | 10.42%     | Borehamwood Meadow Park, Camden Kerbside, Ealing Horn Lane, London Bexley, London Bloomsbury, London Eltham, London Harlington, London Hillingdon, London Honor Oak Park, London Marylebone Road, London N. Kensington, London Norbury Manor School, London Teddington Bushy Park, Southwark A2 Old Kent Road |
| PM2.5                  | 15    | 10.42%     | Borehamwood Meadow Park, Camden Kerbside, London Bexley, London Bloomsbury, London Eltham, London Harlington, London Hillingdon, London Honor Oak Park, London Marylebone Road, London N. Kensington, London Norbury Manor School, London Teddington Bushy Park, London Westminster |
| NO2                    | 14    | 9.72%      | Borehamwood Meadow Park, Camden Kerbside, Haringey Roadside, London Bexley, London Bloomsbury, London Eltham, London Haringey Priory Park South, London Harlington, London Hillingdon, London Marylebone Road, London N. Kensington, London Westminster, Southwark A2 Old Kent Road, Tower Hamlets Roadside |
| NOx (Nitrogen oxides)  | 14    | 9.72%      | Borehamwood Meadow Park, Camden Kerbside, Haringey Roadside, London Bexley, London Bloomsbury, London Eltham, London Haringey Priory Park South, London Harlington, London Hillingdon, London Marylebone Road, London N. Kensington, London Westminster, Southwark A2 Old Kent Road, Tower Hamlets Roadside |
| NO (Nitrogen monoxide) | 14    | 9.72%      | Borehamwood Meadow Park, Camden Kerbside, Haringey Roadside, London Bexley, London Bloomsbury, London Eltham, London Haringey Priory Park South, London Harlington, London Hillingdon, London Marylebone Road, London N. Kensington, London Westminster, Southwark A2 Old Kent Road, Tower Hamlets Roadside |
| O3 (Ozone)             | 9     | 6.25%      | London Bloomsbury, London Eltham, London Haringey Priory Park South, London Harlington, London Hillingdon, London Honor Oak Park, London Marylebone Road, London N. Kensington, London Westminster |
| SO2                    | 3     | 2.08%      | London Bloomsbury, London Marylebone Road, London N. Kensington |
| CO (Carbon monoxide)   | 2     | 1.39%      | London Marylebone Road, London N. Kensington                 |
| Benzene                | 2     | 1.39%      | London Eltham, London Marylebone Road                        |
| Toluene                | 2     | 1.39%      | London Eltham, London Marylebone Road                        |
| Ethylbenzene           | 2     | 1.39%      | London Eltham, London Marylebone Road                        |
| m,p-Xylene             | 2     | 1.39%      | London Eltham, London Marylebone Road                        |
| o-Xylene               | 2     | 1.39%      | London Eltham, London Marylebone Road                        |
| n-Pentane              | 2     | 1.39%      | London Eltham, London Marylebone Road                        |
| n-Hexane               | 2     | 1.39%      | London Eltham, London Marylebone Road                        |
| n-Heptane              | 2     | 1.39%      | London Eltham, London Marylebone Road                        |
| n-Octane               | 2     | 1.39%      | London Eltham, London Marylebone Road                        |
| n-Butane               | 2     | 1.39%      | London Eltham, London Marylebone Road                        |
| i-Butane               | 2     | 1.39%      | London Eltham, London Marylebone Road                        |
| i-Pentane              | 2     | 1.39%      | London Eltham, London Marylebone Road                        |
| i-Hexane               | 2     | 1.39%      | London Eltham, London Marylebone Road                        |
| i-Octane               | 2     | 1.39%      | London Eltham, London Marylebone Road                        |
| Propane                | 2     | 1.39%      | London Eltham, London Marylebone Road                        |
| Propene                | 2     | 1.39%      | London Eltham, London Marylebone Road                        |
| Ethane                 | 2     | 1.39%      | London Eltham, London Marylebone Road                        |
| Ethene                 | 2     | 1.39%      | London Eltham, London Marylebone Road                        |
| Ethyne                 | 2     | 1.39%      | London Eltham, London Marylebone Road                        |
| 1-Butene               | 2     | 1.39%      | London Eltham, London Marylebone Road                        |
| 1-Pentene              | 2     | 1.39%      | London Eltham, London Marylebone Road                        |
| cis-2-Butene           | 2     | 1.39%      | London Eltham, London Marylebone Road                        |
| trans-2-Butene         | 2     | 1.39%      | London Eltham, London Marylebone Road                        |
| trans-2-Pentene        | 2     | 1.39%      | London Eltham, London Marylebone Road                        |
| 1,3-Butadiene          | 2     | 1.39%      | London Eltham, London Marylebone Road                        |
| Isoprene               | 2     | 1.39%      | London Eltham, London Marylebone Road                        |
| 1,2,3-TMB              | 2     | 1.39%      | London Eltham, London Marylebone Road                        |
| 1,2,4-TMB              | 2     | 1.39%      | London Eltham, London Marylebone Road                        |
| 1,3,5-TMB              | 2     | 1.39%      | London Eltham, London Marylebone Road                        |

(data/defra/report/pollutant_distrubition.csv file and combination of metadata file data/defra/test/std_london_sites_pollutant.csv)

### 1.2 File Organisation

The collected data maintained consistent monthly organisation across the three-year period:

```bash
data/defra/
├── optimised/                              # Standardised validated measurements.
│   ├── 2023measurements/                   # Full year 2023
│   ├── 2024measurements/                   # Full year 2024
│   └── 2025measurements/                   # Partial year 2025
│       └── [Station_Name]/                 # Station/level organisation
│           └── [POLLUTANT]__YYYY_MM.csv    # Format example: NO2__2023_01.csv
│      
│
├── report/                                 #Quality metrics, statistical analysis reports
│   ├── detailed_analysis/
│   │   ├── seasonal_averages.csv           # Seasonaly pollutant patterns 
│   │   ├── yearly_averages.csv		# Annual trends
│   │		└─── distrubition_of_each_pollutants.png
│		│						└─── Visulation of daily avg/distrubition/hourly avg/monthly distrubition
│		│
│   ├── chi_square_tests.csv                # Year-wise distribution validation.
│   ├── defra_stats.csv                     # Dataset summary, record.
│   ├── nan_values_by_pollutant.csv         # Pollutant-level missing data.
│   ├── nan_values_by_station_pollutant.csv # Station-pollutant combinations.
│   ├── pollutant_distribution.csv          # 37 Pollutant distrubution according to sites
│   └── quality_metrics_validation.csv      # Detailed data quality metrics
│
├── test/       # Functions test folder data
│   ├── std_london_sites_pollutant.csv      # Standardised metadata 
│   ├── london_stations_clean.csv           # Parsed station/pollutant         
│   ├── pollutant_mapping.csv 					# EEA website data mapping details
│		└── 5 more other file...
├── capabilities/                           #API endpoints capabilities documentation
│   ├── capabilities.csv                    #SOS GetCapabilities output data
│   ├── capabilities.json                   #SOS GetCapabilities output data json
│   ├── Air_Quality_Objectives_Update.pdf   #UK legal pollutant limits documentation
│   └── uk_pollutant_limits.csv             #UK legal pollutant limits documentation csv
│
├── logs/                                   #Raw data checking logs, before the changes
│   ├── NaN_values_record.csv       # missing data logs
│   └── logs_missin_value.csv 			#output of missing values file
│
├── processed/                              # raw_data folder files, processed and stored
│   └── (reserved for cross-year analysis outputs)
│
└── raw_data/                               # Raw data
    └── (monthly raw/CSV from DEFRA API)
```

**File structure:** contained timestamp, value, timeseries_id, station_name, and pollutant_name columns

Optimased folder each csv file followed this format:

```bash
timestamp,value,timeseries_id,station_name,pollutant_name,pollutant_std,latitude,longitude
```

I added the site metadata columns (coordinates: latitude, longitude) during collection to facilitate future integration with meteorological datasets.

**Naming convention:** ` (pollutant_std)__year_month.csv `within station-specific subdirectories.

The reduced file count from 2023 (1,431) to 2024 (1,193) and then to 2025 (939) reflected the natural progression of a partial-year dataset rather than equipment failures—a distinction confirmed through temporal analysis.

### 1.3 Metadata Validation

The DEFRA collection process began by parsing data/defra/test/london_stations_clean.csv, which contained metadata for all station-pollutant combinations identified through the API.

**Metadata contents:**

**Station identification:** Station ID, station name, geographic coordinates

**Pollutant information:** Pollutant name (standardised), timeseries ID for API queries

**Expected combinations:** 141 unique station-pollutant pairs

During data collection, every combination in the metadata was queried systematically, and the actual retrieved combinations were cross-checked against expectations. This validation step proved critical for showing data gaps from metadata errors, a problem that had severely affected the LAQN data.

## 2. UK Air Quality Standards Framework

### 2.1 Regulatory Context

The UK Air Quality Standards Regulations 2010 (SI 2010/1001) implement EU air quality directives and establish legally binding limits for pollutant concentrations. These standards define thresholds above which air quality is considered harmful to human health and the environment.

### 2.2 Legal Limits Summary

The UK Air Quality Standards pollutants threshold data stored `air-pollution-levels/data/defra/capabilities/Air_Quality_Objectives_Update.pdf` since the document on pdf, created a function `parse_defra_aq_objectives`to parse as csv. But nature of pdf documentation I ended up integrating manually. 

Here is the csv file for UK Air Quality Standards `uk_pollutant_limits.csv`used for validate the optimised data below:

| Pollutant     | Limit       | Averaging Period          | Permitted Exceedances |
| ------------- | ----------- | ------------------------- | --------------------- |
| NO₂           | 40 µg/m³    | Annual mean               | None                  |
| NO₂           | 200 µg/m³   | 1-hour mean               | 18 per year           |
| NOₓ           | 30 µg/m³    | Annual mean               | None                  |
| PM10          | 40 µg/m³    | Annual mean               | None                  |
| PM10          | 50 µg/m³    | 24-hour mean              | 35 per year           |
| PM2.5         | 20 µg/m³    | Annual mean               | None                  |
| O₃            | 100 µg/m³   | 8-hour running mean       | 10 per year           |
| SO₂           | 125 µg/m³   | 24-hour mean              | 3 per year            |
| SO₂           | 350 µg/m³   | 1-hour mean               | 24 per year           |
| CO            | 10 mg/m³    | Maximum daily 8-hour mean | None                  |
| Benzene       | 16.25 µg/m³ | Running annual mean       | None                  |
| 1,3-Butadiene | 2.25 µg/m³  | Running annual mean       | None                  |

(National Air Quality Objectives - UK-air, 15.12.2025)

The remaining 29 VOCs in the dataset had no specific UK legal limits despite being monitored for source apportionment and health risk assessment purposes.

#### UK Air Quality Objectives Averaging Period Calculations: 

**Annual mean limits** (NO₂, NOₓ, PM10, PM2.5) calculated yearly means then averaged across all available years. For a measurement to be valid, the year needed at least 75% data capture (273 days).

**24-hour mean limits** (PM10, SO₂) took daily means calculated from hourly values, then counted exceedances per calendar year. Compliance meant staying under the permitted exceedance limit.

**8-hour running mean** (O₃, CO) used a continuous rolling 8-hour average updated hourly. Each hour's mean comprised that hour plus the previous 7 hours, with exceedances counted per year.

**1-hour mean limits** (NO₂, SO₂) compared hourly values directly against thresholds and counted how many hours per year exceeded the limit.

**Running annual mean** (Benzene, 1,3-Butadiene) calculated a continuous 365-day (8760-hour) rolling average requiring minimum 300 days data capture per rolling year.

## 3. Data Quality Validation

### 3.1 Quality Assessment Methodology

The `calculate_quality_metrics_uk_limits()` function checks `uk_pollutant_limits.csv` files for available pollutants if they're matching with threshold limitations. The function calculate average period detection. 

- Loads all measurement files for the years 2023, 2024, and 2025.
- Reads the official UK pollutant limits from a CSV file.
- For each pollutant, it checks:
  - If any values are negative (which is not possible in reality).
  - If any values are extremely high (likely sensor errors).
  - If the measurements exceed the UK legal limits (for different averaging periods, like annual mean or 24-hour mean).

quality_metrics_validation.csv each csv file followed this format:

```bash
pollutant,total_measurements,mean_hourly,min,max,p95,negative_values,zero_values,out_of_range,uk_annual_limit,mean_annual,exceeds_annual,uk_24hour_limit,daily_exceedances

```



- It calculates basic statistics (mean, median, standard deviation, min, max, percentiles) for each pollutant.
- It reports how many measurements are negative, zero, or out of range.
- It checks if the annual or daily averages exceed the UK limits.
- As output creates a report `quality_metrics_validation.csv`

##### Quality Metric Result Table for DEFRA

| Metric                           | NOx    | NO2    | SO2    | Benzene | 1,3-Butadiene | CO    | PM2.5  | PM10   | O3     |
| -------------------------------- | ------ | ------ | ------ | ------- | ------------- | ----- | ------ | ------ | ------ |
| Total<br />measurements          | 300408 | 300586 | 65747  | 25063   | 25248         | 45500 | 205122 | 189562 | 167093 |
| Hourly Mean                      | 33.00  | 20.79  | 1.94   | 0.51    | 0.15          | 0.22  | 7.80   | 13.22  | 46.66  |
| Minimum Value <br />Recorded     | 0.00   | 0.00   | 0.00   | 0.00    | 0.01          | 0.00  | 0.00   | 0.00   | 0.00   |
| Maximum Value <br />Recorded     | 861.01 | 274.62 | 156.19 | 54.47   | 9.76          | 2.54  | 189.53 | 857.17 | 200.17 |
| 95th Percentile value            | 104.04 | 53.36  | 4.79   | 1.29    | 0.37          | 0.55  | 20.95  | 31.30  | 84.42  |
| Negative<br />Values             | 0      | 0      | 0      | 0       | 0             | 0     | 0      | 0      | 0      |
| Number of<br />Zero Measurements | 207    | 553    | 851    | 0       | 0             | 2406  | 801    | 48     | 316    |
| Possible Sensor Errors           | 534    | 0      | 0      | 0       | 0             | 0     | 0      | 4      | 0      |
| UK Legal Limit<br />Annual mean  | 30.0   | 40.0   |        | 16.25   | 2.25          | 10    | 20.0   | 40.0   | 100    |
| Annual Mean                      | 32.75  | 20.68  |        |         |               |       | 7.75   | 13.19  |        |
| Annual Mean <br />Exceeds        | yes    | no     |        |         |               |       | no     | no     |        |
| UK Legal<br />24 Hour Limit      |        |        | 125.0  |         |               |       |        | 50.0   |        |

### Explanation of Output Headers

- **mean_hourly**: Average value of all hourly measurements.
- **min**: Minimum value recorded.
- **max**: Maximum value recorded.
- **p95**: 95th percentile value (value below which 95% of data falls).It helps understand the upper range of typical measurements, filtering out the most extreme5% of values, which might be outliers or rare events. It gives a sense of the normal = high values at DEFRA data, without being skewed by rare spikes or errors.
- **negative_values**: Number of negative measurements (should be zero in good data).
- **zero_values**: Number of zero measurements.
- **out_of_range**: Number of values that are extremely high likely sensor errors.
- **uk_annual_limit**: The UK legal limit for the annual mean.
- **mean_annual**: The actual annual mean calculated from the data.
- **exceeds_annual**: Whether the annual mean exceeds the UK limit (yes/no).
- **uk_24hour_limit**: The UK legal limit for the 24-hour mean (if defined).
- **daily_exceedances**: Number of days where the daily mean exceeded the UK 24-hour limit.

### 3.2 Missing Data Assesment by Pollutant

| Pollutant       | Total Records | Total Missing | Percentage Missing |
| --------------- | ------------- | ------------- | ------------------ |
| NO              | 326,061       | 25,944        | 7.96%              |
| NO2             | 326,072       | 25,486        | 7.82%              |
| NOx             | 325,387       | 24,979        | 7.68%              |
| PM10            | 227,142       | 37,580        | 16.54%             |
| PM2.5           | 234,748       | 29,626        | 12.62%             |
| O3              | 194,333       | 27,240        | 14.02%             |
| SO2             | 72,928        | 7,181         | 9.85%              |
| 1,2,3-TMB       | 26,649        | 1,560         | 5.85%              |
| 1,2,4-TMB       | 26,649        | 1,610         | 6.04%              |
| 1,3,5-TMB       | 26,649        | 1,641         | 6.16%              |
| 1,3-Butadiene   | 26,568        | 1,320         | 4.97%              |
| 1-Butene        | 26,599        | 1,307         | 4.91%              |
| 1-Pentene       | 26,572        | 1,381         | 5.20%              |
| Benzene         | 26,649        | 1,586         | 5.95%              |
| Ethane          | 26,599        | 1,315         | 4.94%              |
| Ethene          | 26,618        | 1,312         | 4.93%              |
| Ethylbenzene    | 26,649        | 1,592         | 5.97%              |
| Ethyne          | 26,529        | 1,328         | 5.01%              |
| Isoprene        | 26,618        | 1,341         | 5.04%              |
| Propane         | 26,618        | 1,316         | 4.94%              |
| Propene         | 26,618        | 1,312         | 4.93%              |
| Toluene         | 26,649        | 1,640         | 6.15%              |
| cis-2-Butene    | 26,599        | 1,378         | 5.18%              |
| i-Butane        | 26,599        | 1,308         | 4.92%              |
| i-Hexane        | 26,599        | 1,321         | 4.97%              |
| i-Octane        | 26,649        | 1,624         | 6.09%              |
| i-Pentane       | 26,618        | 1,306         | 4.91%              |
| m,p-Xylene      | 25,503        | 1,612         | 6.32%              |
| n-Butane        | 26,599        | 1,307         | 4.91%              |
| n-Heptane       | 26,649        | 1,622         | 6.09%              |
| n-Hexane        | 26,580        | 1,320         | 4.97%              |
| n-Octane        | 26,649        | 1,764         | 6.62%              |
| n-Pentane       | 26,618        | 1,306         | 4.91%              |
| o-Xylene        | 26,649        | 1,568         | 5.88%              |
| trans-2-Butene  | 26,599        | 1,321         | 4.97%              |
| trans-2-Pentene | 26,599        | 1,366         | 5.14%              |
| CO              | 48,578        | 3,078         | 6.34%              |

(data/defra/report/nan_values_by_pollutant.csv file)

Missing data varies across pollutants, with the highest gaps observed for PM10 (16.54%), O3 (14.02%), and PM2.5 (12.62%). These elevated missing rates likely reflect the technical challenges and limited coverage associated with monitoring these pollutants. Most other pollutants have missing data rates below 10%.

## 4. Chi-Square Test for Data Uniformity

To verify the consistency of the DEFRA data collection throughout the year, chi-square testused. This test compares the number of files collected each month to what would be expected if the data were evenly spread out.

For this dataset, the chi-square statistic was 65.76 and the p-value was 0.0000. This p-value is much less than 0.05, which means the data are not evenly distributed across the months. In other words, some months have noticeably more or fewer files than others.

This result suggests that there may have been gaps or changes in data collection during the year. Possible reasons could include missing data for certain months, stations starting or stopping reporting, or technical issues with the data collection process. Because of this, I will need to look more closely at the monthly data and consider whether any months should be treated differently in the analysis.

In summary, the chi-square test shows that the data are unevenly distributed over the year, so extra care is needed when interpreting trends or making seasonal comparisons.

The chi-square test assessed whether files were evenly distributed across months, testing for systematic collection bias or temporal gaps(M. Sridhar Reddy (2023) “Chi-square Test and Its Utility in Forest Ecology Studies”).

## 5. Seasonal Trend Analysis

### 5.1 Data Overview

The analysis `defra_analyse.ipynb` notebook section 6, very detailed seasonal analysis conducted.

#### Pollutant Coverage

The dataset includes high measurement counts for key pollutants:

- **Nitrogen dioxide (NO₂):** 326,072 measurements
- **Nitrogen monoxide (NO):** 326,061 measurements
- **Nitrogen oxides (NOₓ):** 325,387 measurements
- **PM2.5:** 234,748 measurements
- **PM10:** 227,142 measurements
- **Ozone (O₃):** 194,333 measurements
- **Sulphur dioxide (SO₂):** 72,928 measurements
- **Carbon monoxide (CO):** 48,578 measurements

A wide range of volatile organic compounds (VOCs) such as benzene, toluene, and various xylene isomers are also well represented, each with over 25,000 measurements.

### 5.2 Yearly and Seasonal Trends

#### Yearly Trends

Yearly averages were calculated for each pollutant, revealing how concentrations changed over the three-year period. For example:

- **NO₂:** Mean values decreased slightly from 21.95 µg/m³ in 2023 to 19.75 µg/m³ in 2025.
- **Ozone:** Mean values increased from 45.62 µg/m³ in 2023 to 49.85 µg/m³ in 2025.
- **PM2.5:** Mean values remained relatively stable, with 8.16 µg/m³ in 2023 and 8.10 µg/m³ in 2025.

These trends suggest gradual improvements for some pollutants, while others, such as ozone, show a slight upward trend.

#####  Seasonal Variation in Air Pollutant Concentrations

The file `seasonal_averages.csv` summarises how the average concentrations of various air pollutants change throughout the year. For each pollutant, the mean value is calculated separately for Winter, Spring, Summer, and Autumn.

| Pollutant                           | Winter | Spring | Summer | Autumn |
| ----------------------------------- | ------ | ------ | ------ | ------ |
| 1,2,3-Trimethylbenzene              | 0.03   | 0.03   | 0.03   | 0.03   |
| 1,2,4-Trimethylbenzene              | 0.73   | 0.59   | 0.51   | 2.05   |
| 1,3,5-Trimethylbenzene              | 0.17   | 0.11   | 0.13   | 0.14   |
| 1-Butene                            | 0.35   | 0.27   | 0.29   | 0.36   |
| 1-Pentene                           | 0.07   | 0.15   | 0.15   | 0.08   |
| 1.3 Butadiene                       | 0.14   | 0.13   | 0.16   | 0.17   |
| Benzene                             | 0.80   | 0.40   | 0.37   | 0.53   |
| Carbon monoxide                     | 0.28   | 0.21   | 0.17   | 0.23   |
| Ethane                              | 10.36  | 6.42   | 4.54   | 6.62   |
| Ethene                              | 1.92   | 1.12   | 1.13   | 1.72   |
| Ethyl benzene                       | 0.51   | 0.87   | 0.42   | 0.80   |
| Ethyne                              | 0.92   | 0.53   | 0.41   | 0.59   |
| Isoprene                            | 0.07   | 0.08   | 0.34   | 0.14   |
| Nitrogen dioxide                    | 25.43  | 20.42  | 15.51  | 22.86  |
| Nitrogen monoxide                   | 12.19  | 6.34   | 5.14   | 9.08   |
| Nitrogen oxides                     | 44.32  | 30.05  | 23.39  | 36.75  |
| Ozone                               | 38.78  | 55.40  | 51.25  | 38.60  |
| Particulate matter less than 10 µm  | 14.14  | 15.03  | 11.34  | 12.45  |
| Particulate matter less than 2.5 µm | 9.00   | 8.99   | 5.92   | 7.38   |
| Propane                             | 5.96   | 3.83   | 3.36   | 5.15   |
| Propene                             | 0.89   | 0.60   | 0.80   | 1.04   |
| Sulphur dioxide                     | 2.39   | 2.01   | 1.96   | 1.48   |
| Toluene                             | 1.92   | 1.09   | 1.37   | 1.96   |
| cis-2-Butene                        | 0.13   | 0.11   | 0.10   | 0.14   |
| i-Butane                            | 3.27   | 2.01   | 1.80   | 2.97   |
| i-Hexane                            | 0.57   | 0.48   | 0.63   | 0.64   |
| i-Octane                            | 0.37   | 0.21   | 0.31   | 0.36   |
| i-Pentane                           | 1.78   | 1.20   | 1.56   | 1.98   |
| m,p-Xylene                          | 1.95   | 3.20   | 1.40   | 2.44   |
| n-Butane                            | 5.03   | 3.21   | 3.25   | 4.60   |
| n-Heptane                           | 0.40   | 0.24   | 0.30   | 0.38   |
| n-Hexane                            | 0.34   | 0.24   | 0.30   | 0.68   |
| n-Octane                            | 0.15   | 0.09   | 0.10   | 0.13   |
| n-Pentane                           | 0.88   | 0.56   | 0.67   | 0.88   |
| o-Xylene                            | 0.68   | 1.08   | 0.66   | 1.07   |
| trans-2-Butene                      | 0.23   | 0.18   | 0.14   | 0.18   |
| trans-2-Pentene                     | 0.07   | 0.05   | 0.08   | 0.12   |

- All values are mean concentrations for the given season and pollutant.
- Units are e.g., µg/m³ for most pollutants, mg/m³ for CO.

This seasonal breakdown allows us to identify patterns such as:

- **Ozone (O₃):** levels are highest in spring (55.40) and summer (51.25), and lowest in winter (38.78) and autumn (38.60). This reflects increased sunlight and photochemical activity in warmer months.
- **Nitrogen dioxide (NO₂) and Nitrogen oxides (NOₓ):**Both NO₂ and NOₓ are highest in winter (NO₂: 25.43, NOₓ: 44.32) and autumn (NO₂: 22.86, NOₓ: 36.75), and lowest in summer (NO₂: 15.51, NOₓ: 23.39). This likely results from increased emissions from heating and less atmospheric dispersion in colder months.
- **Particulate matter (PM10 and PM2.5):**PM10 and PM2.5 concentrations are generally higher in winter (PM10: 14.14, PM2.5: 9.00) and spring (PM10: 15.03, PM2.5: 8.99), and lower in summer (PM10: 11.34, PM2.5: 5.92). This may be due to increased combustion and stagnant air during colder seasons.
- **Carbon monoxide (CO):**CO is highest in winter (0.28) and lowest in summer (0.17), consistent with increased heating and reduced atmospheric mixing in winter.
- **Benzene:**Benzene shows a similar pattern, with higher concentrations in winter (0.80) and autumn (0.53), and lower in spring (0.40) and summer (0.37).
- **Sulphur dioxide (SO₂):**SO₂ is highest in winter (2.39) and spring (2.01), and lowest in autumn (1.48), again reflecting increased combustion for heating.
- **Isoprene:**Isoprene peaks in summer (0.34), which is expected as it is mainly produced by vegetation and increases with temperature and sunlight.
- **Volatile Organic Compounds (VOCs) like Toluene, Ethyl benzene, and Xylenes:**These generally show higher values in winter and autumn, and lower in summer, likely due to increased emissions from heating and reduced atmospheric dispersion.

Most pollutants are higher in winter and autumn, reflecting increased emissions and less atmospheric mixing. Ozone and isoprene are exceptions, peaking in spring and summer due to photochemical processes and biological activity. These seasonal patterns are important for understanding when and why air quality issues are most severe, and for designing effective pollution control strategies.

### 5.3 Annual Summary of Pollutants:

The file `yearly_averages.csv` contains the annual summary statistics for each pollutant in dataset, broken down by year.

### What does it explain?

- **Annual Trends:**By comparing the mean and median values across years for each pollutant, to see if pollution levels are rising, falling, or staying the same.
- **Data Completeness:**The count column shows how much data was collected for each pollutant each year, which helps assess data coverage and reliability.

The pollutants included in the table below: Nitrogen dioxide (NO₂), Nitrogen oxides (NOₓ), Ozone (O₃), PM10, PM2.5, Sulphur dioxide (SO₂), Carbon monoxide (CO), Benzene, and 1,3-Butadiene are among the most important for air quality assessment and public health. They are:

| Pollutant        | 2023  | 2024  | 2025  |
| ---------------- | ----- | ----- | ----- |
| Nitrogen dioxide | 21.95 | 20.35 | 19.75 |
| Nitrogen oxides  | 36.20 | 31.49 | 30.56 |
| Ozone            | 45.62 | 44.88 | 49.85 |
| PM10             | 13.82 | 11.80 | 13.94 |
| PM2.5            | 8.16  | 7.00  | 8.10  |
| Sulphur dioxide  | 2.01  | 2.08  | 1.68  |
| Carbon monoxide  | 0.21  | 0.20  | 0.24  |
| Benzene          | 0.53  | 0.51  | 0.46  |
| 1,3-Butadiene    | 0.08  | 0.15  | 0.26  |

- NO₂ and NOₓ levels have gradually decreased over the three years, suggesting improvements in air quality or emission controls.
- Ozone (O₃) levels remained stable in 2023 and 2024, with a slight increase in 2025.
- PM10 and PM2.5 concentrations were lowest in 2024, but increased again in 2025.
- SO₂ and Benzene levels remained low and relatively stable, indicating effective control of these pollutants.
- Carbon monoxide (CO) showed a small increase in 2025, but remained at low concentrations.
- 1,3-Butadiene increased each year, though values remained low.

Overall, the table provides a clear year-by-year view of air quality trends for the most important pollutants, helping to identify improvements, emerging issues, and areas needing further attention.

### 5.4 UK Air Policy Check

The `limit_exceedances.csv` table provides a direct assessment of how well the air quality in the dataset complies with official UK air quality standards for key pollutants. Its main purpose is to summarise, transparently and quantitatively, how often pollutant concentrations exceeded the legal limits set to protect public health.

- **Regulatory Compliance:**The table allows for a straightforward check of whether the air pollution levels recorded in the dataset meet or breach the UK’s legal requirements for each pollutant. 
- **Risk Identification:**By showing the number and percentage of exceedances for each pollutant, the table highlights which pollutants and time periods are most problematic. 
- **Transparency and Accountability:**Including this table in your report demonstrates a rigorous, evidence-based approach. It provides clear documentation of where and how often air quality standards are not met.



| Pollutant                         | Code          | Objective / Limit Description               | Averaging Period    | Limit Value | Unit  | Total Measurements | Exceedances | % Exceedance |
| --------------------------------- | ------------- | ------------------------------------------- | ------------------- | ----------- | ----- | ------------------ | ----------- | ------------ |
| Ozone                             | O3            | 100 µg/m³ not to be exceeded >10 times/year | 8 hour mean         | 100.0       | µg/m³ | 167,093            | 2,831       | 1.69         |
| Nitrogen oxides                   | NOx           | 30 µg/m³                                    | annual mean         | 30.0        | µg/m³ | 300,408            | 107,709     | 35.85        |
| 1.3 Butadiene                     | 1,3-butadiene | 2.25 µg/m³                                  | running annual mean | 2.25        | µg/m³ | 25,248             | 5           | 0.02         |
| Benzene                           | Benzene       | 16.25 µg/m³                                 | running annual      | 16.25       | µg/m³ | 25,063             | 3           | 0.01         |
| Nitrogen dioxide                  | NO2           | 40 µg/m³                                    | annual mean         | 40.0        | µg/m³ | 300,586            | 37,422      | 12.45        |
| Sulphur dioxide                   | SO2           | 125 µg/m³ not to be                         | 24 hour mean        | 125.0       | µg/m³ | 65,747             | 2           | 0.0          |
| Particulate matter <2.5µm (PM2.5) | PM2.5         | 20 µg/m³ not to be                          | annual mean         | 20.0        | µg/m³ | 205,122            | 11,194      | 5.46         |
| Carbon monoxide                   | CO            | 10 mg/m³                                    | maximum daily       | 10.0        | mg/m³ | 45,500             | 0           | 0.0          |
| Particulate matter <10µm (PM10)   | PM10          | 50 µg/m³ not to be                          | 24 hour mean        | 50.0        | µg/m³ | 189,562            | 1,986       | 1.05         |
| Particulate matter <10µm (PM10)   | PM10          | 40 µg/m³                                    | annual mean         | 40.0        | µg/m³ | 189,562            | 4,462       | 2.35         |



This table summarises the compliance of the measured air pollution data with the `uk_pollutant_limits.csv` file limits. For each pollutant, the table lists the legal limit (objective), the averaging period over which the limit applies, the total number of measurements, the number of times the limit was exceeded, and the percentage of exceedances.

- If the percentage of exceedances is low or zero, it means the pollutant levels at dataset are generally within the UK legal limits, indicating compliance.
- If the percentage is high, it means the pollutant frequently exceeded the legal limit, suggesting non-compliance and potential air quality concerns.

- High exceedance rates highlight pollutants and periods where air quality improvements may be needed.

## Citations:

*Vocabulary: Aqd - observation validity* (no date) *Data Dictionary - Vocabulary*. Available at: https://dd.eionet.europa.eu/vocabulary/aq/observationvalidity (Accessed: 15 December 2025). 

M. Sridhar Reddy (2023) “Chi-square Test and Its Utility in Forest Ecology Studies”, *Journal of Global Ecology and Environment*, 17(1), pp. 1–5. doi: 10.56557/jogee/2023/v17i18020.

UK Air (no date) National air quality objectives. Available at: https://uk-air.defra.gov.uk/assets/documents/National_air_quality_objectives.pdf (Accessed: 15 December 2025).

European Environment Agency (no date) Vocabulary: observation validity, Data dictionary. Available at: https://dd.eionet.europa.eu/vocabulary/aq/observationvalidity (Accessed: 15 December 2025).
