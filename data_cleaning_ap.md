# Data Cleaning Guide

## Overview

This guide outlines the data cleaning process for the air pollution prediction project. The cleaning stage sits between data collection and feature engineering. The goal is to ensure all datasets (LAQN, DEFRA, METEO) are consistent, complete, and ready for analysis.

## Current Project Status

As documented in reporting19.md, the project has successfully completed API data collection from LAQN, DEFRA, and meteorological sources for 2023-2025. The next step is systematic data cleaning before feature engineering.

## Data Cleaning Objectives

1. Identify and handle missing values across all datasets.
2. Standardise pollutant names using pollutant_mapps.py.
3. Ensure temporal alignment across all datasets with consistent timestamps.
4. Remove duplicates and validate data integrity.
5. Document all cleaning decisions for reproducibility.

## Stage 1: Initial Data Assessment

Before cleaning, need to examine each dataset to understand its current state.

### LAQN Data Assessment

Location: `data/laqn/monthly_data/`

Start with `df.head()` to look at the first few rows and check if column names match expectations and values look reasonable. Then `df.tail()` to check the last few rows since data quality sometimes degrades at the end of collection periods.

Use `df.info()` to check data types. Timestamps should be datetime objects, not strings, and values should be numeric. Check `df.shape` to see if row count matches expectations for hourly data over a month.

Run `df.isnull().sum()` to count missing values in each column and identify which columns have gaps. Then `df.describe()` to look at statistical summaries and check if minimum and maximum values are sensible or if there are negative pollution values.

Finally check `df['@MeasurementDateGMT'].dtype` to confirm the timestamp column is actually datetime format or still a string. If timestamps are strings, cannot sort by time or calculate time differences. If pollution values are negative, something went wrong with the sensor or data transmission. If there are 744 rows but expected 720 (30 days × 24 hours), might have duplicates. If there are 650 rows, data is missing.

### DEFRA Data Assessment

Location: `data/defra/{year}measurements/`

Use `df.head()` to verify structure. Station name, pollutant name, and timestamp should all be present. Run `df.info()` to check if timestamp is datetime format and if value column is numeric.

Check `df.isnull().sum()` since DEFRA data sometimes has gaps when stations go offline. Use `df.duplicated(subset=['timestamp']).sum()` to check for duplicate timestamps for the same station. Run `df['value'].describe()` for statistical summary to see if values are in a reasonable range for the pollutant.

DEFRA uses different column names than LAQN, need to know this before merging datasets. If timestamps have duplicates, need to decide which measurement to keep. If the value column has nulls, need to decide whether to interpolate or drop those hours.

### METEO Data Assessment

Location: `data/meteo/raw/monthly{year}/`

Start with `df.head()` to verify all expected weather variables are present: temperature, wind speed, pressure, humidity, precipitation. Use `df.info()` to check data types since all weather variables should be numeric. Confirm `df['date'].dtype` is datetime format.

Run `df.isnull().sum()` even though weather APIs usually have complete data. Generate what the complete hourly range should be with `pd.date_range(start=df['date'].min(), end=df['date'].max(), freq='H')` and check if any hours are missing from the sequence.

Weather data should be continuous hourly measurements. If hours are missing, merged dataset will have gaps. If temperature is stored as text instead of numbers, calculations will fail. If precipitation is negative, the API returned bad data.

## Stage 2: Data Quality Issues Identification

### Common Issues to Check

Use `df.isnull().sum()` to find missing values. A few missing values can be interpolated but many missing values mean the sensor was offline or malfunctioning.

Check for duplicate records with `df.duplicated().sum()` or `df.duplicated(subset=['timestamp']).sum()`. Duplicates happen when data transmission errors cause the same measurement to be recorded twice.

Find outliers using `df.describe()` and `df['column'].quantile([0.01, 0.99])`. Values far outside the typical range might be sensor errors.

Check for inconsistent timestamps by examining `df['timestamp'].dtype`. If it says object, the timestamps are strings and need conversion with `pd.to_datetime()`.

Look for inconsistent pollutant naming since LAQN uses codes like NO2 while DEFRA uses full names like Nitrogen dioxide. Need a mapping to standardise these.

### Understanding the Issues

If there is 30% missing data, any patterns found might not be real but just reflect when the sensor was working versus broken. If the same measurement appears twice, statistical calculations will be wrong and averages will be skewed toward duplicated values.

A recorded PM2.5 value of 5000 µg/m³ is physically impossible in London, clearly a sensor malfunction that will distort the model if included. If timestamps are strings, cannot sort chronologically or merge datasets by time since Python will sort 2024-01-02 before 2024-01-10 alphabetically.

