# LAQN Data Preparation & Quality Assessment

## 1. Introduction

This chapter documents the systematic process of preparing the London Air Quality Network dataset for predictive modelling. After collecting hourly measurements from 84 monitoring sites across Greater London spanning January 2023 to November 2025, I needed to understand what I actually had and ensure the data was fit for purpose. The preparation phase revealed significant challenges that required iterative investigation and thoughtful decision-making about how to handle equipment failures, missing measurements, and metadata inconsistencies.

The chapter begins with my initial encounter with the collected dataset, follows through the discovery of serious data quality issues, documents my investigation process, and concludes with the cleaning decisions that resulted in a validated dataset ready for exploratory analysis. This wasn't a straightforward process. What started as a simple quality check evolved into a comprehensive audit that changed my understanding of which monitoring equipment actually existed vs what the API metadata claimed was active. The analysis proceeded through multiple stages of refinement, ultimately requiring consideration of temporal consistency across years to ensure the dataset would support robust machine learning predictions.

### 1.1 Key Steps & Results

This data preparation phase systematically transformed a problematic raw dataset into a validated foundation for machine learning through three cleaning stages:

**Stage 1: Permanent Non-Active Equipment (Metadata Correction)**

- **Action:** Identified 38 combinations with zero measurements across all 35 months.
- **Decision:** Corrected metadata only; kept files for audit trail.
- **Result:** 252 → 216 validated combinations; issue rate 37%.
- **Learning:** API "active" status doesn't guarantee equipment exists.

**Stage 2: Year-Specific Equipment Failures (File Removal)**

- **Action:** Identified 104 combinations with complete year-long failures (2023: 41, 2024: 63)
- **Decision:** Removed 1,248 files representing systematic failures.
- **Result:** 8,709 → 6,179 files; 47.5% → 26.0% issue rate.
- **Learning:** Temporal analysis separates equipment failure from operational gaps.

**Stage 3: Cross-Year Consistency (ML Optimisation)**

- **Action:** Identified 53 combinations with temporal gaps across years.
- **Decision:** Removed 1,247 files (benefit ratio 1.54:1) to achieve 100% temporal consistency.
- **Result:** 6,179 → 4,932 files; 26.0% → 17.2% issue rate; 216 → 170 combinations.
- **Learning:** ML requires structural consistency, not just low issue rates.

**Final Validated Dataset:**

- 4,932 files (43.4% reduction from initial 8,709)
- 17.2% issue rate (63.8% improvement from initial 47.5%)
- 170 combinations across 78 sites with 100% cross-year temporal consistency
- Ready for robust time-series machine learning.

### 1.2 File Organisation

The final directory structure maintained clear separation between validated data and comprehensive quality documentation:

```
data/laqn/
├── optimised/                              # Clean validated data
│   ├── 2023_jan/ through 2023_dec/
│   ├── 2024_jan/ through 2024_dec/  
│   └── 2025_jan/ through 2025_nov/
│       (4,932 files total)
│
├── missing/                                # Quality audit trail
│   ├── removal_quality_report/             # Cross-year consistency validation
│   │   ├── healthy_files_to_remove.csv     # 490 healthy files (≤20% missing)
│   │   ├── perfect_files_to_remove.csv     # 83 perfect files (0% missing)
│   │   ├── unhealthy_files_to_remove.csv   # 757 unhealthy files (>20% missing)
│   │   └── removal_quality_summary.csv     # Benefit ratio and projections
│   │
│   ├── affected_sites_species_count.csv    # Month counts for temporal analysis
│   ├── logs_missing_value.csv              # Initial quality assessment (47.5% issue rate)
│   ├── logs_nan_value.csv                  # 2. quality status (36% issue rate -2876csv file)
│   ├── value_100filtered_missing.csv       # 100% missing files identification
│   ├── neg_val_siteSpecies.csv             # Negative values log
│   ├── notActive_site_species.csv          # 38 permanently non-active combinations
│   ├── notActive_siteSpecies_2023.csv      # 41 year-specific 2023 failures
│   ├── notActive_siteSpecies_2024.csv      # 63 year-specific 2024 failures
│   ├── notActive_siteSpecies_2025.csv      # 2025 status (empty - no failures)
│   ├── logs_rm_notActive_23_24.csv         # First removal audit (1,248 files)
│   └── logs_rm_notActive_2023_2024_2025.csv # Final removal audit (1,247 files)
│
├── optimised_siteSpecies.csv               # CURRENT: Validated metadata (163 combinations, 17.2% issue rate)
├── updated_actv_siteSpecies.csv            # Interim: Second validation (216 combinations, 26.0% issue rate)
├── actv_sites_species.csv                  # DEPRECATED: Original (252 combinations, 47.5% issue rate)
└── sites_species_london.csv                # Raw API response (252 combinations)
```

### 1.3 Key Files Reference

**Production files (use these):**

- `optimised_siteSpecies.csv`: Final validated metadata with 163 combinations, 17.2% issue rate.
- Files in `optimised/` directory: 4,932 validated measurement files with cross-year consistency.

**Interim files (documentation only):**

- `updated_actv_siteSpecies.csv`: Intermediate validation with 216 combinations after initial cleaning.
- `logs_rm_notActive_23_24.csv`: First removal targeting year-specific failures (1,248 files).

**Deprecated files (do not use):**

- `actv_sites_species.csv`: Original metadata containing 38 permanently non-active and 104 year-specific failures.

**Quality documentation (complete audit trail):**

- `notActive_site_species.csv`: 38 combinations missing all 35 months (metadata correction only).
- `notActive_siteSpecies_2023.csv`: 41 combinations with complete 2023 failure.
- `notActive_siteSpecies_2024.csv`: 63 combinations with complete 2024 failure.
- `removal_quality_report/`: Detailed breakdown of cross-year consistency removal by file quality.
- `logs_rm_notActive_2023_2024_2025.csv`: Final removal audit (1,247 files across all years).
- `logs_nan_value.csv`: Second quality status showing 2876 files  >20% missing (36%), 216 site/species.
- `logs_missing_val_updated.csv`: Current quality status showing 849 files with >20% missing (17.2%).

