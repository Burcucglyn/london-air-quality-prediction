```
data dimensions:
  samples: 17,107
  timesteps: 12
  features: 145

feature names (145 total):
  first 10: ['BG1_NO2', 'BG1_SO2', 'BG2_NO2', 'BG2_PM10', 'BQ7_NO2', 'BQ7_O3', 'BQ7_PM10', 'BQ7_PM25', 'BQ9_PM10', 'BQ9_PM25']
  last 10: ['WAC_PM10', 'WM5_NO2', 'WM6_NO2', 'WM6_PM10', 'WMD_NO2', 'WMD_PM25', 'hour', 'day_of_week', 'month', 'is_weekend']
```

## 4. identify all target columns

need to identify which columns are pollutant predictions (targets) and which are temporal features. temporal features like hour, day_of_week are inputs only, not things we want to predict.

### pollutant naming convention

each target column follows the pattern: `{SiteCode}_{PollutantCode}`

for example:
- BG1_NO2 means NO2 at site BG1
- EN5_PM25 means PM2.5 at site EN5

### the 6 regulatory pollutants

| pollutant | code | UK annual limit |
|-----------|------|----------------|
| Nitrogen Dioxide | NO2 | 40 µg/m³ |
| PM2.5 Particulate | PM25 | 20 µg/m³ |
| PM10 Particulate | PM10 | 40 µg/m³ |
| Ozone | O3 | - |
| Sulphur Dioxide | SO2 | - |
| Carbon Monoxide | CO | - |

source: Department for Environment, Food and Rural Affairs (2019) UK Air Quality Objectives

```
total features: 145
temporal features: 4
pollutant targets: 141

breakdown by pollutant:
  NO2: 58 stations
  PM25: 24 stations
  PM10: 42 stations
  O3: 11 stations
  SO2: 4 stations
  CO: 2 stations
```

## 5. build CNN model function

building a function that creates CNN models. using the best hyperparameters found from the single-station tuning:

| parameter | value | why |
|-----------|-------|-----|
| filters_1 | 128 | more capacity to learn patterns |
| kernel_1 | 2 | short-term patterns matter most |
| dropout | 0.1 | less regularisation needed |
| filters_2 | 64 | second layer with fewer filters |
| kernel_2 | 2 | consistent with first layer |
| dense_units | 50 | same as baseline |
| learning_rate | 0.001 | adam default works well |

these parameters came from keras tuner results in the single-station CNN notebook.

source: Géron, A. (2023) Hands-on machine learning with scikit-learn, Keras and TensorFlow. Ch. 15.

 

```
model created with 92,197 parameters
Model: "sequential"
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
┃ Layer (type)                    ┃ Output Shape           ┃       Param # ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
│ conv1d (Conv1D)                 │ (None, 12, 128)        │        37,248 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ dropout (Dropout)               │ (None, 12, 128)        │             0 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ conv1d_1 (Conv1D)               │ (None, 12, 64)         │        16,448 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ dropout_1 (Dropout)             │ (None, 12, 64)         │             0 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ flatten (Flatten)               │ (None, 768)            │             0 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ dense (Dense)                   │ (None, 50)             │        38,450 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ dropout_2 (Dropout)             │ (None, 50)             │             0 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ dense_1 (Dense)                 │ (None, 1)              │            51 │
└─────────────────────────────────┴────────────────────────┴───────────────┘
 Total params: 92,197 (360.14 KB)
 Trainable params: 92,197 (360.14 KB)
 Non-trainable params: 0 (0.00 B)
```

```
callbacks configured:
  - early stopping (patience=10)
  - reduce LR on plateau (factor=0.5, patience=5)
```

