# Executive Summary: Nassau Candy Shipping Optimization & Factory Reallocation System

**Prepared For**: Executive Leadership, Operations Stakeholders & Evaluators  
**Project**: Unified Mentor Machine Learning Internship  
**Author**: Anushka Roy  
**Repository**: [AnushkaRoy04/UM-Project_e-commerce](https://github.com/AnushkaRoy04/UM-Project_e-commerce)  
**Evaluation Date**: 2026  

---

## 1. Strategic Context & The Operational Challenge

Nassau Candy Distributor fulfills orders across the continental United States from five specialized confectionery manufacturing facilities:
1. **Lot's O' Nuts** (Casa Grande, Arizona) — West Coast Production Hub
2. **Wicked Choccy's** (Savannah, Georgia) — East Coast Production Hub
3. **Sugar Shack** (Thief River Falls, Minnesota) — Upper Midwest Production Hub
4. **Secret Factory** (Rock Island, Illinois) — Central Midwest Production Hub
5. **The Other Factory** (Memphis, Tennessee) — Mid-South / Gulf Production Hub

### The Historical Bottleneck
Historically, product lines were assigned to factories via **rigid legacy rules** rather than customer demand geography:
- **Massive Inefficiency**: Over **68.8% of historical shipments (7,011 orders)** were fulfilled by a distant factory when an active, closer production facility existed.
- **Cross-Country Hauling**: High-volume chocolate bars made exclusively in Georgia (*Wonka Bar - Milk Chocolate*, *Wonka Bar - Triple Dazzle Caramel*) were hauled 2,200+ miles to California customers, while nut-based bars in Arizona (*Wonka Bar - Scrumdiddlyumptious*, *Fudge Mallows*) were hauled 2,000+ miles to New York and Florida.
- **Severe Workload Imbalance**: Two coastal factories handled **96.5% of total company orders**, leaving central facilities in Illinois, Tennessee, and Minnesota virtually idle.
- **Freight Cost Inflation**: Incurred **12.55 million freight transit miles**, wasting over **$13.6 million in avoidable carrier transportation costs**.

---

## 2. Decision Intelligence & Multi-Objective Solution

We designed and built an independent **Geospatial Decision Intelligence and Capacity-Guarded Optimization Platform**:
1. **Geodesic Haversine Engine**: Calculates exact physical transit distance from every candidate manufacturing hub to customer delivery coordinates across 542 cities and 59 states/territories.
2. **Visible Mathematical Validation & Reconciliation**: Displays underlying algebraic formulas, intermediate step values, and automated sanity reconciliation badges (0 negative distance anomalies, 100% order reconciliation).
3. **Explicit Parametric Freight Cost Model**: Computes outbound carrier logistics expenditure using an explicit distance-and-volume model ($\text{Freight Cost} = \text{Distance} \times \text{Rate}_{\text{mile}} \times [1 + 0.05 \times (\text{Units} - 1)]$) with interactive rate controls.
4. **Per-Hub Capacity Guardrails**: Enforces factory throughput ceilings and fires prominent visual overload alerts whenever a reallocation scenario exceeds 100% capacity.
5. **24-Month Historical Trend Analysis**: Evaluates monthly and quarterly time-series patterns (Jan 2024 – Dec 2025), isolating seasonal volume surges (Q3-Q4 holiday spikes).
6. **Multi-Criteria Optimization & Sensitivity Matrix**: 3-slider Pareto weighting system balancing distance reduction ($w_d$), freight cost ($w_c$), and capacity balance ($w_b$) with live trade-off curves.
7. **Counterfactual What-If Simulator**: Real-time evaluation of all 5 candidate hubs for any custom SKU, state, shipping mode, and order volume.

---

## 3. Key Quantitative Findings & Reconciled Impact

| Strategic Network KPI | Historical Baseline | Optimized Policy | Quantified Business Impact |
| :--- | :---: | :---: | :--- |
| **Average Transit Distance** | 1,231.4 miles / order | 496.9 miles / order | **-59.65% Reduction (-734.5 miles/order)** |
| **Total Network Freight Miles** | 12,553,210 miles | 5,065,878 miles | **7,487,332 Miles Eliminated** |
| **Suboptimal Shipment Share** | 68.78% (7,011 orders) | 0.00% (0 orders) | **100% Suboptimal Routes Resolved** |
| **Est. Network Freight Spend ($1.75/mi)** | $22,864,120 | $9,226,712 | **$13,637,408 Net Operating Savings** |
| **Operating Margin Impact** | Protected (65.9%) | Expanded (+9.6 pts) | **Zero Margin Erosion; Substantial Net Gain** |
| **Sanity Reconciliation Check** | 10,194 orders | 10,194 orders | **100% Reconciled (0 Negative Anomalies)** |

---

## 4. Top Actionable Reallocation Policies

1. **Reallocate Pacific Region Wonka Bar - Milk Chocolate & Triple Dazzle Caramel to Lot's O' Nuts (AZ)**:
   - *Baseline*: Fulfilled from Savannah, GA (~2,144 miles).
   - *Proposed*: Fulfilled from Casa Grande, AZ (~500 miles).
   - *Impact*: **-76.6% average transit distance**, eliminating **2,192,408 freight miles** and saving **$3.98M in freight spend**.
2. **Reallocate Atlantic Region Wonka Bar - Scrumdiddlyumptious, Fudge Mallows & Nutty Crunch to Wicked Choccy's (GA)**:
   - *Baseline*: Fulfilled from Casa Grande, AZ (~2,050 miles).
   - *Proposed*: Fulfilled from Savannah, GA (~640 miles).
   - *Impact*: **-68.6% average transit distance**, eliminating **2,258,469 freight miles** and saving **$4.11M in freight spend**.
3. **Reallocate Interior Region Nutty Crunch Orders to The Other Factory (TN)**:
   - *Baseline*: Fulfilled from Casa Grande, AZ (~1,540 miles).
   - *Proposed*: Fulfilled from Memphis, TN (~244 miles).
   - *Impact*: **-84.2% transit distance reduction**, saving **456,528 freight miles**.
4. **Implement Capacity Overflow Rerouting to Secret Factory (IL)**:
   - Activates underutilized Midwestern capacity to absorb central demand without crossing coastal boundaries.

---

## 5. Software & Analytical Deliverables

1. **Production Streamlit Dashboard**: `app/main_dashboard.py` (8 modules, responsive design tokens, glassmorphism cards, interactive simulators).
2. **Modular Python Engine**: `src/` (`config.py`, `geo_engine.py`, `data_pipeline.py`, `cost_capacity_engine.py`, `optimization_engine.py`, `simulation_engine.py`, `route_analytics.py`, `report_generator.py`).
3. **Comprehensive Documentation Suite**: `docs/` (`PROJECT_INSTRUCTION.md`, `UNDERSTAND_PROJECT.md`, `METHODOLOGY_AND_ASSUMPTIONS.md`).
4. **Formal Academic Deliverables**: `reports/` (`EXECUTIVE_SUMMARY.md`, `RESEARCH_PAPER.md`, `PROJECT_REPORT.tex`, and compiled `PROJECT_REPORT.pdf`).