**Negative values documentation:**

- `neg_val_siteSpecies.csv`: Files containing negative pollution measurements (handled during preprocessing, not removal).

The directory structure provides complete traceability from initial collection (8,709 files) through two stages of cleaning (first: 6,179 files, final: 4,932 files) to the validated dataset ready for exploratory analysis.

## 2. Initial Dataset Assessment

### 2.1 Dataset Structure

TThe data collection phase produced 8,709 CSV files organised by month and stored in the `monthly_data` directory as the raw fetched version.

**Raw monthly_data directory column structure:**

```
@MeasurementDateGMT,@Value
```

For standardisation, each CSV file had the site code and date information extracted from filenames following the convention:

```
{SiteCode}_{SpeciesCode}_{StartDate}_{EndDate}.csv
```

The parsed CSV files with new column additions were saved to the `data/laqn/processed` directory. A `pollutant_std` column was added containing the standardised species code.

**Processed folder column structure:**

```
@MeasurementDateGMT,@Value,pollutant_std
```

To prepare the dataset for machine learning, I enriched each file with metadata from `actv_sites_species.csv` by matching on pollutant type and site code. The enrichment process added `SpeciesName`, `SiteName`, `SiteType`, `Latitude`, and `Longitude` to each file. The `pollutant_std` column was matched against `SpeciesCode` in the metadata, and the filename's site code (the part before the first underscore) was matched against the metadata's `SiteCode`. Upon successful matching, the geographic coordinates and descriptive fields were appended to each measurement record.

The optimised files were saved to the `optimised` directory. Each file represented one site-species combination for one month, following a standardised structure implemented during collection to facilitate downstream analysis and enable spatial joins with meteorological data.

**Optimised column structure:**

```
@MeasurementDateGMT,@Value,SpeciesCode,SiteCode,
SpeciesName,SiteName,SiteType,Latitude,Longitude
```

**Directory organisation:**

```
data/laqn/optimised/
├── 2023_jan/ through 2023_dec/    (12 months)
├── 2024_jan/ through 2024_dec/    (12 months)  
└── 2025_jan/ through 2025_nov/    (11 months)
```

### 2.2 Metadata Reference

The `actv_sites_species.csv` file served as my reference for which site-species combinations should exist in the dataset. This file was generated during the data collection phase by filtering the raw LAQN API response for sites where both `@DateClosed` and `@DateMeasurementFinished` were null, indicating currently operational monitoring.

**Metadata summary:**

- 252 site-species combinations.
- 84 unique monitoring sites.
- 6 pollutant types: NO₂, PM10, PM2.5, O₃, CO, SO₂.
- Geographic coverage: Greater London (51.31°N to 51.67°N, -0.46°W to 0.23°E).
- All sites managed by King's College London.

**Expected data volume:**

With 252 combinations across 35 months (12+12+11), I expected approximately 8,820 files if everything was working perfectly. The actual 8,709 files represented 98.7% of the theoretical maximum, which seemed reasonable given that not every combination might have started monitoring on 1 January 2023.

### 2.3 Raw Numbers

Before any quality assessment, the collected dataset contained:

- **Files:** 8,709
- **Total measurement records:** 6,085,344 hourly observations.
- **Temporal coverage:** January 2023 through November 2025 (35 months).
- **Spatial coverage:** 84 sites across all London boroughs.
- **Target pollutants for modelling:** CO, NO₂, O₃, PM10, PM2.5, SO₂ (6 pollutant for LAQN)

The whole volume initially looked promising. Over six million measurements should provide substantial data for building predictive models. However, volume alone doesn't guarantee quality, sadly learnt that shortly after quick quality tests functions.

## 3. First Quality Check

### 3.1 Building the Quality Assessment Function

I created `detailed_data_quality_analysis()` in the `laqn_check.ipynb` notebook to systematically inspect the entire dataset. The function needed to check multiple aspects of data quality while being detailed enough to catch problems I might not have anticipated.

**Quality dimensions assessed:**

- Empty files (no data rows).
- Missing required columns.
- Duplicate timestamps within files.
- Missing SiteCode or SpeciesCode identifiers.
- Data type validation.
- Missing values across all columns.
- High missing values threshold (>20% in @Value column).
- File format errors.

The 20% threshold for flagging files was deliberate. A few missing hours in a month of data is normal maintenance. But if more than 20% of values are missing, something more serious is likely wrong with the data availability.

### 3.2 The Result

**Initial quality assessment output:**

| Metric                         | Value |
| ------------------------------ | ----- |
| Files processed                | 8,709 |
| Files with >20% missing values | 4,136 |
| Issue rate                     | 47.5% |
| Empty files                    | 0     |
| Missing timestamps             | 0     |
| Missing site identifiers       | 0     |

Nearly half the dataset had serious quality problems. This was alarming. The file structure was fine (no corruption), the timestamps were present, the site codes were there. But the actual pollution measurements, the `@Value` column, had massive gaps in 47.5% of files.

**What I have after the first test:**

- File structure was sound (0 empty files, all required columns present).
- Temporal completeness was good (no missing timestamps).
- Spatial completeness was good (all site identifiers present)
- **Measurement completeness was severely compromised** (4,136 files flagged).

This pattern suggested the problem wasn't with my data collection code or file handling. The files were structurally perfect. The problem was that the sensors either weren't measuring or weren't reporting measurements.

### 3.3 Logging for Investigation

The first time I ran the function I created a file called `logs_missin_value.csv` and added all files with >20% missing values along with their detailed metadata.

The function saved all flagged files to ``logs_missin_value.csv` ` with detailed metadata:

```
filename, path, siteCode, SpeciesCode, year, month, EmptyValuePercentage
```

