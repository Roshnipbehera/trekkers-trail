# Trekkers Trail (OrbitLink)
### Satellite-Assisted Himalayan Safety Platform & Cloud-Native Ground-Station Downlink Optimizer

**Author:** Roshni Priyadarshini Behera (USN: 25MSFDR009)  
**Programme:** M.Sc. Full Stack Development (Semester I)  
**Institution:** JAIN (Deemed-to-be University)  
**Guide / Faculty:** DR. M N NACHAPPA  
**Academic Assessment:** Continuous Assessment 2 (CA2 / Activity 2)  
**Academic Year:** 2026-27  
**Unified Subjects Covered:**
1. **Algorithm Design** (0/1 Knapsack Coding Challenge & Benchmarking)
2. **Cloud Computing** (Cloud Architecture, Virtualization, IaaS/PaaS/SaaS, Docker)
3. **Statistics & Data Analytics** (Atmospheric Telemetry Dataset, ML Regression, Evaluation Metrics)
4. **Server Side Scripting** (Enterprise Express.js Routing Application & Swagger API)

---

## 🛰️ 1. Executive Summary

**OrbitLink** is an enterprise-grade, cloud-native satellite data downlink optimization and citizen observation platform. Low Earth Orbit (LEO) Earth-observation satellites (e.g., Sentinel-2A, Landsat-9) pass over ground-station antennas for brief 8-to-12 minute contact windows, offering limited radio bandwidth capacity ($W$).

Simultaneously, regular citizens and emergency teams submit observation requests for:
- 🚨 **Disaster Watch:** Rapid wildfire perimeters, flood basin levels, and cyclone surges.
- 🌾 **Agriculture & Small Farm Health:** Soil moisture, crop drought indices, and vegetation health.
- 🏔️ **Trail Check & Hiker Safety:** Mountain pass snowpack, avalanche risks, and trail obstructions.
- 🔭 **Citizen Space Radar:** Stargazing, satellite pass countdowns, and space enthusiasm.

OrbitLink uses **Machine Learning** to forecast atmospheric rain fade and signal loss over the antenna dish, dynamically adjusting the available pass capacity. It then executes a **Space-Optimized 0/1 Knapsack Algorithm** to maximize the total value of dispatched citizen imagery without exceeding the downlink bandwidth ceiling.

---

## 📚 2. Subject-Wise Deliverables & Academic Mapping

```text
activity-2/
├── backend/                       # Subject 4: Server Side Scripting (Express.js)
│   ├── src/
│   │   ├── algorithms/            # Subject 1: Algorithm Design (0/1 Knapsack Engine)
│   │   │   ├── knapsack.js        # 4 Implementations (Recursive, Memo, 2D DP, 1D DP)
│   │   │   ├── knapsack.test.js   # Automated Test Harness (10 test cases)
│   │   │   └── benchmark.js       # Microsecond Performance & Memory Profiler
│   │   ├── controllers/           # Modular Controllers
│   │   ├── routes/                # Versioned Express Routes (/api/v1/...)
│   │   ├── middleware/            # Zod Validation, Helmet, Rate Limiter, Error Handler
│   │   ├── services/              # ML Native Inference & Satellite Services
│   │   ├── public/                # Interactive Citizen Web Dashboard & Leaflet Map
│   │   ├── swagger.yaml           # OpenAPI 3.0 Specification
│   │   └── server.js              # Express Application Entry Point
│   └── package.json
│
├── analytics/                     # Subject 3: Statistics & Data Analytics
│   ├── dataset/                   # Real-World Calibrated Telemetry (2,500 samples)
│   ├── model/                     # Exported Trained Model Parameters (trained_model.json)
│   ├── train_model.py             # Multi-Model ML Pipeline (Linear, Tree, Random Forest)
│   └── report.md                  # Comprehensive Statistical Report & Metrics Table
│
└── cloud/                         # Subject 2: Cloud Computing
    ├── Dockerfile                 # Multi-Stage Lightweight Container (node:20-alpine)
    ├── docker-compose.yml         # Container Orchestration (API + Redis + Postgres)
    └── cloud-architecture.md      # Cloud Models (IaaS/PaaS/SaaS), Security & Scalability
```

---

### Module 1: Algorithm Design (CA2 Requirement)
* **Problem Formulation:**
  $$\text{Maximize } \sum_{i=1}^{n} v_i x_i \quad \text{subject to} \quad \sum_{i=1}^{n} w_i x_i \le W, \quad x_i \in \{0, 1\}$$
* **4 Implemented Variations (`src/algorithms/knapsack.js`):**
  1. *Recursive Brute Force:* $\mathcal{O}(2^n)$ time, $\mathcal{O}(n)$ stack space.
  2. *Top-Down Memoization:* $\mathcal{O}(n \cdot W)$ time and space.
  3. *Bottom-Up 2D Dynamic Programming:* $\mathcal{O}(n \cdot W)$ time and space.
  4. *Space-Optimized 1D Rolling Array DP:* $\mathcal{O}(n \cdot W)$ time, optimized to $\mathcal{O}(W)$ space.
