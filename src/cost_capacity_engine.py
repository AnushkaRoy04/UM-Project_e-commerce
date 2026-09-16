"""
Freight Logistics Cost Model & Hub Capacity Guardrail Engine
Author: Anushka Roy
Unified Mentor Machine Learning Internship
"""

import pandas as pd
import numpy as np
from src.config import (
    FACTORIES,
    DEFAULT_FREIGHT_RATE_PER_MILE,
    FREIGHT_UNIT_SCALING
)


def compute_order_freight_cost(distance_miles, units=1, rate_per_mile=DEFAULT_FREIGHT_RATE_PER_MILE, unit_scaling=FREIGHT_UNIT_SCALING):
    """
    Computes delivery freight cost using an explicit parametric model:
    Cost = Distance * Rate_per_mile * (1 + unit_scaling * (Units - 1))

    Parameters:
        distance_miles: One-way transit distance in miles
        units: Number of units in order
        rate_per_mile: Cost per mile in USD
        unit_scaling: Marginal cost increase per additional unit

    Returns:
        Freight delivery cost in USD (rounded to 2 decimal places).
    """
    unit_multiplier = 1.0 + max(0, units - 1) * unit_scaling
    return round(float(distance_miles) * float(rate_per_mile) * unit_multiplier, 2)


def compute_network_freight_economics(df, rate_per_mile=DEFAULT_FREIGHT_RATE_PER_MILE):
    """
    Calculates total network freight economics comparing baseline vs. optimized allocations.

    Returns:
        dict: Detailed financial metrics, formulas, intermediate figures, and reconciliation check.
    """
    # Vectorized freight calculations
    units_factor = 1.0 + (df['Units'].values - 1) * FREIGHT_UNIT_SCALING

    baseline_freight = df['Transit Distance (Miles)'].values * rate_per_mile * units_factor
    optimized_freight = df['Minimum Distance (Miles)'].values * rate_per_mile * units_factor
    freight_saved = np.maximum(0.0, baseline_freight - optimized_freight)

    total_sales = float(df['Sales'].sum())
    total_prod_cost = float(df['Cost'].sum())
    baseline_gross_profit = float(df['Gross Profit'].sum())

    total_base_freight = float(np.sum(baseline_freight))
    total_opt_freight = float(np.sum(optimized_freight))
    total_freight_saved = float(np.sum(freight_saved))

    # Net profit after freight
    baseline_net_operating_profit = baseline_gross_profit - total_base_freight
    optimized_net_operating_profit = baseline_gross_profit - total_opt_freight
    net_operating_margin_base = (baseline_net_operating_profit / total_sales) * 100.0 if total_sales > 0 else 0.0
    net_operating_margin_opt = (optimized_net_operating_profit / total_sales) * 100.0 if total_sales > 0 else 0.0

    freight_reduction_pct = (total_freight_saved / total_base_freight * 100.0) if total_base_freight > 0 else 0.0

    return {
        "rate_per_mile": rate_per_mile,
        "total_sales": round(total_sales, 2),
        "total_production_cost": round(total_prod_cost, 2),
        "baseline_gross_profit": round(baseline_gross_profit, 2),
        "baseline_gross_margin_pct": round((baseline_gross_profit / total_sales) * 100.0, 2),
        "total_baseline_freight": round(total_base_freight, 2),
        "total_optimized_freight": round(total_opt_freight, 2),
        "total_freight_saved": round(total_freight_saved, 2),
        "freight_reduction_pct": round(freight_reduction_pct, 2),
        "baseline_net_operating_profit": round(baseline_net_operating_profit, 2),
        "optimized_net_operating_profit": round(optimized_net_operating_profit, 2),
        "net_operating_margin_base": round(net_operating_margin_base, 2),
        "net_operating_margin_opt": round(net_operating_margin_opt, 2),
        "operating_margin_expansion_points": round(net_operating_margin_opt - net_operating_margin_base, 2),
        "formula_description": f"Freight = Distance (mi) × ${rate_per_mile:.2f}/mi × [1 + 0.05 × (Units - 1)]"
    }