```
============================================================
Started at: 2025-12-31 01:05:47
Targets to train: 141
Training samples: 17,107
Features: 145
============================================================
[  1/141] BG1_NO2         | R2=0.585 | Time=140s | ETA=326min
[  2/141] BG1_SO2         | R2=0.656 | Time=119s | ETA=300min
[  3/141] BG2_NO2         | R2=-1495952367336140489190212108288.000 | Time=134s | ETA=302min
[  4/141] BG2_PM10        | R2=0.023 | Time=70s | ETA=265min
[  5/141] BQ7_NO2         | R2=0.706 | Time=80s | ETA=247min
[  6/141] BQ7_O3          | R2=0.910 | Time=172s | ETA=269min
[  7/141] BQ7_PM10        | R2=0.760 | Time=108s | ETA=263min
[  8/141] BQ7_PM25        | R2=0.758 | Time=115s | ETA=261min
[  9/141] BQ9_PM10        | R2=0.730 | Time=133s | ETA=263min
[ 10/141] BQ9_PM25        | R2=0.726 | Time=147s | ETA=267min
[ 11/141] BT4_NO2         | R2=0.804 | Time=164s | ETA=273min
[ 12/141] BT4_PM10        | R2=0.554 | Time=135s | ETA=273min
[ 13/141] BT4_PM25        | R2=0.522 | Time=113s | ETA=268min
[ 14/141] BT5_NO2         | R2=0.747 | Time=159s | ETA=271min
[ 15/141] BT5_PM10        | R2=0.525 | Time=94s | ETA=265min
[ 16/141] BT5_PM25        | R2=0.164 | Time=91s | ETA=258min
[ 17/141] BT6_NO2         | R2=0.784 | Time=144s | ETA=259min
[ 18/141] BT6_PM10        | R2=0.507 | Time=218s | ETA=267min
[ 19/141] BT6_PM25        | R2=0.463 | Time=157s | ETA=268min
[ 20/141] BT8_NO2         | R2=0.729 | Time=131s | ETA=266min
   [Checkpoint saved at 20 models]
[ 21/141] BT8_PM10        | R2=0.551 | Time=182s | ETA=269min
[ 22/141] BT8_PM25        | R2=0.579 | Time=111s | ETA=264min
[ 23/141] BX1_NO2         | R2=0.788 | Time=171s | ETA=265min
[ 24/141] BX1_O3          | R2=0.891 | Time=160s | ETA=265min
[ 25/141] BX1_SO2         | R2=0.701 | Time=195s | ETA=268min
[ 26/141] BX2_NO2         | R2=0.761 | Time=142s | ETA=266min
[ 27/141] BX2_PM10        | R2=0.554 | Time=191s | ETA=267min
[ 28/141] BX2_PM25        | R2=0.777 | Time=133s | ETA=264min
[ 29/141] BY7_NO2         | R2=0.722 | Time=137s | ETA=262min
[ 30/141] BY7_PM10        | R2=0.416 | Time=104s | ETA=257min
[ 31/141] BY7_PM25        | R2=0.462 | Time=145s | ETA=255min
[ 32/141] CD1_NO2         | R2=0.682 | Time=139s | ETA=253min
[ 33/141] CD1_PM10        | R2=0.554 | Time=141s | ETA=251min
[ 34/141] CD1_PM25        | R2=0.551 | Time=202s | ETA=252min
[ 35/141] CE2_NO2         | R2=0.509 | Time=73s | ETA=246min
[ 36/141] CE2_O3          | R2=0.887 | Time=228s | ETA=248min
[ 37/141] CE2_PM10        | R2=0.466 | Time=64s | ETA=242min
[ 38/141] CE2_PM25        | R2=0.701 | Time=91s | ETA=238min
[ 39/141] CE3_NO2         | R2=0.378 | Time=66s | ETA=232min
[ 40/141] CE3_PM10        | R2=0.434 | Time=179s | ETA=232min
   [Checkpoint saved at 40 models]
[ 41/141] CE3_PM25        | R2=0.505 | Time=128s | ETA=229min
[ 42/141] CR5_NO2         | R2=0.821 | Time=152s | ETA=228min
[ 43/141] CR7_NO2         | R2=0.799 | Time=215s | ETA=228min
[ 44/141] CR8_PM25        | R2=0.000 | Time=215s | ETA=229min
[ 45/141] CW3_NO2         | R2=0.740 | Time=132s | ETA=226min
[ 46/141] CW3_PM10        | R2=0.844 | Time=204s | ETA=226min
[ 47/141] CW3_PM25        | R2=0.872 | Time=173s | ETA=225min
[ 48/141] EA6_NO2         | R2=0.787 | Time=160s | ETA=223min
[ 49/141] EA6_PM10        | R2=0.550 | Time=194s | ETA=222min
[ 50/141] EA8_NO2         | R2=0.757 | Time=136s | ETA=219min
[ 51/141] EA8_PM10        | R2=0.609 | Time=109s | ETA=216min
[ 52/141] EI1_NO2         | R2=0.797 | Time=144s | ETA=214min
[ 53/141] EI1_PM10        | R2=0.523 | Time=229s | ETA=214min
[ 54/141] EI8_PM10        | R2=0.606 | Time=132s | ETA=211min
[ 55/141] EN1_NO2         | R2=0.851 | Time=149s | ETA=209min
[ 56/141] EN4_NO2         | R2=0.777 | Time=151s | ETA=206min
[ 57/141] EN5_NO2         | R2=0.810 | Time=122s | ETA=203min
[ 58/141] EN7_NO2         | R2=0.765 | Time=165s | ETA=202min
[ 59/141] GB0_PM25        | R2=0.649 | Time=110s | ETA=198min
[ 60/141] GB6_NO2         | R2=0.824 | Time=133s | ETA=196min
   [Checkpoint saved at 60 models]
[ 61/141] GB6_O3          | R2=0.891 | Time=216s | ETA=195min
[ 62/141] GB6_PM10        | R2=0.504 | Time=144s | ETA=192min
[ 63/141] GN0_NO2         | R2=0.780 | Time=88s | ETA=189min
[ 64/141] GN0_PM10        | R2=0.475 | Time=124s | ETA=186min
[ 65/141] GN0_PM25        | R2=0.571 | Time=128s | ETA=183min
[ 66/141] GN3_NO2         | R2=0.786 | Time=124s | ETA=180min
[ 67/141] GN3_O3          | R2=0.884 | Time=190s | ETA=179min
[ 68/141] GN3_PM10        | R2=0.334 | Time=127s | ETA=176min
[ 69/141] GN3_PM25        | R2=0.706 | Time=111s | ETA=173min
[ 70/141] GN4_NO2         | R2=0.802 | Time=152s | ETA=171min
[ 71/141] GN4_PM10        | R2=0.537 | Time=168s | ETA=169min
[ 72/141] GN5_NO2         | R2=0.691 | Time=102s | ETA=166min
[ 73/141] GN5_PM10        | R2=0.559 | Time=168s | ETA=164min
[ 74/141] GN6_NO2         | R2=0.761 | Time=197s | ETA=162min
[ 75/141] GN6_PM10        | R2=0.607 | Time=107s | ETA=159min
[ 76/141] GN6_PM25        | R2=-0.731 | Time=143s | ETA=157min
[ 77/141] GR7_NO2         | R2=0.758 | Time=232s | ETA=156min
[ 78/141] GR7_PM10        | R2=0.602 | Time=179s | ETA=154min
[ 79/141] GR8_NO2         | R2=0.749 | Time=119s | ETA=151min
[ 80/141] GR8_PM10        | R2=0.543 | Time=136s | ETA=149min
   [Checkpoint saved at 80 models]
[ 81/141] GR9_NO2         | R2=0.839 | Time=191s | ETA=147min
[ 82/141] GR9_PM10        | R2=0.592 | Time=213s | ETA=145min
[ 83/141] GR9_PM25        | R2=0.582 | Time=140s | ETA=143min
[ 84/141] HG1_NO2         | R2=0.734 | Time=174s | ETA=140min
[ 85/141] HG4_NO2         | R2=0.860 | Time=138s | ETA=138min
[ 86/141] HG4_O3          | R2=0.919 | Time=211s | ETA=136min
[ 87/141] HP1_NO2         | R2=0.745 | Time=71s | ETA=133min
[ 88/141] HP1_O3          | R2=0.902 | Time=134s | ETA=130min
[ 89/141] HP1_PM10        | R2=0.803 | Time=169s | ETA=128min
[ 90/141] HP1_PM25        | R2=0.847 | Time=210s | ETA=126min
[ 91/141] HV1_NO2         | R2=0.774 | Time=134s | ETA=124min
[ 92/141] HV3_NO2         | R2=0.733 | Time=112s | ETA=121min
[ 93/141] HV3_PM10        | R2=0.777 | Time=231s | ETA=119min
[ 94/141] IS2_NO2         | R2=0.715 | Time=158s | ETA=117min
[ 95/141] IS2_PM10        | R2=0.273 | Time=91s | ETA=114min
[ 96/141] IS6_NO2         | R2=0.775 | Time=161s | ETA=111min
[ 97/141] IS6_PM10        | R2=0.310 | Time=228s | ETA=110min
[ 98/141] KC1_CO          | R2=0.483 | Time=99s | ETA=107min
[ 99/141] KC1_NO2         | R2=0.845 | Time=187s | ETA=105min
[100/141] KC1_O3          | R2=0.895 | Time=153s | ETA=102min
   [Checkpoint saved at 100 models]
[101/141] KC1_PM25        | R2=0.839 | Time=108s | ETA=99min
[102/141] KC1_SO2         | R2=0.803 | Time=176s | ETA=97min
[103/141] LB4_NO2         | R2=0.566 | Time=120s | ETA=94min
[104/141] LB4_PM10        | R2=0.450 | Time=160s | ETA=92min
[105/141] LB4_PM25        | R2=0.405 | Time=176s | ETA=90min
[106/141] LB6_NO2         | R2=0.840 | Time=138s | ETA=87min
[107/141] LB6_PM10        | R2=0.248 | Time=99s | ETA=84min
[108/141] ME9_NO2         | R2=0.764 | Time=159s | ETA=82min
[109/141] MY1_CO          | R2=0.830 | Time=144s | ETA=79min
[110/141] MY1_NO2         | R2=0.722 | Time=126s | ETA=77min
[111/141] MY1_O3          | R2=0.857 | Time=106s | ETA=74min
[112/141] MY1_SO2         | R2=0.077 | Time=226s | ETA=72min
[113/141] RI1_NO2         | R2=0.668 | Time=99s | ETA=69min
[114/141] RI1_PM10        | R2=0.287 | Time=111s | ETA=67min
[115/141] RI2_NO2         | R2=0.804 | Time=137s | ETA=64min
[116/141] RI2_O3          | R2=0.906 | Time=151s | ETA=62min
[117/141] RI2_PM10        | R2=0.453 | Time=107s | ETA=59min
[118/141] SK5_NO2         | R2=0.836 | Time=156s | ETA=57min
[119/141] SK5_PM10        | R2=0.634 | Time=133s | ETA=54min
[120/141] TH2_NO2         | R2=0.830 | Time=177s | ETA=52min
   [Checkpoint saved at 120 models]
[121/141] TH4_NO2         | R2=-243629731975496583525961826304.000 | Time=183s | ETA=50min
[122/141] TH4_O3          | R2=-859351937836635163572058456064.000 | Time=171s | ETA=47min
[123/141] TH4_PM10        | R2=-460376520887681331232768000000.000 | Time=101s | ETA=45min
[124/141] TH4_PM25        | R2=0.000 | Time=201s | ETA=42min
[125/141] TL4_NO2         | R2=0.630 | Time=171s | ETA=40min
[126/141] TL5_NO2         | R2=0.420 | Time=116s | ETA=37min
[127/141] TL6_NO2         | R2=0.696 | Time=112s | ETA=35min
[128/141] TL6_PM25        | R2=0.241 | Time=68s | ETA=32min
[129/141] WA7_NO2         | R2=0.530 | Time=131s | ETA=30min
[130/141] WA7_PM10        | R2=0.398 | Time=109s | ETA=27min
[131/141] WA9_PM10        | R2=0.608 | Time=178s | ETA=25min
[132/141] WAA_NO2         | R2=0.701 | Time=144s | ETA=22min
[133/141] WAA_PM10        | R2=0.527 | Time=112s | ETA=20min
[134/141] WAB_NO2         | R2=0.798 | Time=86s | ETA=17min
[135/141] WAB_PM10        | R2=0.378 | Time=66s | ETA=15min
[136/141] WAC_PM10        | R2=0.539 | Time=102s | ETA=12min
[137/141] WM5_NO2         | R2=0.802 | Time=148s | ETA=10min
[138/141] WM6_NO2         | R2=0.632 | Time=120s | ETA=7min
[139/141] WM6_PM10        | R2=-5526321308161753884842262528.000 | Time=221s | ETA=5min
[140/141] WMD_NO2         | R2=0.534 | Time=87s | ETA=2min
   [Checkpoint saved at 140 models]
[141/141] WMD_PM25        | R2=0.700 | Time=183s | ETA=0min
============================================================
Training complete!
Total time: 344.7 minutes (5.74 hours)
Average per model: 146.7 seconds
============================================================
```