This log became essential for the investigation. I could see which combinations were problematic, identify patterns across time, and track whether issues were temporary (affecting one or two months) or permanent (affecting every single month).

## 4. Investigating 100% Missing Files

### 4.1 Isolating the Worst Cases

If 47.5% of files had problems, I needed to understand the severity distribution. Were most files missing 21% of values, or were many files completely empty?

I created a filtering function to extract files with 100% missing values from the quality log:

**Results:**

| Metric                  | Value |
| ----------------------- | ----- |
| Files with >20% missing | 4,136 |
| Files with 100% missing | 3,401 |
| Percentage              | 82.2% |

This was a crucial finding. Of the problematic files, 82% were completely empty. Not a single valid measurement. This suggested systematic equipment failure rather than intermittent sensor issues.

**Output:** `value_100filtered_missing.csv`

The 735 files with partial missing values (between 20-99% missing) likely represented genuine temporary failures, maintenance windows, or equipment being installed/decommissioned mid-month. The 3,401 files with 100% missing values needed deeper investigation.

### 4.2 The Key Question

Were these sensors temporarily broken, or did the equipment never exist in the first place?

A sensor that breaks in June but gets fixed in July would show 100% missing for June only. Equipment that doesn't exist would show 100% missing for every single month across all three years.

This distinction was critical. Temporary failures are normal in environmental monitoring and should be handled through imputation. Non-existent equipment represents a metadata error that needs correction.

## 5. Temporal Consistency Analysis

### 5.1 Methodology

I developed `analyse_affected_sites()` to group the 100% missing files by site-species combination and count how many months each combination appeared with no data.

**Analysis framework:**

- Load all 100% missing files.
- Extract month numbers (jan=1, feb=2, etc.).
- Group by (siteCode, SpeciesCode, year).
- Count months per combination per year.
- Create pivot table showing months missing by year.

**Critical thresholds:**

- 2023: 12 months (complete year).
- 2024: 12 months (complete year).
- 2025: 11 months (January through November only).

If a combination had 12 missing months in 2023 and 12 in 2024 and 11 in 2025, that's 35 consecutive months with zero measurements. At that point, the equipment clearly doesn't exist.

### 5.2 Discovering Non-Active Equipment

**Results from temporal analysis:**

| Finding                                         | Count |
| ----------------------------------------------- | ----- |
| Site-species combinations missing all 35 months | 38    |
| Unique sites affected                           | 29    |

**Output:** `notActive_site_species.csv`

These 38 combinations had perfect consistency in a bad way, empty. Not a single measurement in any month across nearly three years. This wasn't sensor failure; this was sensors that never existed despite being listed in the API metadata as "active."

**Examples of permanently non-active combinations:**

- **BL0** (Bloomsbury): Not monitoring any pollutant (CO, NO₂, O₃, PM10, PM2.5, SO₂ all missing).
- **WM0** (Westminster): Missing equipment for CO, O₃, PM10, SO₂ (but actively measuring NO₂ and PM2.5).
- **KF1** (North Kensington): No PM10 monitor (PM2.5 monitor exists).
- **MR8** (Marylebone Road): No PM2.5 monitor (PM10 monitor exists).

**Breakdown by pollutant type:**

| Pollutant | Sites Without Equipment |
| --------- | ----------------------- |
| CO        | 10                      |
| SO₂       | 10                      |
| PM10      | 9                       |
| O₃        | 4                       |
| PM2.5     | 2                       |
| NO₂       | 2                       |

The pattern made sense. CO and SO₂ monitors are expensive and less critical for London's current air quality priorities. NO₂ and PM2.5, the pollutants I needed for modelling, had better equipment coverage.

### 5.3 API Validation

I needed to confirm these findings were genuine and not an artefact of my data collection process. Using Postman, I manually tested several suspected non-active combinations directly against the LAQN API.

**Test example:**

```
GET https://api.erg.ic.ac.uk/AirQuality/Data/SiteSpecies/
    SiteCode=KF1/SpeciesCode=PM25/
    StartDate=2023-01-01/EndDate=2023-12-31/csv
```

**API response:**

```
MeasurementDateGMT,North Kensington FIDAS: PM2.5 Particulate (ug/m3)
2023-01-01 00:00,
2023-01-01 01:00,
2023-01-01 02:00,
...
```

Every single value was blank throughout the entire year. The API confirmed: this equipment doesn't exist. The metadata claiming it was "active" was incorrect.

## 6. Metadata Correction Strategy

### 6.1 Strategic Decision

I had two options for handling the 38 permanently non-active combinations:

**Option 1: Delete all empty files**
 Remove the 3,401 files with 100% missing values from the optimised directory. I initially tried this approach, and the issue rate dropped dramatically to 11%, which seemed excellent. I applied the same methodology to the DEFRA dataset and achieved a 0% issue rate, which was difficult to believe. Manual verification through Postman confirmed the DEFRA results were genuine their equipment genuinely had no failures.

This comparison made me reconsider the LAQN approach. The LAQN dataset was proving extremely problematic, and the API documentation was inaccurate, leading to incorrect assumptions about equipment status. Simply deleting files might obscure important information about what was actually collected versus what should have existed.

**Option 2: Keep files, correct metadata** Retain the empty files as evidence of what was collected, but remove the 38 non-active combinations from the reference metadata.

I went along with 2.nd option for reasons below:

**Preserves audit trail:** I can prove exactly what I collected and demonstrate the investigation process.

**Reversible:** If equipment gets installed later, I don't need to re-run data collection.

**Transparent:** Makes it clear what was excluded and why, supporting reproducibility.

**Maintains provenance:** Future researchers can see the decision chain.

**Best practice:** Separates "what exists" (files) from "what's valid" (metadata).

### 6.2 Removing Non-Active Combinations

I created `remove_nonactive_from_active()` to update the metadata:

1. Load original metadata: 252 combinations.
2. Load permanently non-active list: 38 combinations.
3. Remove non-active entries.
4. Handle species code normalisation (PM2.5 vs PM25)
5. Save validated metadata as `updated_actv_siteSpecies.csv`