When merging LAQN and DEFRA data, need to know that NO2 and Nitrogen dioxide refer to the same pollutant. Without standardisation, they will appear as different variables.

## Stage 3: Data Cleaning Strategy

### Decision Framework for Missing Values

Less than 5% missing means interpolation is acceptable using linear interpolation between surrounding values. A few missing hours in a month of data will not significantly affect patterns and interpolating fills small gaps without introducing much error.

Between 5% and 20% missing requires flagging for manual review to check if missing values cluster at specific times. If data is missing randomly, interpolation is still acceptable. If data is missing every night, that is a systematic problem and interpolating would hide a real pattern in sensor availability.

More than 20% missing means considering excluding this site-pollutant-month combination since cannot be confident in any patterns when data quality is too poor to be useful.

For consecutive missing blocks, do not interpolate but mark as data gap. If 24 consecutive hours are missing, the sensor was offline and interpolating would create fake data that did not actually exist.

### LAQN Cleaning Process

Convert timestamp to datetime using `pd.to_datetime()` on the `@MeasurementDateGMT` column since need datetime objects to sort chronologically, calculate time differences, and merge with other datasets by time.

Remove duplicates using `df.drop_duplicates(subset=['@MeasurementDateGMT'], keep='first')` to keep the first measurement when duplicates exist since the first is more likely to be the original reading before any transmission errors.

Sort by timestamp using `df.sort_values('@MeasurementDateGMT')` because time series data must be in chronological order for interpolation to work correctly and makes the data easier to visually inspect.

Handle missing values by first counting them with `df['@Value'].isnull().sum()` then calculating the percentage and applying the decision framework above. If interpolating, use `df['@Value'].interpolate(method='linear', limit=3)` where the limit parameter prevents interpolating over gaps larger than 3 hours. A gap of 1-3 hours is likely a temporary sensor glitch but a gap of 6+ hours suggests the sensor was offline or malfunctioning, so do not want to invent data for long outages.

Handle negative values using `df.loc[df['@Value'] < 0, '@Value'] = 0` since negative pollution values are physically impossible and result from sensor calibration errors. Setting them to 0 is more realistic than keeping impossible negative numbers.

Add metadata columns with `data_source='LAQN'` and `cleaned=True` so when merging multiple datasets later, can track which source each measurement came from. The cleaned flag helps distinguish processed data from raw data.

### DEFRA Cleaning Process

Convert timestamp to datetime using `pd.to_datetime()` on the timestamp column for the same reason as LAQN, need datetime objects for time-based operations.

Remove duplicates using `df.drop_duplicates(subset=['timestamp'], keep='first')` with same logic as LAQN to keep first occurrence and discard duplicates.

Sort by timestamp using `df.sort_values('timestamp')` since chronological order is required for time series analysis.

Handle missing values by counting with `df['value'].isnull().sum()`, calculating percentage, and applying decision framework. If interpolating, use `df['value'].interpolate(method='linear', limit=3)` with same interpolation logic as LAQN where small gaps can be filled but large gaps should not be.

Handle negative values using `df.loc[df['value'] < 0, 'value'] = 0` since negative pollution values are impossible sensor errors.

Add metadata with `data_source='DEFRA'` and `cleaned=True` to track data provenance when merging datasets.

### METEO Cleaning Process

Convert timestamp to datetime using `pd.to_datetime()` on the date column since consistent datetime format across all datasets is required for merging.

Remove duplicates using `df.drop_duplicates(subset=['date'], keep='first')` because weather data should have one reading per hour and duplicates are transmission errors.

Sort by timestamp using `df.sort_values('date')` since weather data must be chronologically ordered.

Check for missing hours by creating expected hourly range with `pd.date_range(start=df['date'].min(), end=df['date'].max(), freq='H')` and finding missing hours with `expected_range.difference(df['date'])`. Weather APIs should provide continuous hourly data and if hours are missing, creates problems when merging with pollution data.

If hours are missing, reindex the dataframe using `df.set_index('date').reindex(expected_range)` which creates rows for missing hours with null values. This is better than implicit gaps since makes it clear where data is missing.

Interpolate missing meteorological values using `df[col].interpolate(method='linear', limit=2)` for each weather variable. Use limit=2 because weather conditions change gradually and missing 1-2 hours can be reasonably interpolated but missing 5+ hours might span a weather front passage and cannot reliably interpolate.

Forward fill remaining missing values using `df.fillna(method='ffill', limit=1)`. If interpolation did not work due to too large a gap, use the previous hour's value for one hour since weather usually persists for at least an hour. Beyond one hour, leave as null rather than assuming conditions stayed constant.

Add metadata with `data_source='METEO'` and `cleaned=True` for same data provenance tracking as other datasets.

