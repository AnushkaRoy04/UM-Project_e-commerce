# Project Instructions & Technical Specifications

## Nassau Candy Distributor: Geospatial Decision Intelligence & Factory Reallocation Platform
**Unified Mentor Machine Learning Internship**  
**Author**: Anushka Roy  
**Repository**: [AnushkaRoy04/UM-Project_e-commerce](https://github.com/AnushkaRoy04/UM-Project_e-commerce)  

---

## 1. Project Overview & Business Case

**Nassau Candy Distributor** is a leading wholesale manufacturer and distributor of specialty confectionery and foods across the United States. Operations leadership identified high cross-country shipping distances, prolonged delivery lead times, and freight cost inflation caused by **static legacy manufacturing allocation rules**.

This project builds a complete **Geospatial Decision Support and Optimization System** that:
1. Calculates geodesic transit distances between manufacturing hubs and customer destinations across the continental US.
2. Identifies severe route bottleneck corridors using unsupervised clustering.
3. Quantifies freight logistics expenditure using an explicit distance-and-volume freight rate model.
4. Enforces manufacturing hub capacity limits with visual overload alerts.
5. Performs multi-criteria Pareto optimization balancing speed, cost, and workload capacity.
6. Deploys an executive operations dashboard with counterfactual what-if simulation and 24-month trend analysis.

---

## 2. Dataset Fields Specification (18 Columns)

The raw transactional dataset (`dataset/Nassau Candy Distributor.csv.xls`) contains **10,194 records** with zero missing values:

| Field Name | Data Type | Description & Domain Notes | Example Values |
| :--- | :---: | :--- | :--- |
| **`Row ID`** | Integer | Unique transaction row identifier | `1, 2, 3, ...` |
| **`Order ID`** | String | Unique order reference code | `US-2021-103800-CHO-MIL-31000` |
| **`Order Date`** | String | Date order was placed (DD-MM-YYYY format) | `03-01-2024` to `31-12-2025` |
| **`Ship Date`** | String | Date order was shipped (DD-MM-YYYY format) | `30-06-2026` to `28-06-2030` |
| **`Ship Mode`** | String | Fulfillment logistics SLA tier | `Standard Class`, `Second Class`, `First Class`, `Same Day` |
| **`Customer ID`** | Integer | Unique commercial customer account number | `103800`, `112326` |
| **`Country/Region`**| String | Destination sovereign nation | `United States` |
| **`City`** | String | Destination municipal delivery location | `Houston`, `Naperville`, `Los Angeles` |
| **`State/Province`**| String | Destination US state or territory (59 unique) | `Texas`, `Illinois`, `California` |
| **`Postal Code`** | String | Destination US ZIP postal code | `77095`, `60540` |
| **`Division`** | String | High-level product division | `Chocolate`, `Sugar`, `Other` |
| **`Region`** | String | Macro sales territory | `Interior`, `Atlantic`, `Gulf`, `Pacific` |
| **`Product ID`** | String | Unique product SKU inventory code | `CHO-MIL-31000`, `CHO-NUT-13000` |
| **`Product Name`** | String | Confectionery line name (15 SKUs) | `Wonka Bar - Milk Chocolate` |
| **`Sales`** | Float | Total gross sales revenue ($) | `$1.25` to `$260.00` |
| **`Units`** | Integer | Total units ordered | `1` to `14` |
| **`Gross Profit`** | Float | Gross profit from order ($) | `$0.25` to `$130.00` |
| **`Cost`** | Float | Manufacturing production cost ($) | `$0.50` to `$130.00` |

---

## 3. Manufacturing Hub Reference Master

| Hub Facility Name | Latitude | Longitude | City, State | Regional Hub Role | Rated Capacity |
| :--- | :---: | :---: | :--- | :--- | :---: |
| **Lot's O' Nuts** | `32.881893` | `-111.768036` | Casa Grande, AZ | West Coast / Pacific | 3,500 orders |
| **Wicked Choccy's** | `32.076176` | `-81.088371` | Savannah, GA | East Coast / Atlantic | 3,500 orders |
| **Sugar Shack** | `48.119140` | `-96.181150` | Thief River Falls, MN | Upper Midwest / Interior | 600 orders |
| **Secret Factory** | `41.446333` | `-90.565487` | Rock Island, IL | Central Midwest / Interior | 1,800 orders |
| **The Other Factory** | `35.117500` | `-89.971107` | Memphis, TN | Mid-South / Gulf Corridor | 1,600 orders |

---

## 4. Products & Baseline Legacy Assignments

| Product Confectionery SKU | Division | Baseline Assigned Hub | Network Volume Share |
| :--- | :---: | :--- | :---: |
| **Wonka Bar - Milk Chocolate** | Chocolate | Wicked Choccy's (GA) | 2,137 orders (21.0%) |
| **Wonka Bar - Scrumdiddlyumptious** | Chocolate | Lot's O' Nuts (AZ) | 2,064 orders (20.2%) |
| **Wonka Bar - Triple Dazzle Caramel** | Chocolate | Wicked Choccy's (GA) | 2,015 orders (19.8%) |
| **Wonka Bar - Fudge Mallows** | Chocolate | Lot's O' Nuts (AZ) | 1,818 orders (17.8%) |
| **Wonka Bar - Nutty Crunch Surprise** | Chocolate | Lot's O' Nuts (AZ) | 1,810 orders (17.8%) |
| **Wonka Gum** | Other | Secret Factory (IL) | 120 orders (1.2%) |
| **Kazookles** | Other | The Other Factory (TN) | 96 orders (0.9%) |
| **Lickable Wallpaper** | Other | Secret Factory (IL) | 94 orders (0.9%) |
| **Laffy Taffy** | Sugar | Sugar Shack (MN) | 10 orders (0.1%) |
| **SweeTARTS** | Sugar | Sugar Shack (MN) | 10 orders (0.1%) |
| **Fizzy Lifting Drinks** | Other | Sugar Shack (MN) | 6 orders (0.1%) |
| **Nerds** | Sugar | Sugar Shack (MN) | 4 orders (0.0%) |
| **Hair Toffee** | Sugar | The Other Factory (TN) | 4 orders (0.0%) |
| **Everlasting Gobstopper** | Sugar | Secret Factory (IL) | 3 orders (0.0%) |
| **Fun Dip** | Sugar | Sugar Shack (MN) | 3 orders (0.0%) |

---

## 5. Mandatory Graded Rubric Improvements

This build directly satisfies all evaluator feedback criteria:
1. **Visible Mathematical Validation**: Formulations, intermediate values, and automated sanity reconciliation badges are shown on-screen.
2. **Dedicated In-App Assumptions & Methodology Panel**: Full technical documentation embedded directly within the dashboard.
3. **Explicit Freight Logistics Cost Model**: Explicit rate-per-mile $\times$ distance $\times$ volume scaling model with real-time slider controls.
4. **Per-Hub Capacity Constraints**: Rated limits per factory with dynamic utilization tracking and visual overload alert banners.
5. **24-Month Historical Trend Analysis**: Full monthly and quarterly time-series tracking volume, mileage wasted, freight expenditure, and gross margins.
6. **Multi-Factor Weight Sensitivity**: Interactive 3-slider Pareto weighting matrix with live trade-off curves.
7. **Coherent Executive Design System**: Unified design tokens, responsive layout, glassmorphic metric cards, and zero raw errors.