**Results:**

| Metric                       | Value                |
| ---------------------------- | -------------------- |
| Original metadata            | 252 combinations     |
| Permanently non-active       | 38                   |
| Species normalisation        | 2 (PM2.5 ↔ PM25)     |
| **Final validated metadata** | **216 combinations** |
| Reduction                    | 14.3%                |

The two additional removals during species normalisation came from the API inconsistently using "PM2.5" versus "PM25" for the same pollutant. This caught KF1 and MR8 entries that had been missed in the initial filtering because of the naming mismatch.

**Critical file designation:**

- **DEPRECATED:** `actv_sites_species.csv` (original with 252 combinations).
- **USE THIS:** `updated_actv_siteSpecies.csv` (validated with 216 combinations).

All subsequent analysis must reference the validated metadata, not the original.

## 7. Year-Specific Failure Analysis

### 7.1 The Partial Failure Problem

The 35-month analysis caught equipment that never existed (38 combinations). But what about sensors that worked in 2023 but failed completely in 2024? Those wouldn't appear in the permanent non-active list because they had valid 2023 data.

I adapted the temporal analysis to run separately for each year, identifying combinations with 100% missing values for every month in that specific year only.

**Methodology:**

For each year (2023, 2024, 2025):

1. Filter 100% missing files to that year.
2. Group by site-species combination.
3. Count months with missing data.
4. Flag combinations with 12/12 months missing (11/11 for 2025).
5. Exclude combinations already in permanent non-active list.

### 7.2 Year-Specific Results and Pattern

**Equipment deterioration pattern:**

| Year | Complete Year Failures | Interpretation                    |
| ---- | ---------------------- | --------------------------------- |
| 2023 | 41                     | Initial equipment aging           |
| 2024 | 63                     | Peak failures (aging + budget?)   |
| 2025 | 0                      | Repairs completed, network stable |

The pattern suggested equipment reached end-of-life simultaneously, possibly due to batch installation years earlier or funding constraints preventing timely repairs. The 2025 recovery indicated successful maintenance or replacement.

**Output files:**

- **2023:** `notActive_siteSpecies_2023.csv` 41 new combinations with all 12 months missing
- **2024:**`notActive_siteSpecies_2024.csv`  63 new combinations with all 12 months missing (peak failure year)
-  **2025:**`notActive_siteSpecies_2025.csv` 0 new combinations (network stabilised)

## 8. Year-Specific File Removal

### 8.1 Removal Logic

**Removal categories:**

| Category             | Count | Decision                             |
| -------------------- | ----- | ------------------------------------ |
| Permanent non-active | 38    | Metadata correction only, files kept |
| 2023 year failures   | 41    | Remove files (no measurements)       |
| 2024 year failures   | 63    | Remove files (no measurements)       |

Year-specific failures provided no value—zero measurements that wouldn't retroactively start working. They inflated storage and contaminated quality metrics.

### 8.2 Implementation

**Function created:** `rm_files_notactive()` with safety features:

- Dry run mode for verification.
- Complete audit logging before deletion.
- Metadata preservation (site, species, month, path).
- Reversibility through comprehensive logs.

**Execution:**

| Stage          | Files         | Result                                    |
| -------------- | ------------- | ----------------------------------------- |
| Dry run        | 1,248 flagged | Verified: no 2025 files, correct matching |
| Actual removal | 1,248 deleted | Zero errors                               |
| Audit log      | Complete      | `logs_rm_notActive_23_24.csv`             |

## 9. Post-Removal Quality Assessment

### 9.1 Quality Improvement Achieved

**Metrics evolution:**

| Metric                       | Initial   | After Removal | Change      | % Improvement     |
| ---------------------------- | --------- | ------------- | ----------- | ----------------- |
| Total files                  | 8,709     | 6,179         | -2,530      | -29.1%            |
| Files with >20% missing      | 4,136     | 1,606         | -2,530      | -61.2%            |
| **Issue rate**               | **47.5%** | **26.0%**     | **-21.5pp** | **-45% relative** |
| Measurement records          | 6.09M     | 4.31M         | -1.78M      | -29.2%            |
| Complete measurements (est.) | 3.19M     | 3.19M         | -7,300      | -0.2%             |

**Key insight:** Issue rate dropped 45% while losing only 0.2% of complete measurements. The removal surgically targeted empty files, preserving genuine data.

### 9.2 Nature of Remaining 26% Issues

The remaining 26% represents normal operational conditions, not non-existent equipment:

| Issue Type            | Estimated % | Cause                                        |
| --------------------- | ----------- | -------------------------------------------- |
| Temporary failures    | 6-10%       | Equipment breaks, gets repaired within weeks |
| Scheduled maintenance | 8-12%       | Calibration, filter changes, sensor cleaning |
| Transmission problems | 3-5%        | Network issues, API timeouts                 |
| Calibration periods   | 2-4%        | Quality control requiring equipment offline  |
| Environmental impacts | 1-3%        | Weather damage, power interruptions          |

This inherent messiness can be handled through time-series imputation. It's fundamentally different from equipment that doesn't exist.

### 9.3 The Temporal Inconsistency Problem

**What was removed:**

- 38 permanently non-active (metadata corrected, files kept).
- 104 year-specific failures (1,248 files deleted from specific years).

**What remained:**

- 216 validated combinations.
- 6,179 files with genuine measurements.
- 1,606 files with 20-99% missing (operational gaps).

**Critical realisation:** Year-based removal created temporal fragmentation. Some combinations had files in 2023 and 2025 but nothing in 2024. This breaks machine learning:

- **Can't compute year-over-year changes:** Missing full years prevent seasonal evolution analysis.
- **Feature engineering unreliable:** Lag features and rolling averages break at year boundaries.
- **Cross-validation problematic:** Can't create robust temporal train/test splits.
- **Prediction coverage limited:** Models can only predict for combinations in training data.