def analyze_hub_capacity_utilization(df, custom_capacities=None):
    """
    Evaluates order volume workload distribution across all 5 hubs
    under baseline policy vs. unconstrained closest-hub reallocation.

    Flags over-capacity hubs and calculates utilization metrics.
    """
    hub_capacities = {}
    for hub, info in FACTORIES.items():
        if custom_capacities and hub in custom_capacities:
            hub_capacities[hub] = custom_capacities[hub]
        else:
            hub_capacities[hub] = info["rated_capacity_orders"]

    total_orders = len(df)
    baseline_counts = df['Current Factory'].value_counts().to_dict()
    optimal_counts = df['Closest Factory'].value_counts().to_dict()

    hub_analysis = []
    overload_warnings = []

    for hub in FACTORIES.keys():
        rated_cap = hub_capacities.get(hub, 2000)
        base_vol = baseline_counts.get(hub, 0)
        opt_vol = optimal_counts.get(hub, 0)

        base_share = round((base_vol / total_orders) * 100.0, 1)
        opt_share = round((opt_vol / total_orders) * 100.0, 1)

        base_util = round((base_vol / rated_cap) * 100.0, 1)
        opt_util = round((opt_vol / rated_cap) * 100.0, 1)

        vol_delta = opt_vol - base_vol
        vol_growth_pct = round((vol_delta / base_vol) * 100.0, 1) if base_vol > 0 else 0.0

        is_overloaded = opt_vol > rated_cap
        overload_excess = max(0, opt_vol - rated_cap)

        if is_overloaded:
            status = "CRITICAL OVERLOAD"
            status_color = "#F43F5E"
            overload_warnings.append({
                "hub": hub,
                "rated_capacity": rated_cap,
                "projected_volume": opt_vol,
                "excess_orders": overload_excess,
                "utilization_pct": opt_util,
                "location": f"{FACTORIES[hub]['city']}, {FACTORIES[hub]['state']}"
            })
        elif opt_util >= 80.0:
            status = "HIGH UTILIZATION"
            status_color = "#F59E0B"
        else:
            status = "OPTIMAL / SAFE"
            status_color = "#10B981"

        hub_analysis.append({
            "Factory": hub,
            "Location": f"{FACTORIES[hub]['city']}, {FACTORIES[hub]['state']}",
            "Rated Capacity (Orders)": rated_cap,
            "Baseline Volume": base_vol,
            "Baseline Share (%)": base_share,
            "Baseline Util (%)": base_util,
            "Reallocated Volume": opt_vol,
            "Reallocated Share (%)": opt_share,
            "Reallocated Util (%)": opt_util,
            "Volume Delta": vol_delta,
            "Volume Growth (%)": vol_growth_pct,
            "Status": status,
            "Status Color": status_color,
            "Is Overloaded": is_overloaded
        })

    analysis_df = pd.DataFrame(hub_analysis)
    return analysis_df, overload_warnings


def balanced_capacity_allocation(df, custom_capacities=None):
    """
    Executes a capacity-constrained reallocation:
    Assigns orders to the closest available hub that has NOT exceeded its capacity ceiling.
    If the closest hub is full, overflows to the next closest candidate hub.
    """
    hub_capacities = {}
    for hub, info in FACTORIES.items():
        if custom_capacities and hub in custom_capacities:
            hub_capacities[hub] = custom_capacities[hub]
        else:
            hub_capacities[hub] = info["rated_capacity_orders"]

    # Candidate distance columns
    hub_list = list(FACTORIES.keys())
    col_map = {hub: f"Dist_{hub.replace(' ', '_').replace(chr(39), '')}" for hub in hub_list}

    current_hub_counts = {hub: 0 for hub in hub_list}
    assigned_hubs = []
    assigned_distances = []

    # Sort orders by highest savings priority so critical orders get nearest hub first
    df_sorted = df.sort_values(by='Potential Distance Saved (Miles)', ascending=False).copy()

    for _, row in df_sorted.iterrows():
        # Get distances sorted
        dists = [(hub, row[col_map[hub]]) for hub in hub_list]
        dists.sort(key=lambda x: x[1])

        # Pick the nearest hub that has capacity remaining
        chosen_hub = None
        chosen_dist = None
        for hub, dist in dists:
            if current_hub_counts[hub] < hub_capacities[hub]:
                chosen_hub = hub
                chosen_dist = dist
                break

        # If all hubs full, fallback to closest regardless
        if chosen_hub is None:
            chosen_hub = dists[0][0]
            chosen_dist = dists[0][1]

        current_hub_counts[chosen_hub] += 1
        assigned_hubs.append(chosen_hub)
        assigned_distances.append(chosen_dist)

    df_sorted['Balanced_Assigned_Hub'] = assigned_hubs
    df_sorted['Balanced_Distance'] = assigned_distances
    df_sorted['Balanced_Miles_Saved'] = np.maximum(0.0, df_sorted['Transit Distance (Miles)'] - df_sorted['Balanced_Distance'])

    # Return to original index order
    return df_sorted.loc[df.index]
