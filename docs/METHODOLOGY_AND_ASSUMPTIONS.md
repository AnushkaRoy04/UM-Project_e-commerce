# Assumptions & Engineering Methodology Ledger

**Project**: Nassau Candy Factory Reallocation & Shipping Optimization  
**Author**: Anushka Roy  
**Unified Mentor Machine Learning Internship**  

This document serves as the formal engineering reference ledger detailing every operational hypothesis, parametric assumption, and mathematical boundary condition utilized in the platform.

---

## 1. Network Topology & Facility Operational Assumptions

1. **Fixed Facility Footprint**:
   - The manufacturing network is strictly modeled on the five operational facilities specified in the brief: Casa Grande (AZ), Savannah (GA), Thief River Falls (MN), Rock Island (IL), and Memphis (TN).
   - Coordinates represent the surveyed centroids of each production compound.
2. **SKU Portability & Production Line Tooling**:
   - The platform assumes multi-site tooling feasibility: that packaging lines and molding equipment for solid and nut chocolate varieties can be co-located or expanded across facilities with standard capital expenditure.
   - Quality control and ingredient supply chains (cocoa liquor, peanuts, sugar) are assumed equivalent across all five manufacturing nodes.
3. **Rated Operating Capacities**:
   - *Lot's O' Nuts* (AZ): 3,500 orders/year.
   - *Wicked Choccy's* (GA): 3,500 orders/year.
   - *Secret Factory* (IL): 1,800 orders/year.
   - *The Other Factory* (TN): 1,600 orders/year.
   - *Sugar Shack* (MN): 600 orders/year.
   - Facilities operating beyond 100% of rated capacity encounter bottleneck penalties and trigger automated re-routing recommendations.

---

## 2. Geospatial Routing & Geodesic Formulations

1. **Haversine Great-Circle Formulation**:
   - Physical distance is computed via the spherical Haversine formula assuming a mean Earth radius $R = 3,958.8$ statute miles.
   - Great-circle distances represent the theoretical minimum transit mileage. In road freight logistics, actual highway mileage typically exhibits a circuity factor of $1.15$ to $1.20$.
2. **Customer Destination Hierarchy**:
   - Customer shipping destinations are resolved via a two-tier precision hierarchy:
     - Tier 1: 50+ Major US Metropolitan centroids for city-level precision.
     - Tier 2: State geographic centroids for broader territorial coverage.
     - Tier 3: Contiguous US geographic centroid fallback (`39.8283° N, -98.5795° W`).

---

## 3. Freight Delivery Logistics Cost Model

1. **Baseline Freight Rate**:
   - Outbound commercial freight is modeled at a baseline rate of **$1.75 per mile** for standard Less-Than-Truckload (LTL) confectionery distribution.
   - The rate is exposed as an interactive slider ($1.00 – $3.00/mi) in the dashboard to support inflationary sensitivity analysis.
2. **Volume & Weight Scaling Factor**:
   - Order freight cost scales with order unit count via the factor: $[1 + 0.05 \times (\text{Units} - 1)]$.
   - This accounts for incremental pallet space, dimensional weight, and handling surcharges for multi-case shipments.
3. **Margin Preservation**:
   - Freight logistics savings are treated as reductions in operational fulfillment costs, directly expanding net operating profit margins while preserving baseline gross margins.

---

## 4. Multi-Criteria Optimization & Sensitivity Weights

1. **Normalized Multi-Objective Function**:
   - The objective function combines three competing corporate objectives:
     $$\text{Score} = w_d \cdot (\text{Distance Saved \%}) + w_c \cdot (\text{Normalized Margin \%}) - w_b \cdot (\text{Capacity Penalty})$$
   - Default weights: Distance $w_d = 0.50$, Cost $w_c = 0.30$, Capacity Balance $w_b = 0.20$.
   - Weights dynamically normalize such that $\sum w_i = 1.0$.
2. **Reassignment Threshold**:
   - A factory reassignment policy is only recommended if the proposed alternative facility eliminates at least **50 miles of transit distance** per order, avoiding frivolous reassignments for negligible mileage gains.

---

## 5. Data Hygiene & Reconciliation Standards

1. **Completeness**: All 10,194 records are parsed without dropping or imputing missing fields.
2. **Reconciliation Invariant**: Baseline transit miles minus optimized transit miles must strictly equal total mileage saved with zero negative savings anomalies.
3. **Temporal Bounds**: 24 consecutive months of order transactions from January 2024 through December 2025.