```
Overall CNN Performance Summary
==================================================
Total targets trained: 141

Test R² statistics:
  Mean:   -21736431768397984426180476928.0000
  Median: 0.6956
  Std:    150738021277393015649098268672.0000
  Min:    -1495952367336140489190212108288.0000
  Max:    0.9194

Test RMSE statistics:
  Mean:   0.0364
  Median: 0.0366
```

```
Performance by Pollutant Type
==================================================
                r2_mean        r2_std        r2_min  r2_max  n_stations  rmse_mean  mae_mean
pollutant                                                                                   
CO         6.567000e-01  2.453000e-01  4.833000e-01  0.8302           2     0.0505    0.0225
NO2       -2.999279e+28  1.984614e+29 -1.495952e+30  0.8597          58     0.0425    0.0313
O3        -7.812290e+28  2.591044e+29 -8.593519e+29  0.9194          11     0.0417    0.0312
PM10      -1.109292e+28  7.102196e+28 -4.603765e+29  0.8441          42     0.0323    0.0211
PM25       4.954000e-01  3.576000e-01 -7.310000e-01  0.8720          24     0.0280    0.0190
SO2        5.593000e-01  3.276000e-01  7.670000e-02  0.8032           4     0.0195    0.0138
```

![test_r2 image](/Users/burdzhuchaglayan/Desktop/test_r2 image.png)