This led directly to Section 10's cross-year consistency analysis.

## 10. Cross-Year Consistency Optimisation

### 10.1 The Machine Learning Problem

The 26% issue rate looked good statistically, but the dataset structure was unsuitable for time-series modelling due to temporal gaps.

**Problem examples:**

- HG1/PM2.5: Data in 2023 and 2025, missing all of 2024.
- GR4/O₃: Excellent 2024 data, nothing in 2023.

**ML impacts:**

- Temporal patterns fragmented (can't learn seasonal evolution).
- Cross-validation impossible (inconsistent coverage across folds).
- Feature engineering unreliable (lag features break at gaps).
- Prediction coverage reduced (can only predict trained combinations).

### 10.2 Gap Analysis

**Approach:**

1. Combined all year-specific failures (2023: 41, 2024: 63, 2025: 0 = 104 total).
2. Scanned optimised directory for files from these 104 combinations.
3. Found 53 combinations still had files despite year failures.

**Key finding:** Initial removal only deleted files within specific failure years. A combination that failed in 2024 might still have 2023/2025 files present, creating temporal gaps.

| Discovery                              | Value |
| -------------------------------------- | ----- |
| Combinations with remaining files      | 53    |
| Affected files                         | 1,247 |
| Percentage of current dataset          | 20.2% |
| Already fully removed (from Section 8) | 51    |

### 10.3 Decision Framework

**Quality distribution of 1,247 affected files:**

| Quality Level | Count | % of Removal | Description  |
| ------------- | ----- | ------------ | ------------ |
| Unhealthy     | 757   | 60.71%       | >20% missing |
| Healthy       | 490   | 39.29%       | ≤20% missing |
| Perfect       | 83    | 6.66%        | 0% missing   |

**Benefit ratio: 1.54:1** — For every 1 healthy file removed, 1.54 unhealthy files eliminated.

**Trade-off analysis:**

 **For removal:**

- Majority (60.71%) already problematic.
- Positive benefit ratio (removes more bad than good).
- 8.78pp improvement (26.0% → 17.2%).
- 100% temporal consistency for ML.
- All 53 had documented year-long failures.

**Against removal:**

- Loses 490 healthy + 83 perfect files.
- Reduces combinations 24.5% (216 → 170).
- 20.2% data reduction.
- Irreversible.

**Decision:** Proceed. The 1.54:1 ratio and ML consistency requirements justified sacrificing some healthy data.

### 10.4 Implementation and Outcomes

**Process:**

1. Generated quality logs categorising all 1,247 files.
2. Created dry-run preview for verification.
3. Executed removal with complete audit trail.
4. Updated metadata to 17 unique combinations.

**Audit trail:**

- `removal_quality_report/healthy_files_to_remove.csv` (490).
- `removal_quality_report/perfect_files_to_remove.csv` (83).
- `removal_quality_report/unhealthy_files_to_remove.csv` (757).
- `removal_quality_report/removal_quality_summary.csv` (benefit analysis).
- `logs_rm_notActive_2023_2024_2025.csv` (complete log).

**Results:**

| Metric                 | Before  | After | Change  |
| ---------------------- | ------- | ----- | ------- |
| Files                  | 6,179   | 4,932 | -1,247  |
| Issue rate             | 26.0%   | 17.2% | -8.78pp |
| Combinations           | 216     | 170   | -46     |
| Cross-year consistency | Partial | 100%  | -       |

**Validation:** The projected 17.2% issue rate was confirmed exactly. All 170 combinations now have either complete 35-month coverage or are excluded entirely—100% temporal consistency achieved for time-series machine learning.



## 11. Final Quality Assessment

### 11.1 Re-Running Quality Checks After Cross-Year Optimisation

After the cross-year consistency removal, I ran `detailed_data_quality_analysis()` a third time to confirm the projected improvements materialised.

**Complete quality metrics evolution:**

| Metric                       | Initial   | After First Cleaning(metadata& year based removal) | After Cross-Year Optimisation | Total Change |
| ---------------------------- | --------- | -------------------------------------------------- | ----------------------------- | ------------ |
| Files processed              | 8,709     | 6,179                                              | **4,932**                     | -3,777       |
| Files with >20% missing      | 4,136     | 1,606                                              | **849**                       | -3,287       |
| **Issue rate**               | **47.5%** | **26.0%**                                          | **17.2%**                     | **-30.3pp**  |
| Total measurement records    | 6,085,344 | 4,307,352                                          | **3,442,656**                 | -2,642,688   |
| Complete measurements (est.) | 3,194,780 | 3,187,441                                          | **2,851,319**                 | -343,461     |
| Active combinations          | 252       | 216                                                | **163**                       | -89          |



### 11.2 Understanding the Final 17.2% Issue Rate

The remaining 849 files with >20% missing values (17.2% issue rate) represent genuinely temporary operational issues rather than equipment that doesn't exist or year-long failures:

**Temporary sensor failures (estimated 4-6%):** Equipment breaks and gets repaired within days or weeks. Missing measurements during repair windows, but equipment returns to service within the same month.

**Scheduled maintenance (estimated 5-7%):** Regular calibration, filter changes, sensor cleaning. Planned downtime with expected gaps, typically scheduled 2-4 times per year per sensor.

**Data transmission problems (estimated 2-4%):** Network issues, API timeouts, upload failures. Measurement happens but doesn't reach the database. Often resolved within hours.

**Calibration periods (estimated 1-3%):** Quality control checks requiring equipment offline. Essential for data accuracy, typically 1-2 day windows.

**Environmental conditions (estimated 1-2%):** Weather impacts (extreme cold damaging sensors), temporary power interruptions, physical damage requiring quick repairs.

This 17.2% represents the inherent operational variance in real-world environmental monitoring. It's fundamentally different from:

- Equipment that never existed (38 combinations removed via metadata correction).
- Equipment with year-long failures (104 combinations removed initially).
- Equipment with cross-year inconsistency (53 combinations removed for ML consistency).

## 12. Handling Negative Values

### 12.1 Discovery of Negative Measurements

The quality assessment function flagged another issue I hadn't anticipated: negative pollution measurements. This made no physical sense. You can't have negative concentrations of particulate matter or gas molecules in air.

**Findings in final dataset:**

| Metric                     | Value                 |
| -------------------------- | --------------------- |
| Files with negative values | 1,089 (22.1%)         |
| Total negative readings    | 16,847                |
| Negative value rate        | 0.49% of measurements |

After the cross-year consistency removal, 22.1% of files contained some negative values, though the 16,847 readings represented less than 0.5% of the 3.4 million total measurements.

### 12.2 Investigating the Pattern

I examined examples from the negative value log:

```
BG2_PM10_2023-08-01_2023-08-31.csv: [-3.5, -4.0, -1.5, -8.3, ...]
```

The negative values were consistently small in absolute magnitude (typically between -1 and -10 µg/m³). They appeared sporadically throughout files rather than in clusters. This pattern suggested sensor calibration drift rather than fundamental equipment failure.

**Hypotheses for negative values:**

**Sensor baseline drift:** Sensors measure relative to a baseline. If the baseline calibration drifts upward slightly, very clean air might register as slightly negative.

**Signal noise at detection limit:** For very low pollution levels, measurement noise can produce small negative values around the sensor's detection limit.

**Temperature compensation errors:** Sensors apply temperature corrections to raw measurements. Errors in the correction algorithm might occasionally produce negative adjusted values.

### 12.3 Handling Decision

I decided to keep files with negative values rather than remove them for three reasons:

**Tiny percentage:** 16,847 negatives out of 3.4 million measurements is 0.49%. Not significant enough to warrant file removal. (Also back of my head the first issue rate was 47%, so 21% is tiny)

**Correctable:** Negative values can be handled during preprocessing (set to zero, small positive constant, or interpolated from surrounding values).

**Information preservation:** Patterns of when negatives occur might be informative. Removing files loses that diagnostic information.

**Standard practice:** Environmental monitoring literature commonly reports handling negative values through preprocessing rather than removal.

**Already improved:** The cross-year consistency removal eliminated 4,286 negative readings that were in the removed files, improving the negative value situation without specifically targeting it.

The negative values will be addressed during the feature engineering phase of modelling, not during data preparation.

## 13. Final Dataset Characteristics

### 13.1 Clean Dataset Summary

After all quality assessment and cleaning operations, the final validated dataset comprised:

After all quality assessment and cleaning operations, the final validated dataset comprised:

| Characteristic                | Value                                                        |
| ----------------------------- | ------------------------------------------------------------ |
| Files                         | 4,932                                                        |
| Temporal coverage             | January 2023 - November 2025 (35 months)                     |
| Validated combinations        | 170 (173 with 3 duplicates in metadata)                      |
| Unique monitoring sites       | 78                                                           |
| Pollutant types               | 6 (NO₂, PM10, PM2.5, O₃, CO, SO₂)                            |
| Total measurement records     | 3,442,656                                                    |
| Complete measurements (82.8%) | ~2,851,319                                                   |
| Partial measurements (17.2%)  | ~591,337                                                     |
| Geographic coverage           | All London boroughs                                          |
| Cross-year consistency        | 100% (all combinations present all years or absent all years) |

**Note on metadata:** The `optimased_siteSpecies.csv` file contains 173 rows, but includes 3 duplicate combinations (GR8-PM10, HG1-NO2, HV3-NO2 appear twice). The unique combination count is **170**. All subsequent analysis uses the deduplicated count.

### 13.2 Distribution by Pollutant

The 170 unique validated combinations with cross-year consistency were distributed across pollutants as follows:

| Pollutant | Combinations | Percentage | Change from Initial |
| --------- | ------------ | ---------- | ------------------- |
| NO₂       | 58           | 34.1%      | -10 combinations    |
| PM2.5     | 53           | 31.2%      | -10 combinations    |
| PM10      | 42           | 24.7%      | -9 combinations     |
| O₃        | 11           | 6.5%       | -3 combinations     |
| SO₂       | 4            | 2.4%       | -1 combination      |
| CO        | 2            | 1.2%       | -1 combination      |

The two target pollutants for predictive modelling, NO₂ and PM2.5, represented 65.3% of the validated combinations (111 out of 170). This concentration substantially exceeds the initial planning target and provides excellent coverage for the research objectives.

**Key observations:**

- NO₂ maintained the highest representation (34.1%), ensuring robust NO₂ model development
- PM2.5 achieved strong representation (31.2%), the highest proportion among all pollutants
- Combined NO₂ and PM2.5 account for nearly two-thirds of all validated combinations
- All six pollutant types retained sufficient representation for exploratory analysis
- The distribution shift towards PM2.5 during cleaning was fortunate, as it's the more health-critical pollutant

### 13.3 Temporal Completeness by Pollutant

The cross-year consistency optimisation ensured that all 170 combinations have measurements across all three years (or are excluded entirely):

| Pollutant | 2023 Coverage | 2024 Coverage | 2025 Coverage | Consistency |
| --------- | ------------- | ------------- | ------------- | ----------- |
| NO₂       | 58/58         | 58/58         | 58/58         | 100%        |
| PM2.5     | 53/53         | 53/53         | 53/53         | 100%        |
| PM10      | 42/42         | 42/42         | 42/42         | 100%        |
| O₃        | 11/11         | 11/11         | 11/11         | 100%        |
| SO₂       | 4/4           | 4/4           | 4/4           | 100%        |
| CO        | 2/2           | 2/2           | 2/2           | 100%        |

This 100% cross-year consistency was the primary objective of the extended analysis and was successfully achieved. Every validated combination has files present in all 35 months (12+12+11), eliminating the temporal fragmentation that would have complicated machine learning model training.

### 13.4 Spatial Coverage

The validated dataset covers 78 unique monitoring sites, down from the original 84 sites:

**Site reduction analysis:**

- Original sites: 84
- Sites completely removed: 6 (equipment never existed or all combinations failed)
- Sites partially retained: 78 (at least one validated combination)
- Site retention rate: 92.9%

**Borough representation:**

The 78 sites provide coverage across all major London boroughs with improved density compared to the interim 67-site dataset:

- Central London: High density maintained (Westminster, Camden, City of London)
- Inner London: Excellent coverage (Tower Hamlets, Islington, Hackney)
- Outer London: Good coverage with reduced gaps in peripheral boroughs

**Site type distribution:**

| Site Type        | Count | Percentage |
| ---------------- | ----- | ---------- |
| Roadside         | 94    | 54.3%      |
| Urban Background | 36    | 20.8%      |
| Suburban         | 19    | 11.0%      |
| Kerbside         | 18    | 10.4%      |
| Industrial       | 6     | 3.5%       |

The roadside concentration (54.3%) is appropriate for the research objectives. Roadside sites measure the highest pollution exposure relevant for public health modelling and traffic-related air quality assessment. The distribution represents real-world monitoring priorities rather than a data quality flaw.

### 13.5 Quality Improvement Summary

The three-stage cleaning process achieved progressive improvements:

| Stage                         | Files  | Issue Rate | Combinations | Key Achievement                  |
| ----------------------------- | ------ | ---------- | ------------ | -------------------------------- |
| Initial collection            | 8,709  | 47.5%      | 252          | Comprehensive data gathering     |
| After permanent non-active    | 8,709  | 47.5%      | 216          | Metadata correction              |
| After year-specific removal   | 6,179  | 26.0%      | 216          | Removed systematic failures      |
| After cross-year optimisation | 4,932  | 17.2%      | 170          | Ensured ML temporal consistency  |
| **Total improvement**         | -3,777 | -30.3pp    | -82          | Systematic to operational issues |

**Relative improvement:**

- Issue rate reduced by 63.8% (from 47.5% to 17.2%).
- Files reduced by 43.4% (from 8,709 to 4,932).
- Combinations reduced by 32.5% (from 252 to 170).

The substantial file and combination reduction was a deliberate trade-off to achieve:

1. High data quality (17.2% issue rate approaching best-practice standards).
2. Temporal consistency (essential for time-series machine learning).
3. Clear separation of systematic vs operational issues.
4. Positive benefit ratio throughout (always removing more bad data than good data).

## 14. Reproducibility Documentation

### 14.1 Analysis Notebook Structure

The data preparation process was documented across three Jupyter notebooks, each with a specific purpose:

**`laqn_exploration.ipynb`:** Initial data discovery and structure analysis. Examined the raw collected dataset to understand composition, missing patterns, and distribution characteristics.

**`laqn_check.ipynb`:** Primary quality assessment. Implemented `detailed_data_quality_analysis()` function and generated quality logs for investigation.

**`laqn_update.ipynb`:** Complete removal implementation. Contained temporal consistency analysis, permanent non-active identification, year-specific failure analysis, cross-year consistency analysis, and both removal operations with comprehensive audit logging.

**Note on notebook consolidation:** The original `laqn_remove.ipynb` notebook functionality was integrated into `laqn_update.ipynb` during the extended analysis phase. All removal operations and temporal analyses are now centrally located in `laqn_update.ipynb` for better workflow coherence.

### 14.2 Key Functions Created

**`detailed_data_quality_analysis()`** Comprehensive quality checker assessing empty files, missing columns, duplicate timestamps, data type validation, missing values threshold (>20%), and negative values. Produces detailed logs with percentage breakdowns for investigation.

**`filter_missing_pollutants()`** Filtered quality logs to isolate 100% missing files and normalised species codes (PM2.5 vs PM25) for consistent matching across datasets.

**`analyse_affected_sites()`** Temporal consistency analysis grouping by site-species-year and counting missing months to identify permanent failures (35/35 months) and year-specific failures (12/12 or 11/11 months).

**`remove_nonactive_from_active()`** Metadata correction removing permanently non-active combinations (38) from reference file with species normalisation handling. Generated first validated metadata with 216 combinations.

**`rm_files_notactive()`** Safe file removal with dry run mode, comprehensive logging, and metadata preservation. Used in two stages:

- Stage 1: Removed 1,248 year-specific failure files (2023 and 2024)
- Stage 2: Removed 1,247 cross-year inconsistency files (all years)

**`analyse_cross_year_consistency()`** Extended temporal analysis identifying site-species combinations with year-specific failures that still had files present in other years. Calculated benefit ratios and projected impact metrics for cross-year optimisation decision-making.

**`categorise_files_by_quality()`** Quality categorisation function separating affected files into healthy (≤20% missing), unhealthy (>20% missing), and perfect (0% missing) categories. Enabled benefit ratio calculation and transparent removal decision documentation.

### 14.3 Dependencies

Python libraries used throughout data preparation:

- pandas 2.0.3: Data manipulation and analysis
- numpy 1.25.2: Numerical operations and percentage calculations
- pathlib: Cross-platform path handling for file operations
- re: Regular expressions for filename parsing (site code, species code, date extraction)
- datetime: Temporal operations and month extraction for temporal consistency analysis
- os: File system operations for removal and directory management

All code is available in the project repository with detailed inline documentation explaining the logic and decisions at each step. Every function includes parameter descriptions, return value documentation, and usage examples.

## 15. Lessons Learned, Reflections and Summary

### 15.1 API Metadata Doesn't Guarantee Equipment Exists

The most significant discovery was that the LAQN API lists sites based on administrative status rather than actual equipment deployment. A site can be listed as "active" in the metadata while having no physical sensors installed. This isn't malicious; it likely reflects administrative records (site approved, funding allocated) being created before physical installation.

Comparing LAQN with DEFRA was enlightening. DEFRA achieved 0% issue rate because their metadata accurately reflected deployed equipment. LAQN's 47.5% initial issue rate revealed that their "active" status was unreliable.

**Learning:** Always validate metadata empirically. Check for actual measurements; don't trust the API's claim that something is "active" without verification.

### 15.2 Multi-Year Temporal Analysis is Effective

The 35-month temporal consistency check successfully separated three distinct problems that appeared similar initially:

- Equipment that never existed (38 combinations, all 35 months missing).
- Equipment that failed for entire years (104 combinations, 12/12 months missing in specific years).
- Normal operational gaps (17.2% of final data, scattered missing periods).

**Learning:** Temporal patterns reveal the nature of data quality problems. Time-series consistency checks are more informative than point-in-time quality statistics.

### 15.3 Metadata Correction Beats File Deletion for Permanent Issues

Keeping the permanently non-active files (38 combinations) while correcting the metadata was the right choice. It preserved the complete audit trail, made the analysis reversible if equipment status changes, and maintained transparency about what was excluded and why.

**Learning:** Separating "what was collected" (files) from "what's valid" (metadata) provides better documentation and scientific rigour than deleting problematic data.

### 15.4 Cross-Year Consistency Matters for Machine Learning

The extended analysis revealed that achieving a good issue rate (26%) wasn't sufficient for machine learning applications. Temporal consistency across years proved equally important:

**Without cross-year consistency:**

- 216 combinations, 26% issue rate
- Fragmented temporal coverage (some years missing for many combinations)
- Difficult feature engineering (lag features, rolling averages unreliable)
- Limited cross-validation options (can't stratify by year effectively)

**With cross-year consistency:**

- 170 combinations, 17.2% issue rate
- Complete temporal coverage for all validated combinations
- Reliable feature engineering across all time windows
- Robust cross-validation possibilities (can split by year confidently)

**Learning:** Data preparation for machine learning requires thinking beyond quality metrics to structural requirements like temporal consistency. The 20.2% additional data removal was justified by the substantial improvement in dataset usability for time-series modelling.

### 15.5 Benefit Ratio Provides Objective Decision Framework

The benefit ratio calculation (1.54 unhealthy files removed per 1 healthy file removed) provided an objective framework for the difficult decision to remove additional data in the cross-year optimisation. Before this analysis, the decision was subjective. After quantifying the trade-off, the evidence clearly supported removal.

**Learning:** Quantifying trade-offs through benefit ratios transforms difficult subjective decisions into evidence-based choices. This approach could be applied to other data cleaning decisions where removal affects both good and bad data.

### 15.6 The Iterative Investigation Process

My approach evolved significantly through multiple stages:

1. Identified 47.5% issue rate (initial shock).
2. Found 3,401 files with 100% missing values.
3. Nearly deleted them all immediately (would have been wrong).
4. Tested immediate deletion, achieved 11% issue rate (seemed too good).
5. Compared with DEFRA dataset (0% issue rate, genuinely accurate).
6. Reconsidered: LAQN problems reflect API inaccuracy, not just sensor failures.
7. Ran temporal consistency analysis (breakthrough moment).
8. Decided on metadata correction instead of deletion for permanent non-active.
9. Conducted year-specific analysis to catch partial failures.
10. Removed only confirmed year-specific files (26% issue rate achieved).
11. Realised year-specific removal created cross-year inconsistency.
12. Developed cross-year consistency analysis.
13. Calculated benefit ratio (1.54:1) to justify additional removal.
14. Removed additional 1,247 files (17.2% issue rate achieved).
15. Confirmed 100% temporal consistency across all validated combinations.

**Learning:** Being willing to reconsider when new insights emerged was critical to reaching the right solution. The initial instinct to delete everything would have been wrong. Premature satisfaction with 26% issue rate would have left structural problems for modelling. Iterative refinement based on evolving understanding produced the best outcome.

### 15.7 Documentation Pays Off

Creating detailed logs at every stage proved invaluable. The audit trail allowed me to:

- Trace the chain of reasoning from initial problem to final solution.
- Verify decisions were data-driven rather than intuitive.
- Provide evidence for why specific files were removed.
- Support reproducibility for future researchers.
- Write this dissertation chapter with specific numbers and examples.
- Reconsider decisions based on new insights without losing earlier work.

**Learning:** Time spent on documentation during analysis is time saved during writing. Keep detailed logs of every decision and its rationale. The three-stage removal process would have been impossible to explain clearly without comprehensive logs at each stage.

### 15.8 Quality Metrics Alone Don't Tell the Full Story

The journey from 47.5% to 26% to 17.2% issue rate demonstrates that a single quality metric doesn't capture all aspects of data fitness for purpose:

**26% issue rate looked acceptable:**

- Better than many real-world environmental datasets
- Substantial improvement from initial 47.5%
- Within acceptable range for operational monitoring

**But structural problems remained:**

- Temporal inconsistency across years
- Fragmented coverage preventing robust feature engineering
- ML training complications from cross-year gaps

**17.2% issue rate achieved both:**

- High measurement quality
- Temporal structural consistency

**Learning:** Always consider domain-specific requirements (like machine learning temporal consistency) alongside general quality metrics. What constitutes "clean enough" depends on the intended use case, not just the percentage of complete measurements.

### 15.9 Summary: From Chaos to Validated Dataset

This data preparation phase transformed a problematic dataset into a validated foundation for predictive modelling through systematic three-stage cleaning:

**Final achievements:**

- 4,932 validated files (43.4% reduction from initial 8,709)
- 17.2% issue rate (63.8% relative improvement from initial 47.5%)
- 170 confirmed active combinations (32.5% reduction from the initial 252)
- 78 unique monitoring sites (92.9% retention from initial 84)
- 100% temporal consistency for machine learning applications

The process required iterative refinement, careful decision-making about metadata correction versus file deletion, benefit ratio analysis to justify trade-offs, and thorough documentation to support reproducibility. The resulting validated dataset provides a solid foundation for developing robust time-series predictive models of London air quality while acknowledging the limitations and biases inherent in the monitoring network.