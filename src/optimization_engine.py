"""
Multi-Criteria Pareto Optimization & Policy Reallocation Engine
Author: Anushka Roy
Unified Mentor Machine Learning Internship
"""

import os
import pandas as pd
import numpy as np
from src.config import (
    FACTORIES,
    PROCESSED_DATA_DIR,
    DEFAULT_FREIGHT_RATE_PER_MILE,
    DEFAULT_WEIGHT_DISTANCE,
    DEFAULT_WEIGHT_COST,
    DEFAULT_WEIGHT_CAPACITY
)
from src.geo_engine import haversine_distance


def compute_multicriteria_score(
    distance_reduction_pct,
    margin_pct,
    capacity_penalty=0.0,
    weight_distance=DEFAULT_WEIGHT_DISTANCE,
    weight_cost=DEFAULT_WEIGHT_COST,
    weight_capacity=DEFAULT_WEIGHT_CAPACITY
):
    """
    Computes normalized multi-objective optimization score (0 to 100).
    Score = w_d * Distance_Reduction_% + w_c * Normalized_Margin - w_b * Capacity_Penalty

    Weights are dynamically normalized to sum to 1.0.
    """
    total_w = weight_distance + weight_cost + weight_capacity
    if total_w > 0:
        w_d = weight_distance / total_w
        w_c = weight_cost / total_w
        w_b = weight_capacity / total_w
    else:
        w_d, w_c, w_b = 0.5, 0.3, 0.2

    # Scale margin (baseline average is ~65%)
    norm_margin = min(100.0, max(0.0, margin_pct))
    norm_dist = min(100.0, max(0.0, distance_reduction_pct))

    score = (w_d * norm_dist) + (w_c * norm_margin) - (w_b * capacity_penalty)
    return round(max(0.0, float(score)), 2)