```
Random Forest results not found at: /data/ml/LAQN_ALL/rf_model/all_targets_results.csv
Run rf_training_laqn_all.ipynb first for comparison.
```

```
============================================================
CNN Model Training Complete - All LAQN Stations
============================================================

Dataset: LAQN (London Air Quality Network)
Targets trained: 141
Training samples: 17,107
Test samples: 3,657

--- Overall Performance ---
Mean Test R²:   -21736431768397984426180476928.0000
Median Test R²: 0.6956
Mean Test RMSE: 0.0364
Mean Test MAE:  0.0255

--- By Pollutant ---
CO    : R²=0.657 ± 0.245 (n=2 stations)
SO2   : R²=0.559 ± 0.328 (n=4 stations)
PM25  : R²=0.495 ± 0.358 (n=24 stations)
PM10  : R²=-11092924814186739467376656384.000 ± 71021957445095715383046832128.000 (n=42 stations)
NO2   : R²=-29992794815717878440877096960.000 ± 198461362304017972436913881088.000 (n=58 stations)
O3    : R²=-78122903439694109777502142464.000 ± 259104358242630619732897693696.000 (n=11 stations)

--- Training Info ---
Total time: 344.7 minutes (5.74 hours)
Average per model: 146.7 seconds

--- Files Saved ---
Location: /content/cnn_outputs
  - checkpoint_100.csv
  - checkpoint_40.csv
  - checkpoint_120.csv
  - pollutant_summary.csv
  - checkpoint_140.csv
  - checkpoint_20.csv
  - summary_stats.joblib
  - r2_distribution_cnn.png
  - checkpoint_60.csv
  - all_targets_results.csv
  - checkpoint_80.csv
```

