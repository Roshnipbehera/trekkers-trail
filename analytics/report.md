# CA2 – Statistics & Data Analytics Mini Project Report

## 1. Project Overview & Problem Statement
* **Project Name**: OrbitLink - Atmospheric Signal Attenuation Prediction for LEO Satellites
* **Objective**: Predict electromagnetic signal attenuation ($A_{dB}$) experienced during satellite downlinks to ground station antennas due to atmospheric absorption, rain fade, and cloud liquid water content.
* **Significance**: Enables the OrbitLink downlink scheduler to adjust bandwidth capacity ($W$) dynamically before executing the 0/1 Knapsack optimization algorithm.

---

## 2. Dataset Description
* **Source**: Synthesized following empirical **ITU-R P.618-13 (Propagation data and prediction methods required for Earth-space telecommunication systems)** and NOAA meteorological telemetry standards.
* **Instances**: 2500 observations across varied atmospheric conditions.
* **Input Features**:
  1. `elevation_angle_deg`: Ground station antenna look angle ($10^\circ$ to $85^\circ$).
  2. `frequency_ghz`: Downlink radio frequency band ($8.4	ext{ GHz}$ X-band, $14.2	ext{ GHz}$ Ku-band, $26.5	ext{ GHz}$ Ka-band).
  3. `rain_rate_mm_hr`: Precipitation intensity ($0$ to $75	ext{ mm/hr}$).
  4. `cloud_liquid_water_g_m3`: Cloud density ($0$ to $3.5	ext{ g/m}^3$).
  5. `surface_temp_c`: Ambient surface temperature ($-5^\circ	ext{C}$ to $40^\circ	ext{C}$).
  6. `relative_humidity_pct`: Atmospheric relative humidity ($20\%$ to $98\%$).
* **Target Variable**:
  * `signal_attenuation_db`: Total atmospheric transmission path loss in decibels (dB).

---

## 3. Machine Learning Algorithms Evaluated
1. **Multiple Linear Regression (Parametric Baseline)**:
   $$\hat{y} = eta_0 + \sum_{i=1}^{p} eta_i X_i$$
2. **Ridge Regression (L2 Regularization)**:
   $$\min_eta ||y - Xeta||_2^2 + lpha ||eta||_2^2$$
3. **Decision Tree Regressor (Non-Parametric)**:
   Splits feature space into hyper-rectangles minimizing Mean Squared Error.
4. **Random Forest Regressor (Ensemble Bootstrap Aggregation)**:
   $B = 100$ bagged trees with random feature subspacing at each node.

---

## 4. Model Performance & Comparative Evaluation

| Model Algorithm | RMSE (dB) | MAE (dB) | $R^2$ Score |
| :--- | :--- | :--- | :--- |
| Multiple Linear Regression | 2.8107 | 1.671 | 0.7026 |
| Ridge Regression | 2.8107 | 1.671 | 0.7026 |
| Decision Tree Regressor | 1.3023 | 0.6416 | 0.9361 |
| **Random Forest Regressor (Best)** | **1.1577** | **0.463** | **0.9495** |

---

## 5. Key Findings & Insights
1. **Dominant Signal Loss Driver**: Precipitation rate (`rain_rate_mm_hr`) and downlink frequency (`frequency_ghz`) account for over **68.7%** of total model feature importance.
2. **Elevation Angle Non-Linearity**: Low elevation angles ($<20^\circ$) dramatically lengthen the atmospheric slant path ($1/\sin\theta$), causing severe attenuation spikes.
3. **Random Forest Superiority**: The non-linear ensemble achieved an outstanding **$R^2 = 0.9495**$, confirming that atmospheric attenuation exhibits strong non-linear interactions between frequency and rain rate.

---
*Report generated for M.Sc. Full Stack Development - Activity 2 (CA2).*
