# DEFRA Random Forest Haringey Priory Park South Station NO2 Pollutant Modelling Report

## 1. Purpose

Initial Random Forest training on a single DEFRA station to compare with LAQN baseline and test whether data quality beats data quantity.

**Target:** London_Haringey_Priory_Park_South_NO2 (located ~3.3 km from LAQN's EN5)

**Selection criteria:** Closest DEFRA station to LAQN's EN5 (Enfield), located approximately 3.3 km apart. The same pollutant (NO2) select for direct comparison.

---

## 2. Dataset

| Metric | DEFRA | LAQN | Difference |
|--------|-------|------|------------|
| Training samples | 11,138 | 9,946 | +12% |
| Features | 288 | 468 | -39% |
| Data completeness | 91.2% | 87.1% | +4.1% |

---

## 3. Baseline Model

**Configuration:** Default RandomForestRegressor (n_estimators=100, max_depth=None)

**Training time:** 33 seconds

| Dataset | R² |
|---------|----------|
| Training | 0.985 |
| Validation | 0.866 |
| Test | 0.852 |

**DEFRA outperforms LAQN by +5% on test R²**

---

## 4. Cross-Validation

| Metric | DEFRA |
|--------|-------|
| CV RMSE (mean) | 0.047 |
| CV RMSE (std) | 0.005 |

DEFRA achieves 14% lower CV RMSE.

---

## 5. Hyperparameter Tuning

**Method:** GridSearchCV with 3-fold CV

**Parameter grid:** 24 combinations

**Training time:** 29 minutes (vs LAQN's 54 minutes)

| Parameter | Best Value |
|-----------|-------|
| max_depth | None |
| min_samples_leaf | 2 |
| min_samples_split | 5 |
| n_estimators | 200 |

**Both networks selected identical hyperparameters.**

| Metric | DEFRA |
|--------|-------|
| Best CV RMSE | 0.046 |

DEFRA achieves 16% lower CV RMSE with identical configuration.

---

## 6. Tuned Model Results

| Metric | DEFRA |
|--------|-------|
| Test R² | 0.855 |
| Test RMSE | 0.033 |
| Test MAE | 0.023 |
| Overfitting gap | 0.114 |

**DEFRA achieves 34% lower RMSE with 39% fewer features.**

---

## 7. Feature Importance

| Feature | Importance |
|---------|-------|
| Target station t-1 | 86.1% |
| Other NO2 stations | 9.5% |
| O3 stations | 2.1% |
| PM10 stations | 1.6% |
| Temporal features | 0.7% |

Both models show identical behaviour: heavy reliance on t-1 autocorrelation.

DEFRA captures a stronger O3 cross-pollutant relationship.

---

## 8. Key Findings

1. **Data quality beats data quantity.** DEFRA achieves better results with fewer features.

2. **Identical optimal hyperparameters.** Both networks converge to the same configuration.

3. **Same prediction pattern.** Both rely on t-1 autocorrelation (83-86%).

4. **DEFRA errors 34% smaller.** Higher data completeness translates to better predictions.

5. **DEFRA trains 46% faster.** Fewer features reduce computation time.

---

## 9. Output Files

All saved to: `data/defra/rf_model/`

| File | Contents |
|------|----------|
| rf_model_tuned.joblib | Trained model |
| predictions.joblib | Actual vs predicted values |
| feature_importance.csv | Feature importance scores |
| results_summary.joblib | Evaluation metrics |



