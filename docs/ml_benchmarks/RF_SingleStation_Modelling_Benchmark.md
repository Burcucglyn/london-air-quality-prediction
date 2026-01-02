# Random Forest Single-Station Trial Benchmark

## DEFRA vs LAQN Comparison

---

## 1. Purpose

Compare Random Forest performance between DEFRA and LAQN networks using a single target station from each. This initial trial established methodology and tested whether data quality compensates for fewer features before scaling to all stations.

**Station Selection:**

| Network | Target Station | Location | Selection Criteria |
|---------|----------------|----------|-------------------|
| LAQN | EN5_NO2 | Enfield, North London | Initial training target |
| DEFRA | London_Haringey_Priory_Park_South_NO2 | Haringey, North London | Closest to EN5 (~3.3 km) |

Both stations measure NO2 and are located in North London, enabling direct comparison.

---

## 2. Dataset Comparison

| Metric | LAQN | DEFRA | Difference |
|--------|------|-------|------------|
| Training samples | 9,946 | 11,138 | DEFRA +12% |
| Validation samples | 2,131 | 2,387 | DEFRA +12% |
| Test samples | 2,132 | 2,387 | DEFRA +12% |
| Original features | 39 | 24 | LAQN +63% |
| Flattened features | 468 | 288 | LAQN +63% |
| Data completeness | 87.1% | 91.2% | DEFRA +4.1% |

LAQN has more features from denser station coverage. DEFRA has more samples and higher data quality.

---

## 3. Baseline Model Comparison

Default RandomForestRegressor (n_estimators=100, max_depth=None)

| Metric | LAQN | DEFRA | Winner |
|--------|------|-------|--------|
| Training time | 87 sec | 33 sec | DEFRA |
| Training R² | 0.979 | 0.985 | DEFRA |
| Validation R² | 0.861 | 0.866 | DEFRA |
| Test R² | 0.810 | 0.852 | DEFRA |
| Overfitting gap | 0.118 | 0.119 | Similar |

DEFRA achieves higher R² across all datasets while training 62% faster.

---

## 4. Cross-Validation Comparison

5-fold cross-validation results:

| Metric | LAQN | DEFRA | Winner |
|--------|------|-------|--------|
| CV RMSE (mean) | 0.054 | 0.047 | DEFRA |
| CV RMSE (std) | 0.004 | 0.005 | LAQN |
| Best fold | 0.050 | 0.037 | DEFRA |
| Worst fold | 0.062 | 0.051 | DEFRA |

DEFRA achieves 14% lower mean CV RMSE with slightly higher variance between folds.

---

## 5. Hyperparameter Tuning Comparison

GridSearchCV with 24 parameter combinations, 3-fold CV:

| Metric | LAQN | DEFRA |
|--------|------|-------|
| Training time | 53.86 min | 29.09 min |
| Best CV RMSE | 0.055 | 0.046 |

**Best parameters found:**

| Parameter | LAQN | DEFRA |
|-----------|------|-------|
| max_depth | None | None |
| min_samples_leaf | 2 | 2 |
| min_samples_split | 5 | 5 |
| n_estimators | 200 | 200 |

Both networks independently selected identical hyperparameters. DEFRA trains 46% faster and achieves 16% lower CV RMSE.

---

## 6. Tuned Model Comparison

| Metric | LAQN | DEFRA | Difference | Winner |
|--------|------|-------|------------|--------|
| Training R² | 0.974 | 0.980 | +0.6% | DEFRA |
| Validation R² | 0.862 | 0.866 | +0.5% | DEFRA |
| Test R² | 0.814 | 0.855 | +5.0% | DEFRA |
| Test RMSE | 0.050 | 0.033 | -34% | DEFRA |
| Test MAE | 0.034 | 0.023 | -34% | DEFRA |
| Overfitting gap | 0.112 | 0.114 | Similar | - |

---

## 7. Feature Importance Comparison

| Category | LAQN | DEFRA |
|----------|------|-------|
| Target station t-1 | 83.5% | 86.1% |
| Target station t-2, t-3 | 0.3% | 0.8% |
| Other NO2 stations | 12.2% | 9.5% |
| O3 stations | 1.2% | 2.1% |
| PM10 stations | 2.4% | 1.6% |
| Temporal features | 0.7% | 0.7% |

---

## 8. Training Efficiency

| Metric | LAQN | DEFRA | DEFRA Advantage |
|--------|------|-------|-----------------|
| Baseline training | 87 sec | 33 sec | 62% faster |
| GridSearchCV | 53.86 min | 29.09 min | 46% faster |
| Features processed | 468 | 288 | 39% fewer |

DEFRA's smaller feature set enables faster training without sacrificing accuracy.

---

## 9. Conclusions

### Data Quality vs Data Quantity

DEFRA demonstrates that higher data completeness (91.2% vs 87.1%) is more valuable than having more features (288 vs 468). Despite 39% fewer features, DEFRA achieves:

- 5% higher test R² (0.855 vs 0.814)
- 34% lower test RMSE (0.033 vs 0.050)
- 46% faster hyperparameter tuning

The 4.1 percentage point advantage in data completeness translates to substantially better predictions.

### Identical Model Behaviour

Both networks independently converged to identical optimal hyperparameters (max_depth=None, min_samples_leaf=2, min_samples_split=5, n_estimators=200). This suggests these parameters are optimal for NO2 time series prediction regardless of network choice.

Both models show the same fundamental pattern:

- Heavy reliance on t-1 autocorrelation (83-86%)
- Weak spatial correlation from neighbouring stations
- Minimal contribution from cross-pollutant features
- Negligible temporal feature importance (<1%)

The models learn persistence-based prediction: next hour ≈ current hour + small adjustments.

### Cross-Pollutant Relationships

DEFRA captures stronger O3 relationship (2.1% vs 1.2%), while LAQN captures stronger PM10 relationship (2.4% vs 1.6%). This may reflect different station compositions or local emission characteristics between networks.

### Prediction Limitations

Both models share the same limitation: underestimation of peak pollution events. When actual values exceed 0.5, predictions fall below actual. This is a direct consequence of t-1 reliance. The model cannot anticipate rapid changes because it predicts based on recent history.

DEFRA's underestimation is less severe (~18% below peaks vs ~22% for LAQN), suggesting cleaner training data helps the model learn slightly better peak responses.

### Practical Implications

For single-station NO2 prediction in London:

- DEFRA provides more accurate predictions with lower computational cost.
- Both networks are suitable for trend forecasting but not for predicting pollution spikes.
- The choice of network matters less than data quality at the chosen station.

---

## 10. Summary Table

| Metric | LAQN | DEFRA | Winner |
|--------|------|-------|--------|
| Test R² | 0.814 | 0.855 | DEFRA |
| Test RMSE | 0.050 | 0.033 | DEFRA |
| Test MAE | 0.034 | 0.023 | DEFRA |
| CV RMSE | 0.055 | 0.046 | DEFRA |
| Training time (tuning) | 54 min | 29 min | DEFRA |
| Features | 468 | 288 | - |
| Samples | 9,946 | 11,138 | DEFRA |
| Data completeness | 87.1% | 91.2% | DEFRA |
| t-1 importance | 83.5% | 86.1% | - |
| Overfitting gap | 0.112 | 0.114 | Similar |

**Overall:** DEFRA wins on accuracy, speed, and data quality. LAQN wins only on feature count, which proved less important than data completeness.

