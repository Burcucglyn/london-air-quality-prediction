# Random Forest Benchmark Report

## DEFRA vs LAQN Network Comparison

**Testing Whether Data Quality Beats Data Quantity**

---

## 1. Introduction

This report compares Random Forest model performance between two air quality monitoring networks covering Greater London: DEFRA (Department for Environment, Food and Rural Affairs) and LAQN (London Air Quality Network).

DEFRA operates the Automatic Urban and Rural Network (AURN), the UK's statutory national monitoring network with rigorous quality assurance. LAQN is London's local network with denser station coverage but lower data completeness.

The comparison uses identical methodology, time periods, and evaluation metrics.

---

## 2. Dataset Comparison

**Table 1: Network Dataset Characteristics**

| Metric | LAQN | DEFRA | Difference |
|--------|------|-------|------------|
| Site-pollutant combinations | 141 | 40 | LAQN 3.5x more |
| Training samples | 17,107 | 17,036 | Similar |
| Flattened features | 1,740 | 528 | LAQN 3.3x more |
| Data completeness | 87.1% | 91.2% | DEFRA +4.1% |

**Table 2: Station Distribution by Pollutant**

| Pollutant | LAQN | DEFRA |
|-----------|------|-------|
| NO2 | 58 | 13 |
| PM10 | 42 | 7 |
| PM25 | 24 | 7 |
| O3 | 11 | 8 |
| SO2 | 4 | 3 |
| CO | 2 | 2 |

---

## 3. Training Comparison

**Table 3: Training Statistics**

| Metric | LAQN | DEFRA |
|--------|------|-------|
| Total training time | 32.7 hours | 167.2 minutes |
| Average time per model | 14 minutes | 4.2 minutes |
| Tuning time | Not recorded | 12.8 minutes |

DEFRA training was 12x faster due to fewer features (528 vs 1,740).

---

## 4. Hyperparameter Tuning Comparison

**Table 4: Tuning Results**

| Pollutant | DEFRA CV R² | LAQN CV R² | Better |
|-----------|-------------|------------|--------|
| SO2 | 0.904 | 0.422 | DEFRA |
| O3 | 0.845 | 0.812 | DEFRA |
| NO2 | 0.725 | 0.697 | DEFRA |
| CO | 0.718 | 0.520 | DEFRA |
| PM10 | 0.663 | 0.399 | DEFRA |
| PM25 | 0.633 | 0.728 | LAQN |

DEFRA outperforms LAQN in tuning for 5 out of 6 pollutants. The largest improvement is SO2 (+0.482), where DEFRA's London_Bloomsbury station captures real variation while LAQN readings are nearly flat.

**Table 5: Best Parameters Found**

| Pollutant | LAQN max_depth | DEFRA max_depth | LAQN n_estimators | DEFRA n_estimators |
|-----------|----------------|-----------------|-------------------|-------------------|
| CO | 10 | 10 | 100 | 200 |
| NO2 | None | 10 | 200 | 100 |
| O3 | 10 | 10 | 100 | 200 |
| PM10 | 10 | 10 | 200 | 100 |
| PM25 | 10 | None | 200 | 200 |
| SO2 | None | None | 200 | 200 |

---

## 5. Overall Performance

**Table 6: Model Performance Summary**

| Metric | LAQN | DEFRA | Winner |
|--------|------|-------|--------|
| Valid models | 136 | 39 | - |
| Broken models | 5 (3.5%) | 1 (2.5%) | DEFRA |
| Mean test R² | 0.814 | 0.793 | LAQN |
| Mean RMSE | 0.033 | 0.026 | DEFRA |
| Overfitting gap | 0.104 | 0.068 | DEFRA |

An R² of 0.81 (LAQN) or 0.79 (DEFRA) means the model explains approximately 80% of the variance in hourly pollution levels.

---

## 6. Performance by Pollutant

**Table 7: Test R² by Pollutant**

| Pollutant | DEFRA | LAQN | Winner |
|-----------|-------|------|--------|
| O3 | 0.911 | 0.920 | Similar |
| CO | 0.888 | 0.638 | DEFRA |
| NO2 | 0.800 | 0.856 | LAQN |
| PM25 | 0.761 | 0.764 | Similar |
| SO2 | 0.759 | 0.641 | DEFRA |
| PM10 | 0.664 | 0.736 | LAQN |

**Analysis:**

