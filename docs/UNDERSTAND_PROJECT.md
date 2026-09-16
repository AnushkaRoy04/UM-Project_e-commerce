# Master Technical Guide: Understanding the Nassau Candy Decision Intelligence Platform

**Author**: Anushka Roy  
**Project**: Unified Mentor Machine Learning Internship  
**Repository**: [AnushkaRoy04/UM-Project_e-commerce](https://github.com/AnushkaRoy04/UM-Project_e-commerce)  

---

## 1. System Architecture & High-Level Flow

The platform is designed around a clean separation of concerns:

```
[ Raw Transactions (10,194 Orders) ]
              │
              ▼
[ Geospatial Enrichment Engine ] ──► Haversine transit distances to all 5 candidate hubs
              │
              ▼
[ Cost & Capacity Engine ] ───────► Freight delivery cost model & factory capacity limits
              │
              ▼
[ Route Analytics & Trends ] ─────► K-Means bottleneck clustering & 24-month historical series
              │
              ▼
[ Multi-Criteria Optimizer ] ─────► 3-factor Pareto scoring (Distance vs. Cost vs. Capacity)
              │
              ▼
[ Executive Streamlit Dashboard ] ─► 8 interactive modules, glassmorphic UI & PDF exporter
```

---

## 2. Core Methodologies & Mathematical Foundations

### 2.1 Haversine Great-Circle Geodesics
Planar Euclidean distance calculations introduce massive distortion when computing cross-country freight lines across continental distances. The spherical Haversine formula measures great-circle distance along Earth's curvature:

$$d = 2 R \arcsin\left( \sqrt{\sin^2\left(\frac{\Delta\phi}{2}\right) + \cos(\phi_F)\cos(\phi_C)\sin^2\left(\frac{\Delta\lambda}{2}\right)} \right)$$

- $R = 3,958.8$ statute miles (Earth mean spherical radius).
- Coordinates $(\phi, \lambda)$ are converted to radians.
- Distance calculations are vectorized with NumPy for sub-millisecond execution over 10,000+ records.

### 2.2 Destination Coordinate Resolution Hierarchy
To resolve customer delivery locations with maximum geographic accuracy:
1. **Tier 1 (City-Level Resolution)**: Exact matches against 50+ major US metropolitan coordinates (e.g., Houston, Los Angeles, Chicago).
2. **Tier 2 (State Centroid Resolution)**: Accurate geographic center coordinates for all 50 US states and District of Columbia.
3. **Tier 3 (Continental Fallback)**: Geographic center of the contiguous United States (`39.8283° N, 98.5795° W`).

### 2.3 Explicit Freight Logistics Cost Model
Rather than using opaque percentages, the platform evaluates actual carrier freight economics via an explicit formula:

$$\text{Freight Spend} = d \times r_{\text{mile}} \times \left[ 1 + 0.05 \times (u - 1) \right]$$

- $d$: One-way transit distance in miles.
- $r_{\text{mile}}$: Freight rate per mile (default $\$1.75$/mi, adjustable $\$1.00 - \$3.00$).
- $u$: Order units ordered.
- Marginal unit factor ($0.05$) accounts for dimensional weight and LTL pallet volume surcharges.

### 2.4 Multi-Criteria Pareto Optimization
To balance delivery distance against factory capacity limits and profit margins:

$$\text{Score} = w_d \cdot \left(\frac{d_{\text{curr}} - d_{\text{rec}}}{d_{\text{curr}}} \times 100\right) + w_c \cdot \left(\frac{\text{Margin}}{\text{Margin}_{\text{base}}} \times 100\right) - w_b \cdot \text{Penalty}$$

- $w_d$: Distance Reduction Weight (Default 50%)
- $w_c$: Freight Cost / Margin Weight (Default 30%)
- $w_b$: Capacity Workload Balance Weight (Default 20%)
- Weights are automatically normalized: $\sum w_i = 1.0$.

---

## 3. Evaluator Improvements Summary

| Evaluator Criterion | Implementation Details |
| :--- | :--- |
| **Visible Formula Validation** | Metric cards feature expandable formula drawers with LaTeX equations, step-by-step arithmetic, and live sanity reconciliation badges. |
| **In-App Assumptions Panel** | Module 8 embeds the full engineering assumptions ledger into the running Streamlit dashboard. |
| **Delivery Cost Estimates** | Real-time dollar figures for baseline freight, optimized freight, and net savings, controlled by an interactive rate slider. |
| **Capacity Constraints & Overload Alerts** | Factory progress bars and prominent amber/red alert banners fire whenever simulated reallocations push a hub past 100% capacity. |
| **24-Month Trend Analysis** | Time-series charts tracking monthly and quarterly order density, mileage wasted, and seasonal demand peaks. |
| **Sensitivity Sliders** | 3 interactive sliders exposing distance, cost, and capacity weights with dynamic trade-off curves. |

---

## 4. Execution & CLI Commands

```bash
# 1. Run data ingestion, geospatial enrichment, and validation
python -m src.data_pipeline

# 2. Run multi-criteria optimization engine
python -m src.optimization_engine

# 3. Generate formal compiled PDF report
python -m src.report_generator

# 4. Launch interactive Streamlit executive dashboard
streamlit run app/main_dashboard.py
```
