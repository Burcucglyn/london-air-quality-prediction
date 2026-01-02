# CNN Single Station Pollutant Modelling Report

## DEFRA Network - London_Haringey_Priory_Park_South_NO2

---

## 1. Purpose

Train a CNN to predict NO2 levels and compare against Random Forest baseline (test R² = 0.855).

**Target:** London_Haringey_Priory_Park_South_NO2

**Selection criteria:** Closest DEFRA station to enable cross-network comparison, same pollutant (NO2).

---

## 2. Dataset

| Metric | Value |
|--------|-------|
| Training samples | 11,138 |
| Validation samples | 2,387 |
| Test samples | 2,387 |
| Input shape | (samples, 12 timesteps, 24 features) |
| Data completeness | 91.2% |

The 3D shape allows CNN to learn temporal patterns across 12 hours of history.

---

## 3. Baseline Model

**Architecture:** 2 Conv1D layers (32 filters each, kernel_size=4) + Dense (50 units)

**Parameters:** 16,933 (66.14 KB)

**Training:** Stopped at epoch 34, best at epoch 19

| Dataset | R² |
|---------|-----|
| Training | 0.806 |
| Validation | 0.715 |
| Test | 0.706 |

**Comparison with RF:** CNN baseline (0.706) underperforms RF (0.855).

---

## 4. Training Behaviour

| Metric | Start (Epoch 1) | Best (Epoch 19) | Change |
|--------|-----------------|-----------------|--------|
| val_loss | 0.0070 | 0.00387 | -45% |
| val_mae | 0.0570 | 0.0421 | -26% |

Learning rate reduced four times before early stopping triggered. Validation curve was smooth with minimal spikes, indicating stable training on clean data.

---

## 5. Hyperparameter Tuning

**Method:** KerasTuner RandomSearch, 20 trials, 34 minutes

| Parameter | Baseline | Tuned |
|-----------|----------|-------|
| filters_1 | 32 | 32 |
| filters_2 | 32 | 16 |
| kernel_size | 4 | 2 |
| dropout_1 | 0.2 | 0.1 |
| dropout_3 | 0.2 | 0.3 |
| dense_units | 50 | 25 |

**Key findings:**

- Simpler model won (16 filters, 25 dense units).
- Shorter kernel (2 hours) captures patterns better than 4 hours.
- Mixed dropout strategy: less in conv layers (0.1), more in dense layer (0.3).

---

## 6. Tuned Model Results

| Dataset | R² |
|---------|-----|
| Training | 0.895 |
| Validation | 0.864 |
| Test | 0.840 |

**Improvement:** Test R² increased from 0.706 to 0.840 (+19%).

**Overfitting gap:** 0.055 (training - test), minimal overfitting.

---

## 7. Model Comparison

| Model | Test R² | Test RMSE | Test MAE |
|-------|---------|-----------|----------|
| Baseline CNN | 0.706 | 0.0473 | 0.0335 |
| Tuned CNN | 0.840 | 0.0349 | 0.0243 |
| Random Forest | 0.855 | 0.0332 | 0.0227 |

**Result:** Tuned CNN approaches RF performance. Gap reduced from 0.149 to 0.015.

---

## 8. Key Findings

1. **Tuning essential.** Baseline CNN significantly underperformed RF. Tuning closed the gap.

2. **Simpler model works.** 32/16 filters and 25 dense units outperformed larger architectures.

3. **Short-term patterns matter.** kernel_size=2 (2 hours) optimal for predicting next hour.

4. **Minimal overfitting.** Gap of 0.055 is the smallest across all models tested.

5. **Peak underprediction improved.** Worst case improved from 52% to 25% underprediction.

---

## 9. Output Files

All saved to: `data/ml/DEFRA_Haringey_NO2/cnn_model/`

| File | Contents |
|------|----------|
| tuned_cnn_model_London_Haringey_Priory_Park_South_NO2.keras | Trained model |
| tuned_predictions_London_Haringey_Priory_Park_South_NO2.joblib | Actual vs predicted values |
| best_hyperparameters_London_Haringey_Priory_Park_South_NO2.joblib | Tuning results |
| results_summary_London_Haringey_Priory_Park_South_NO2.joblib | Evaluation metrics |

---

## 10. Conclusion

For DEFRA data, the tuned CNN (0.840) approaches Random Forest performance (0.855). The high data quality (91.2% completeness) allows CNN to learn temporal patterns effectively with a simple architecture. A smaller model with fewer parameters generalises better, confirming that clean data reduces the need for model complexity.

---

## References

Gilik, A., Ogrenci, A.S. and Ozmen, A. (2021) 'Air quality prediction using CNN+LSTM-based hybrid deep learning architecture', *Environmental Science and Pollution Research*, 29(8), pp. 11920–11938.

Géron, A. (2023) *Hands-On Machine Learning with Scikit-Learn, Keras and TensorFlow*. 3rd edn. O'Reilly Media.

Keras Tuner Documentation. Available at: https://keras.io/keras_tuner/