- **O3:** Both achieve R² > 0.91 and follow a predictable daily pattern (low at night, high in the afternoon) driven by sunlight, making it equally easy to predict in both networks.
- **CO:** DEFRA outperforms by +0.250. Clearer patterns at London_N._Kensington_CO.
- **NO2:** LAQN better by +0.056. Denser network (58 vs 13 stations) captures spatial patterns.
- **PM10:** LAQN better by +0.072. More stations (42 vs 7) provide more training examples.
- **SO2:** DEFRA better by +0.118. DEFRA shows better variation; LAQN is nearly flat.

---

## 7. Top and Bottom Performers

**Table 8: Top 5 Models**

| Rank | DEFRA Station | R² | LAQN Station | R² |
|------|---------------|-----|--------------|-----|
| 1 | London_Haringey_Priory_Park_South_O3 | 0.940 | HG4_O3 | 0.939 |
| 2 | London_N._Kensington_O3 | 0.927 | HP1_O3 | 0.935 |
| 3 | London_Westminster_O3 | 0.922 | RI2_O3 | 0.928 |
| 4 | Borehamwood_Meadow_Park_PM25 | 0.920 | BQ7_O3 | 0.925 |
| 5 | London_Bloomsbury_O3 | 0.917 | KC1_O3 | 0.925 |

Both networks achieve similar peak performance (R² approximately 0.94). O3 dominates top performers in both.

---

## 8. Broken Models

**Table 9: Broken Models Summary**

| Aspect | DEFRA | LAQN |
|--------|-------|------|
| Broken models | 1 (2.5%) | 5 (3.5%) |
| Affected stations | 1 | 3 |

**DEFRA:** Tower_Hamlets_Roadside_NO2 (constant test values).

**LAQN:** BG2_NO2, TH4_O3, TH4_PM10, TH4_NO2, WM6_PM10. The TH4 station had complete equipment failure affecting three pollutants.

All broken models share the same root cause: test set standard deviation of 0.000000. When actual values are constant, the R² calculation fails.

---

## 9. Overfitting Analysis

**Table 10: Overfitting Metrics**

| Metric | DEFRA | LAQN |
|--------|-------|------|
| Mean gap (train - val) | 0.068 | 0.104 |
| Max gap | 0.584 | 1.175 |
| Conclusion | Minimal | Mild |

DEFRA's reduced overfitting likely results from higher data quality and fewer features reducing model complexity.

---

## 10. Feature Importance

**Table 11: t-1 Feature Importance**

| Pollutant | DEFRA | LAQN |
|-----------|-------|------|
| O3 | 0.954 | 0.952 |
| PM10 | 0.924 | 0.933 |
| PM25 | 0.911 | 0.935 |
| CO | 0.891 | 0.906 |
| NO2 | 0.878 | 0.918 |
| SO2 | 0.870 | 0.890 |

The previous hour's value (t-1) explains 85% to 95% of predictions in both networks. Spatial correlation is weak (2-5%), and temporal features contribute less than 2%.

---

## 11. Conclusions

### Data Quality vs Data Quantity

Neither network is definitively better:

**LAQN advantages:**
- Slightly higher mean test R² (0.814 vs 0.793).
- Better NO2 and PM10 due to more stations.

**DEFRA advantages:**
- Fewer broken models (2.5% vs 3.5%).
- Less overfitting (gap 0.068 vs 0.104).
- Lower RMSE (0.026 vs 0.033).
- Better CO and SO2 performance.
- 12x faster training.

### Consistent Findings Across Both Networks

- O3 is the most predictable pollutant.
- PM10 is the hardest to predict.
- Temporal autocorrelation dominates (85-95%).
- Models underestimate sudden pollution spikes.
- Models are reliable for trend forecasting but not for predicting high pollution episodes.

---

## 12. Summary Table

| Metric | DEFRA | LAQN | Winner |
|--------|-------|------|--------|
| Mean test R² | 0.793 | 0.814 | LAQN |
| Broken models | 2.5% | 3.5% | DEFRA |
| Overfitting gap | 0.068 | 0.104 | DEFRA |
| Mean RMSE | 0.026 | 0.033 | DEFRA |
| Training time | 167 min | 1,960 min | DEFRA |
| Data completeness | 91.2% | 87.1% | DEFRA |

### Final Verdict

The choice between networks depends on priority:

- **Prioritise accuracy:** LAQN provides slightly better predictions for NO2 and PM10.
- **Prioritise reliability:** DEFRA produces more consistent results with fewer failures.



## References

Géron, A. (2023) *Hands-On Machine Learning with Scikit-Learn, Keras and TensorFlow*. 3rd edn. O'Reilly Media.

*HalvingGridSearchCV* (no date) scikit-learn. Available at: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.HalvingGridSearchCV.html

*RandomForestRegressor* (no date) scikit-learn. Available at: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html

*r2_score* (no date) scikit-learn. Available at: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.r2_score.html
