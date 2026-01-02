# Random Forest Single-Station Trial Report

## LAQN Network - EN5_NO2

---

## 1. Purpose

Initial Random Forest training on a single station to establish baseline methodology before scaling to all 141 site-pollutant combinations.

**Target:** EN5_NO2 (Enfield, North London)

---

## 2. Dataset

| Metric | Value |
|--------|-------|
| Training samples | 9,946 |
| Validation samples | 2,131 |
| Test samples | 2,132 |
| Flattened features | 468 (12 timesteps × 39 features) |

---

## 3. Baseline Model

**Configuration:** Default RandomForestRegressor (n_estimators=100, max_depth=None)

**Training time:** 87 seconds

| Dataset | R² |
|---------|-----|
| Training | 0.979 |
| Validation | 0.861 |
| Test | 0.810 |

**Overfitting gap:** 0.118 (mild overfitting detected)

---

## 4. Cross-Validation

5-fold CV RMSE: 0.054 ± 0.004

Consistent performance across folds confirmed model stability.

---

## 5. Hyperparameter Tuning

**Method:** GridSearchCV with 3-fold CV

**Parameter grid:** 24 combinations

**Training time:** 53.86 minutes

| Parameter | Best Value |
|-----------|------------|
| max_depth | None |
| min_samples_leaf | 2 |
| min_samples_split | 5 |
| n_estimators | 200 |

**Best CV RMSE:** 0.055

---

## 6. Tuned Model Results

| Dataset | R² |
|---------|-----|
| Training | 0.974 |
| Validation | 0.862 |
| Test | 0.814 |

**Overfitting gap:** 0.112 (reduced from 0.118)

**Improvement:** Test R² increased from 0.810 to 0.814

---

## 7. Feature Importance

| Feature | Importance |
|---------|------------|
| EN5_NO2_t-1 | 83.5% |
| Other NO2 stations | 12.2% |
| PM10 stations | 2.4% |
| O3 stations | 1.2% |
| Temporal features | 0.7% |

The previous hour's value dominates predictions. Model learns persistence: next hour ≈ current hour.

---

## 8. Key Findings

1. **Temporal autocorrelation dominates.** The t-1 feature explains 83.5% of predictions.

2. **Cross-pollutant relationships weak.** PM10 and O3 contribute only 3.6% combined.

3. **Peak underestimation.** Model struggles with sudden pollution spikes.

4. **Mild overfitting.** Gap of 0.11 between training and test R².

5. **R² = 0.814 is acceptable baseline** for CNN comparison.

---

## 9. Output Files

All saved to: `data/laqn/rf_model/`

| File | Contents |
|------|----------|
| rf_model_EN5_NO2.joblib | Trained model |
| predictions_EN5_NO2.joblib | Actual vs predicted values |
| feature_importance_EN5_NO2.csv | Feature importance scores |
| results_summary_EN5_NO2.joblib | Evaluation metrics |

