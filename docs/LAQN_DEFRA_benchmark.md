#  LAQN vs DEFRA Air Quality Dataset Benchmark

This benchmark evaluates two air quality monitoring datasets for use in London air pollution analysis. The aim is to identify which dataset is more suitable for different research objectives based on spatial coverage, pollutant diversity, data quality and practical usability.

Both datasets cover January 2023 to November 2025 (35 months) and monitor air pollution across Greater London.

**LAQN (London air quality network):** Operated by Imperial College London through the Environmental Research Group. Data accessed via the LAQN API at api.erg.ic.ac.uk.

**DEFRA (Department for Environment, Food and Rural Affairs):** Part of the automatic urban and rural network (AURN), the UK national monitoring network. Data accessed via the UK Air archive API.

## Evaluation criteria

The datasets are compared against five criteria relevant to air quality research.

| Criteria            | Description                                         |
| ------------------- | --------------------------------------------------- |
| Spatial coverage    | Number of monitoring stations and geographic spread |
| Pollutant diversity | Range of pollutants measured                        |
| Data completeness   | Percentage of valid measurements                    |
| Data quality        | Consistency of collection and ease of validation    |
| Usability           | Time required for cleaning and preparation          |

## 1. Spatial coverage

| Metric                         | LAQN                | DEFRA                 |
| ------------------------------ | ------------------- | --------------------- |
| Number of monitoring stations  | 78                  | 18                    |
| Station pollutant combinations | 141                 | 141                   |
| Geographic focus               | All London boroughs | Selected London sites |

LAQN provides broader spatial coverage with stations distributed across all London boroughs. This density allows analysis of local variations between areas such as roadside versus background locations or differences between inner and outer London.

DEFRA stations are fewer but form part of the national network. These stations follow standardised siting criteria and measurement protocols which makes them suitable for comparisons with other uk cities.

**Assessment:** LAQN is stronger for spatial analysis within London. DEFRA is stronger for national comparisons.

## 2. Pollutant diversity

| Dataset | Number of pollutants | Pollutants measured                                      |
| ------- | -------------------- | -------------------------------------------------------- |
| LAQN    | 6                    | NO2, PM10, PM2.5, O3, SO2, CO                            |
| DEFRA   | 37                   | Regulatory pollutants plus 31 volatile organic compounds |

LAQN measures the six primary regulatory pollutants which are sufficient for compliance checking and health impact studies focused on common urban pollutants.

DEFRA monitors a wider range, including benzene, toluene, ethylbenzene and xylene isomers (BTEX compounds) plus various alkanes and alkenes. However, only two stations (London Eltham and London Marylebone Road) monitor these volatile organic compounds. Unfortunately, the UK does not have any mandatory policies regarding these pollutant levels, which makes it more difficult to evaluate and plan for the future.

**Assessment:** DEFRA is stronger for source distribution and VOC analysis. LAQN is sufficient for regulatory pollutant studies.

## 3. Data completeness

| Metric                    | LAQN      | DEFRA     |
| ------------------------- | --------- | --------- |
| Total hourly measurements | 3,446,208 | 2,525,991 |
| Data completeness         | 87.13%    | 91.18%    |
| Missing values            | 12.87%    | 8.82%     |
| Total files               | 4,932     | 3,563     |

DEFRA achieves higher data completeness at 91.18% compared to 87.13% for LAQN. The missing data in DEFRA is clearly flagged using standardised codes where -99 indicates station maintenance or calibration and -1 indicates other invalid data or insufficient capture.

LAQN raw data contained approximately 47% missing values before cleaning. After validation and removal of inactive station pollutant combinations the completeness improved to 87.13%. This required significant processing time.

### Missing data by pollutant

| Pollutant        | LAQN missing | DEFRA missing |
| ---------------- | ------------ | ------------- |
| Nitrogen dioxide | 10.50%       | 7.82%         |
| PM10             | 12.35%       | 16.54%        |
| PM2.5            | 17.17%       | 12.62%        |
| Ozone            | 17.54%       | 14.02%        |
| Sulphur dioxide  | 16.15%       | 9.85%         |
| Carbon monoxide  | 9.18%        | 6.34%         |

Missing data patterns vary by pollutant. LAQN has lower missing rates for PM10 while DEFRA has lower rates for most other pollutants. Ozone and PM2.5 show higher gaps in both datasets which reflects the technical complexity of measuring these pollutants.

