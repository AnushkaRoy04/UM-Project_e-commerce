"""
Counterfactual What-If Scenario Reallocation Simulator
Author: Anushka Roy
Unified Mentor Machine Learning Internship
"""

import pandas as pd
import numpy as np
from src.config import (
    FACTORIES,
    PRODUCT_FACTORY_MAP,
    DEFAULT_FREIGHT_RATE_PER_MILE,
    FREIGHT_UNIT_SCALING
)
from src.geo_engine import (
    resolve_customer_coordinates,
    haversine_distance
)
from src.cost_capacity_engine import compute_order_freight_cost


def estimate_lead_time_days(distance_miles, ship_mode="Standard Class"):
    """
    Estimates delivery lead time in days based on transit distance and ship mode.
    Base processing + distance transit + mode SLA.
    """
    mode_offsets = {
        "Same Day": 1.0,
        "First Class": 2.5,
        "Second Class": 4.0,
        "Standard Class": 5.5
    }
    base_days = mode_offsets.get(ship_mode, 5.0)
    transit_days = (distance_miles / 450.0)  # Standard average commercial freight daily transit ~450 miles
    return round(base_days + transit_days, 1)


def simulate_counterfactual_order(
    product_name,
    state,
    city=None,
    ship_mode="Standard Class",
    units=3,
    freight_rate_per_mile=DEFAULT_FREIGHT_RATE_PER_MILE,
    custom_capacities=None
):
    """
    Simulates fulfilling an order from all 5 candidate manufacturing hubs.

    Returns:
        pd.DataFrame: Comparative performance across all 5 hubs.
        dict: Baseline order context.
    """
    current_hub = PRODUCT_FACTORY_MAP.get(product_name, "Lot's O' Nuts")
    dest_lat, dest_lon = resolve_customer_coordinates(city, state)

    # Calculate baseline metrics
    curr_h_lat = FACTORIES[current_hub]['latitude']
    curr_h_lon = FACTORIES[current_hub]['longitude']
    baseline_distance = haversine_distance(curr_h_lat, curr_h_lon, dest_lat, dest_lon)
    baseline_lead_time = estimate_lead_time_days(baseline_distance, ship_mode)
    baseline_freight_cost = compute_order_freight_cost(
        baseline_distance, units=units, rate_per_mile=freight_rate_per_mile
    )

    # Typical product unit economics
    unit_price = 14.0
    unit_cost_prod = 5.0
    order_revenue = round(unit_price * units, 2)
    order_prod_cost = round(unit_cost_prod * units, 2)

    candidate_results = []

    for hub_name, hub_info in FACTORIES.items():
        h_lat = hub_info['latitude']
        h_lon = hub_info['longitude']
        distance = haversine_distance(h_lat, h_lon, dest_lat, dest_lon)

        dist_saved = round(baseline_distance - distance, 1)
        dist_saved_pct = round((dist_saved / baseline_distance) * 100.0, 1) if baseline_distance > 0 else 0.0

        lead_time = estimate_lead_time_days(distance, ship_mode)
        lead_time_saved = round(baseline_lead_time - lead_time, 1)

        freight_cost = compute_order_freight_cost(
            distance, units=units, rate_per_mile=freight_rate_per_mile
        )
        freight_saved = round(baseline_freight_cost - freight_cost, 2)

        # Net profit after manufacturing and freight
        total_order_cost = round(order_prod_cost + freight_cost, 2)
        net_profit = round(order_revenue - total_order_cost, 2)
        net_margin_pct = round((net_profit / order_revenue) * 100.0, 1) if order_revenue > 0 else 0.0

        is_current = (hub_name == current_hub)

        # Capacity threshold check
        rated_cap = custom_capacities.get(hub_name, hub_info['rated_capacity_orders']) if custom_capacities else hub_info['rated_capacity_orders']
        capacity_status = "Available" if rated_cap > 1000 else "Constrained"

        candidate_results.append({
            "Factory": hub_name,
            "Hub Location": f"{hub_info['city']}, {hub_info['state']}",
            "Is Current Assignment": is_current,
            "Distance (Miles)": distance,
            "Distance Saved (Miles)": dist_saved,
            "Distance Reduction (%)": max(0.0, dist_saved_pct),
            "Estimated Lead Time (Days)": lead_time,
            "Lead Time Saved (Days)": lead_time_saved,
            "Freight Cost ($)": freight_cost,
            "Freight Dollars Saved ($)": freight_saved,
            "Total Order Cost ($)": total_order_cost,
            "Net Profit ($)": net_profit,
            "Net Operating Margin (%)": net_margin_pct,
            "Capacity Status": capacity_status
        })

    sim_df = pd.DataFrame(candidate_results)
    sim_df = sim_df.sort_values(by="Distance (Miles)", ascending=True).reset_index(drop=True)

    baseline_info = {
        "product_name": product_name,
        "destination": f"{city + ', ' if city else ''}{state}",
        "current_hub": current_hub,
        "baseline_distance": baseline_distance,
        "baseline_lead_time": baseline_lead_time,
        "baseline_freight_cost": baseline_freight_cost,
        "units": units,
        "revenue": order_revenue
    }

    return sim_df, baseline_info