* **Empirical Benchmark Results:**

| Items ($n$) | Capacity ($W$) | Recursive $\mathcal{O}(2^n)$ | Memoized $\mathcal{O}(nW)$ | 2D DP $\mathcal{O}(nW)$ | 1D Rolling DP $\mathcal{O}(nW, W \text{ mem})$ |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **10** | 50 | 0.22 ms | 0.40 ms | 0.31 ms | **0.34 ms** |
| **20** | 100 | 2.24 ms | 0.26 ms | 0.21 ms | **0.12 ms** |
| **25** | 150 | Skipped ($\mathcal{O}(2^{25})$) | 0.16 ms | 0.35 ms | **0.22 ms** |
| **100** | 500 | Skipped | 12.80 ms | 0.56 ms | **0.54 ms** |
| **500** | 2000 | Skipped | Skipped (OOM) | 8.88 ms | **5.63 ms** |
| **1000** | 5000 | Skipped | Skipped (OOM) | 41.76 ms | **21.59 ms** |

---

### Module 2: Cloud Computing (CA2 Requirement)
* **Cloud Architecture:** Hybrid Cloud linking edge ground-station antennas with public cloud compute clusters.
* **Service Models:** 
  - **SaaS:** OrbitLink Web Dashboard (Citizen Portal + Ground Station Manager).
  - **PaaS:** Managed Docker container execution (AWS ECS / Fargate, Google Cloud Run).
  - **IaaS:** Virtual Private Cloud (VPC), isolated subnets, security groups, and block storage.
* **Security & Scalability:** Multi-stage Docker container running as non-root user (`USER node`), Redis caching for $\mathcal{O}(1)$ memoized pass computation, and rate-limited API protection.

---

### Module 3: Statistics & Data Analytics (CA2 Requirement)
* **Dataset:** 2,500 calibrated atmospheric transmission observations based on ITU-R P.618 and NOAA Earth telecommunication standards.
* **Features:** Elevation Look Angle ($^\circ$), Downlink Frequency (GHz), Rain Rate (mm/hr), Cloud Liquid Water ($\text{g/m}^3$), Ambient Temperature ($^\circ\text{C}$), Humidity (%).
* **Target:** Electromagnetic Signal Attenuation in Decibels ($A_{\text{dB}}$).
* **Comparative Model Evaluation:**

| Model Algorithm | RMSE (dB) | MAE (dB) | $R^2$ Score (Accuracy) |
| :--- | :--- | :--- | :--- |
| Multiple Linear Regression | 2.8107 | 1.6710 | 0.7026 |
| Ridge Regression (L2) | 2.8107 | 1.6710 | 0.7026 |
| Decision Tree Regressor | 1.3023 | 0.6416 | 0.9361 |
| **Random Forest Regressor (Best)** | **1.1577** | **0.4630** | **0.9495 (95.0%)** |

---

### Module 4: Server-Side Scripting (Express.js) (CA2 Requirement)
* **Modular Routing:** Clean Controller-Service-Repository architecture.
* **REST Endpoints:**
  - `GET  /api/health` — Cloud orchestrator health check and memory telemetry.
  - `GET  /api/v1/citizen/requests` — Retrieve queued citizen observation tasks.
  - `POST /api/v1/citizen/requests` — Submit new request (Zod schema validated).
  - `POST /api/v1/downlink/optimize` — Run 0/1 Knapsack optimization on pass window.
  - `POST /api/v1/analytics/predict-loss` — Real-time ML atmospheric attenuation prediction.
  - `GET  /api/v1/analytics/model-stats` — Model metrics, evaluation, and feature drivers.
  - `GET  /api/v1/satellite/passes` — Live upcoming LEO satellite contact passes.
* **API Documentation:** Interactive OpenAPI 3.0 Swagger UI hosted at `/api/docs`.

---

## ⚡ 3. How to Run & Verify the Project

### Prerequisites
* **Node.js:** v18+ (tested on v24.13.1)
* **Python:** 3.10+ (tested on Python 3.14.3 with `scikit-learn`, `pandas`, `numpy`)

### 1. Algorithm Tests & Benchmarks
```bash
cd backend

# Run automated test harness (10 unit tests covering edge cases & triage)
npm run test:algorithm

# Run microsecond complexity profiler
npm run benchmark:algorithm
```

### 2. Machine Learning Training & Report
```bash
cd analytics

# Run EDA, train 4 regression models, evaluate metrics, and export model.json
python train_model.py
```

### 3. Start the Express.js Application & Citizen Dashboard
```bash
cd backend

# Start the server
npm start
```

* **Interactive Web App:** Open `http://localhost:5000` in any browser.
* **Swagger API Docs:** Open `http://localhost:5000/api/docs`.
* **Health Endpoint:** Open `http://localhost:5000/api/health`.

---
*Built for M.Sc. Full Stack Development — Activity 2 (CA2).*