**Assessment:** DEFRA is stronger for data completeness and quality flagging. LAQN requires more preprocessing.

## 4. Data quality and consistency

Chi-square testing assessed whether data collection was evenly distributed across the study period.

| Dataset | Chi square statistic | P value | Interpretation       |
| ------- | -------------------- | ------- | -------------------- |
| LAQN    | 0.0035               | 0.9983  | Uniform distribution |
| DEFRA   | 65.76                | 0.0000  | Uneven distribution  |

LAQN showed consistent file counts across months with observed values matching expected values almost exactly. This indicates stable network operation without systematic gaps.

DEFRA showed uneven distribution with some months having more or fewer files than expected. This may reflect stations starting or stopping reporting or changes in the monitoring programme during the study period.

**Assessment:** LAQN is stronger for temporal consistency. DEFRA requires attention to monthly variations.

## 5. Usability and preparation time

| Factor             | LAQN                            | DEFRA                  |
| ------------------ | ------------------------------- | ---------------------- |
| Raw data quality   | Required extensive cleaning     | Cleaner initial state  |
| Metadata accuracy  | Contained inactive combinations | Accurate combinations  |
| Quality flags      | Not standardised                | Standardised (-99, -1) |
| Preparation effort | High (double time spent)        | Moderate               |

LAQN data required significant effort to validate. The metadata contained station pollutant combinations that were no longer active which meant fetching empty or partial datasets. Approximately double the time was spent on cleaning and validation compared to DEFRA.

DEFRA data appeared clean on first inspection with no empty values. The negative flags (-99 and -1) initially looked like measurement errors but investigation revealed these are standardised quality markers indicating maintenance periods or data capture issues.

**Assessment:** DEFRA is stronger for ease of use. LAQN requires more preparation time, but the effort is manageable once the cleaning pipeline is established.

## 6. Annual mean concentrations

Both datasets show similar pollution trends, which provides confidence in data quality.

| Pollutant | LAQN 2023 | DEFRA 2023 | LAQN 2024 | DEFRA 2024 | LAQN 2025 |
| --------- | --------- | ---------- | --------- | ---------- | --------- |
| NO2       | 24.92     | 21.95      | 22.78     | 20.35      | 22.19     |
| PM10      | 16.69     | 13.82      | 16.32     | 11.80      | 18.94     |
| PM2.5     | 8.81      | 8.16       | 8.42      | 7.00       | 10.63     |
| Ozone     | 46.28     | 45.62      | 47.38     | 44.88      | 49.73     |

All values are in micrograms per cubic metre. Nitrogen dioxide decreased over the study period in both datasets. Ozone increased in both datasets. The absolute differences between datasets reflect different monitoring locations rather than measurement errors. LAQN values are slightly higher, which may reflect greater coverage of roadside and urban centre locations.

## Summary of assessments

| Criteria             | Stronger dataset |
| -------------------- | ---------------- |
| Spatial coverage     | LAQN             |
| Pollutant diversity  | DEFRA            |
| Data completeness    | DEFRA            |
| Temporal consistency | LAQN             |
| Usability            | DEFRA            |

## Conclusion

Neither dataset is universally superior. The choice depends on research objectives.

**Use LAQN when:**

- Analysing spatial variations across London boroughs
- Comparing roadside versus background locations
- Studying local pollution hotspots
- Temporal consistency is important

**Use DEFRA when:**

- Comparing London with other uk cities
- Analysing volatile organic compounds
- Source apportionment studies
- Minimising data preparation time

**Use both datasets when:**

- Cross validating findings.
- Combining spatial coverage with pollutant diversity.
- Building comprehensive air quality models.

For machine learning applications both datasets can be used together. LAQN provides spatial density while DEFRA provides pollutant breadth. The similar trends in shared pollutants confirm that combining datasets is feasible after appropriate harmonisation.

## References

European Environment Agency (no date) Vocabulary: observation validity, Data dictionary. Available at: https://dd.eionet.europa.eu/vocabulary/aq/observationvalidity (Accessed: 15 December 2025).

Reddy, M.S. (2023) 'Chi-square test and its utility in forest ecology studies', Journal of global ecology and environment, 17(1), pp. 1-5. Available at: https://doi.org/10.56557/jogee/2023/v17i18020 (Accessed: 15 December 2025).

UK Air (no date) National air quality objectives. Available at: https://uk-air.defra.gov.uk/assets/documents/National_air_quality_objectives.pdf (Accessed: 15 December 2025).