# CNN Single Station Pollutant Modelling Report

## LAQN Network - EN5_NO2

---

## 1. Purpose

Train a CNN to predict NO2 levels and compare against Random Forest baseline (test R² = 0.814).

**Target:** EN5_NO2 (Enfield, North London)

**Selection criteria:** Highest data coverage (99.6%) in LAQN network.

---

## 2. Dataset

| Metric | Value |
|--------|-------|
| Training samples | 9,946 |
| Validation samples | 2,131 |
| Test samples | 2,132 |
| Input shape | (samples, 12 timesteps, 39 features) |

The 3D shape allows CNN to learn temporal patterns across 12 hours of history.

---

## 3. Baseline Model

**Architecture:** 2 Conv1D layers (32 filters each, kernel_size=4) + Dense (50 units)

**Parameters:** 18,853 (73.64 KB)

**Training:** Stopped at epoch 30, best at epoch 15

| Dataset | R² |
|---------|-----|
| Training | 0.743 |
| Validation | 0.670 |
| Test | 0.615 |

**Comparison with RF:** CNN baseline (0.615) significantly underperforms RF (0.814).

---

## 4. Training Behaviour

| Metric | Start (Epoch 1) | Best (Epoch 15) | Change |
|--------|-----------------|-----------------|--------|
| val_loss | 0.0120 | 0.0077 | -36% |
| val_mae | 0.0841 | 0.0634 | -25% |

Learning rate reduced three times before early stopping triggered.

---

## 5. Hyperparameter Tuning

**Method:** KerasTuner RandomSearch, 20 trials, 6 minutes

| Parameter | Baseline | Tuned |
|-----------|----------|-------|
| filters_1 | 32 | 128 |
| filters_2 | 32 | 64 |
| kernel_size | 4 | 2 |
| dropout | 0.2 | 0.1 |
| dense_units | 50 | 50 |

**Key finding:** Larger model (128/64 filters) and shorter kernel (2 hours) work better.

---

## 6. Tuned Model Results

| Dataset | R² |
|---------|-----|
| Training | 0.872 |
| Validation | 0.867 |
| Test | 0.796 |

**Improvement:** Test R² increased from 0.615 to 0.796 (+29%).

**Overfitting gap:** 0.076 (training - test), acceptable.

---

## 7. Model Comparison

| Model | Test R² | Test RMSE | Test MAE |
|-------|---------|-----------|----------|
| Baseline CNN | 0.615 | 0.0725 | 0.0519 |
| Tuned CNN | 0.796 | 0.0528 | 0.0367 |
| Random Forest | 0.814 | 0.0505 | 0.0344 |

**Result:** Random Forest still wins by 0.018, but tuned CNN is now competitive.

---

## 8. Key Findings

1. **Baseline CNN underperformed RF** due to insufficient model capacity and suboptimal kernel size.

2. **Tuning closed the gap** from 0.199 to 0.018 between CNN and RF.

3. **Short-term patterns matter.** kernel_size=2 (2 hours) outperformed larger windows.

4. **More capacity needed.** LAQN's noisier data required larger model (128/64 filters).

5. **Both models underpredict peaks** due to limited extreme pollution samples.

---

## 9. Output Files

All saved to: `data/ml/LAQN_EN5_NO2/cnn_model/`

| File | Contents |
|------|----------|
| tuned_cnn_model_EN5_NO2.keras | Trained model |
| tuned_predictions_EN5_NO2.joblib | Actual vs predicted values |
| best_hyperparameters_EN5_NO2.joblib | Tuning results |
| results_summary_EN5_NO2.joblib | Evaluation metrics |

---

## 10. Conclusion

For LAQN data, Random Forest slightly outperforms CNN (0.814 vs 0.796). The noisier data (87.1% completeness) requires a larger CNN architecture but still cannot match RF's ability to exploit the dominant t-1 feature directly.

---

## References

Gilik, A., Ogrenci, A.S. and Ozmen, A. (2021) 'Air quality prediction using CNN+LSTM-based hybrid deep learning architecture', *Environmental Science and Pollution Research*, 29(8), pp. 11920–11938.

Géron, A. (2023) *Hands-On Machine Learning with Scikit-Learn, Keras and TensorFlow*. 3rd edn. O'Reilly Media.

Keras Tuner Documentation. Available at: https://keras.io/keras_tuner/