def generate_optimization_recommendations(
    enriched_df,
    weight_distance=DEFAULT_WEIGHT_DISTANCE,
    weight_cost=DEFAULT_WEIGHT_COST,
    weight_capacity=DEFAULT_WEIGHT_CAPACITY,
    freight_rate_per_mile=DEFAULT_FREIGHT_RATE_PER_MILE,
    min_mileage_savings_threshold=50.0
):
    """
    Analyzes every unique Product SKU x Destination Region order corridor
    and computes Pareto-optimal hub reassignments.

    Returns:
        pd.DataFrame: Ranked policy recommendations with metrics and rationale.
    """
    # Group by Product Name, Region, and Current Factory
    grouped = enriched_df.groupby(['Product Name', 'Region', 'Current Factory']).agg(
        Order_Count=('Row ID', 'count'),
        Total_Units=('Units', 'sum'),
        Total_Sales=('Sales', 'sum'),
        Total_Cost=('Cost', 'sum'),
        Total_Gross_Profit=('Gross Profit', 'sum'),
        Avg_Current_Distance=('Transit Distance (Miles)', 'mean'),
        Avg_Optimal_Distance=('Minimum Distance (Miles)', 'mean'),
        Total_Miles_Saved=('Potential Distance Saved (Miles)', 'sum'),
        Avg_Margin_Pct=('Gross Margin %', 'mean'),
        Cust_Lat=('Customer Latitude', 'mean'),
        Cust_Lon=('Customer Longitude', 'mean')
    ).reset_index()

    # Precalculate baseline hub load share for capacity penalty
    hub_loads = enriched_df['Closest Factory'].value_counts(normalize=True).to_dict()

    recommendations = []

    for _, row in grouped.iterrows():
        product = row['Product Name']
        region = row['Region']
        curr_factory = row['Current Factory']
        order_count = int(row['Order_Count'])
        c_lat = row['Cust_Lat']
        c_lon = row['Cust_Lon']
        curr_dist = row['Avg_Current_Distance']
        margin = row['Avg_Margin_Pct']

        candidate_evaluations = []

        for candidate_hub, hub_info in FACTORIES.items():
            h_lat = hub_info['latitude']
            h_lon = hub_info['longitude']
            cand_dist = haversine_distance(h_lat, h_lon, c_lat, c_lon)

            dist_saved = curr_dist - cand_dist
            dist_reduction_pct = (dist_saved / curr_dist * 100.0) if curr_dist > 0 else 0.0

            # Capacity penalty if hub load is high (>25% share of total network)
            load_share = hub_loads.get(candidate_hub, 0.0)
            capacity_penalty = max(0.0, (load_share - 0.25) * 50.0)

            score = compute_multicriteria_score(
                distance_reduction_pct=dist_reduction_pct,
                margin_pct=margin,
                capacity_penalty=capacity_penalty,
                weight_distance=weight_distance,
                weight_cost=weight_cost,
                weight_capacity=weight_capacity
            )

            candidate_evaluations.append({
                "Hub": candidate_hub,
                "Distance": cand_dist,
                "Distance_Saved": dist_saved,
                "Distance_Reduction_Pct": dist_reduction_pct,
                "Score": score
            })

        # Rank candidates by multi-criteria score
        cand_df = pd.DataFrame(candidate_evaluations).sort_values(by='Score', ascending=False)
        best_candidate = cand_df.iloc[0]
        recommended_hub = best_candidate['Hub']

        is_reassignment = (
            recommended_hub != curr_factory and
            best_candidate['Distance_Saved'] >= min_mileage_savings_threshold
        )

        final_hub = recommended_hub if is_reassignment else curr_factory
        final_dist = best_candidate['Distance'] if is_reassignment else curr_dist
        final_reduction_pct = best_candidate['Distance_Reduction_Pct'] if is_reassignment else 0.0
        miles_saved_total = round(best_candidate['Distance_Saved'] * order_count, 0) if is_reassignment else 0.0
        freight_dollars_saved = round(miles_saved_total * freight_rate_per_mile, 2)

        recommendations.append({
            "Confectionery SKU": product,
            "Destination Region": region,
            "Current Hub": curr_factory,
            "Recommended Hub": final_hub,
            "Policy Action": "Reassign Hub" if is_reassignment else "Maintain Baseline",
            "Orders": order_count,
            "Current Distance (mi)": round(curr_dist, 1),
            "Recommended Distance (mi)": round(final_dist, 1),
            "Distance Reduction (%)": round(max(0.0, final_reduction_pct), 1),
            "Freight Miles Saved": int(max(0, miles_saved_total)),
            "Est. Freight Savings ($)": freight_dollars_saved,
            "Gross Margin (%)": round(margin, 1),
            "Optimization Score": best_candidate['Score']
        })

    recs_df = pd.DataFrame(recommendations)
    recs_df = recs_df.sort_values(
        by=["Policy Action", "Freight Miles Saved"],
        ascending=[True, False]
    ).reset_index(drop=True)
    return recs_df


def compute_weight_sensitivity_curve(enriched_df, steps=10):
    """
    Computes sensitivity curve across a grid of distance vs. capacity balance weights.
    Returns DataFrame showing how freight miles saved and reallocations respond to weights.
    """
    results = []
    weight_steps = np.linspace(0.1, 0.9, steps)

    for w_dist in weight_steps:
        w_cap = 1.0 - w_dist
        w_cost = 0.0

        recs = generate_optimization_recommendations(
            enriched_df,
            weight_distance=w_dist,
            weight_cost=w_cost,
            weight_capacity=w_cap
        )

        actionable = recs[recs['Policy Action'] == 'Reassign Hub']
        total_miles_saved = actionable['Freight Miles Saved'].sum()
        reassigned_orders = actionable['Orders'].sum()

        results.append({
            "Distance Weight (%)": round(w_dist * 100, 0),
            "Capacity Balance Weight (%)": round(w_cap * 100, 0),
            "Actionable Policies": len(actionable),
            "Reassigned Order Volume": reassigned_orders,
            "Total Miles Saved": total_miles_saved,
            "Total Freight Dollars Saved ($)": round(total_miles_saved * DEFAULT_FREIGHT_RATE_PER_MILE, 0)
        })

    return pd.DataFrame(results)