## Stage 4: Pollutant Name Standardisation

The project includes `src/pollutant_mapps.py` which standardises pollutant names across LAQN and DEFRA datasets. This step is critical because the two data sources use different naming conventions.

LAQN uses short codes: NO2, PM25, PM10, O3, SO2, CO. DEFRA uses full names: Nitrogen dioxide, Particulate Matter PM2.5, Particulate Matter PM10, Ozone, Sulphur dioxide, Carbon monoxide.

The PollutantMapper class in pollutant_mapps.py creates a unified naming scheme where all pollutants are mapped to standard codes. When merging LAQN and DEFRA data, need to combine measurements of the same pollutant. Without standardisation, NO2 from LAQN and Nitrogen dioxide from DEFRA would appear as separate variables and the model would not learn that they are the same thing.

The pollutant_mapps.py file already includes methods for batch processing: `std_laqn_pollutants()` and `std_defra_pollutants()`. These read raw files, add a `pollutant_std` column with standardised names, and save to `data/{source}/processed/`.

After running standardisation, all datasets will have a pollutant_std column with consistent codes. This column should be used for merging and analysis instead of the original pollutant name columns.

## Stage 5: Batch Processing All Files

Need to apply cleaning steps to all files systematically since cannot do this manually for hundreds of files.

Create a batch processing script that finds all files in the raw data directories, applies the appropriate cleaning function to each file, saves cleaned files to processed directories, maintains the same folder structure with year/month organisation, and logs any errors without stopping the entire process.

Use tqdm for progress bars to see how many files have been processed and estimate remaining time. Use try-except blocks around each file so if one file has an unexpected problem, the script continues with other files instead of crashing.

Manual cleaning of 2000+ files would take weeks and introduce human error. Batch processing applies the same logic consistently to every file and can run overnight to wake up to cleaned data.

## Stage 6: Validation and Quality Checks

After cleaning, validate that the processed data meets quality standards.

Check that every raw file has a corresponding processed file. If a file is in raw but not in processed, something failed during cleaning.

Sample random processed files and verify no missing values in critical columns (timestamp, value, identifiers), no negative pollution values remain, no duplicate timestamps, timestamp column is datetime type not string, and all expected columns are present.

Check statistical summaries using `df.describe()` on processed files and compare to raw files. Cleaning should not drastically change the distribution unless removing many outliers.

Create a validation report listing total files processed, files with issues that need manual review, and summary statistics before and after cleaning.

Cannot trust cleaned data without checking it. Validation catches errors in the cleaning logic before moving to feature engineering. Finding problems now is much easier than discovering them during modelling when the cause is unclear.

## Stage 7: Documentation

Document all cleaning decisions and create a data dictionary.

### Cleaning Log

Create `data/cleaning_log.md` to track all cleaning operations.

Record for each dataset the date processing was done, number of files processed, output location, cleaning steps applied, issues encountered, and decisions made for ambiguous cases.

Six months from now, need to remember why certain files were excluded or why specific interpolation limits were chosen. Documentation ensures the process is reproducible and decisions can be explained.

### Data Dictionary

Create `data/data_dictionary.md` describing the structure of cleaned data.

For each dataset, list file location, column names and descriptions, data types, units of measurement, and any transformations applied.

When merging datasets or creating features, need a reference for what each column means. A data dictionary prevents confusion about whether temperature is in Celsius or Fahrenheit, whether timestamps are UTC or local time, whether PM25 refers to PM2.5 or something else.

## Stage 8: Final Checks Before Feature Engineering

Before moving to feature engineering, verify all raw files have corresponding processed files by checking file counts match. Confirm no critical columns contain missing values using `df.isnull().sum()` on sample files.

Check all timestamps are in consistent format using `df.dtypes` on sample files from each dataset. Verify pollutant names are standardised across LAQN and DEFRA by confirming pollutant_std column exists and has consistent values.

Confirm data ranges are sensible and no extreme outliers remain using `df.describe()` on sample files.

If any of these checks fail, go back to the relevant cleaning stage and fix the issue before proceeding. Feature engineering assumes cleaned data. If timestamp formats are inconsistent, merging will fail. If pollutant names are not standardised, features will be calculated separately for what should be the same variable. Catching problems now prevents wasted time later.

## Next Steps

After completing data cleaning, update reporting19.md with cleaning statistics and any issues encountered. Run data inventory again using src/data_inventory.py to document the processed datasets.

Begin feature engineering as outlined in the MS proposal Section 5.3. Create temporal features like hour of day, day of week, and season. Create spatial features including distance calculations and borough classifications. Merge LAQN, DEFRA, and METEO datasets on common timestamps.

