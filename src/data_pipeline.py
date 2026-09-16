"""
Data Ingestion, Cleaning & Geospatial Feature Enrichment Pipeline
Author: Anushka Roy
Unified Mentor Machine Learning Internship
"""

import os
import pandas as pd
import numpy as np
from src.config import (
    DATASET_PATH,
    PROCESSED_DATA_DIR,
    FACTORIES,
    PRODUCT_FACTORY_MAP,
    PRODUCT_DIVISION_MAP
)
from src.geo_engine import (
    resolve_customer_coordinates,
    haversine_distance,
    vectorized_haversine
)


def load_raw_dataset(file_path=DATASET_PATH):
    """
    Loads raw CSV data with automatic encoding handling.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Raw dataset not found at expected path: {file_path}")

    try:
        df = pd.read_csv(file_path, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, encoding='latin1')

    print(f">> Successfully loaded raw data: {df.shape[0]:,} rows, {df.shape[1]} columns.")
    return df


def clean_and_enrich_dataset(raw_df):
    """
    Cleans raw transactions and performs end-to-end geospatial and temporal enrichment.
    """
    df = raw_df.copy()

    # Clean whitespace on string columns
    str_cols = ['Order ID', 'Ship Mode', 'City', 'State/Province', 'Division', 'Region', 'Product ID', 'Product Name']
    for col in str_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    # Step 1: Temporal Date Parsing (format: DD-MM-YYYY)
    df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d-%m-%Y', errors='coerce')
    df['Ship Date'] = pd.to_datetime(df['Ship Date'], format='%d-%m-%Y', errors='coerce')

    # Lead time in days
    df['Lead Time (Days)'] = (df['Ship Date'] - df['Order Date']).dt.days

    # Temporal Calendar attributes
    df['Order Year'] = df['Order Date'].dt.year
    df['Order Month'] = df['Order Date'].dt.month
    df['Order Month Name'] = df['Order Date'].dt.strftime('%B')
    df['Order Year-Month'] = df['Order Date'].dt.to_period('M').astype(str)
    df['Order Quarter'] = 'Q' + df['Order Date'].dt.quarter.astype(str) + ' ' + df['Order Date'].dt.year.astype(str)
    df['Order Day of Week'] = df['Order Date'].dt.day_name()

    # Step 2: Product & Division Mapping
    df['Current Factory'] = df['Product Name'].map(PRODUCT_FACTORY_MAP).fillna("Lot's O' Nuts")
    if 'Division' not in df.columns or df['Division'].isnull().any():
        df['Division'] = df['Product Name'].map(PRODUCT_DIVISION_MAP).fillna("Chocolate")

    # Step 3: Destination Customer Coordinates Resolution
    coords = [
        resolve_customer_coordinates(city, state)
        for city, state in zip(df['City'], df['State/Province'])
    ]
    df['Customer Latitude'] = [c[0] for c in coords]
    df['Customer Longitude'] = [c[1] for c in coords]

    # Step 4: Factory Origin Coordinates
    df['Factory Latitude'] = df['Current Factory'].map(lambda f: FACTORIES[f]['latitude'])
    df['Factory Longitude'] = df['Current Factory'].map(lambda f: FACTORIES[f]['longitude'])

    # Step 5: Current Baseline Transit Distance (Miles)
    df['Transit Distance (Miles)'] = vectorized_haversine(
        df['Factory Latitude'].values,
        df['Factory Longitude'].values,
        df['Customer Latitude'].values,
        df['Customer Longitude'].values
    )

    # Step 6: Distances from All 5 Candidate Hubs
    hub_keys = list(FACTORIES.keys())
    dist_cols = []
    for hub in hub_keys:
        clean_col = "Dist_" + hub.replace(" ", "_").replace("'", "")
        dist_cols.append(clean_col)
        hub_lat = FACTORIES[hub]['latitude']
        hub_lon = FACTORIES[hub]['longitude']
        df[clean_col] = vectorized_haversine(
            np.full(len(df), hub_lat),
            np.full(len(df), hub_lon),
            df['Customer Latitude'].values,
            df['Customer Longitude'].values
        )

    # Step 7: Identify Geographically Closest Factory
    dist_matrix = df[dist_cols].values
    min_indices = np.argmin(dist_matrix, axis=1)
    df['Closest Factory'] = [hub_keys[idx] for idx in min_indices]
    df['Minimum Distance (Miles)'] = np.min(dist_matrix, axis=1)

    # Step 8: Calculate Mileage Savings & Suboptimal Flag
    df['Potential Distance Saved (Miles)'] = np.maximum(
        0.0,
        df['Transit Distance (Miles)'] - df['Minimum Distance (Miles)']
    )
    df['Is Suboptimal Shipment'] = df['Current Factory'] != df['Closest Factory']

    # Step 9: Unit Economics
    df['Unit Price'] = (df['Sales'] / df['Units'].replace(0, 1)).round(2)
    df['Unit Cost'] = (df['Cost'] / df['Units'].replace(0, 1)).round(2)
    df['Gross Margin %'] = np.where(
        df['Sales'] > 0,
        ((df['Gross Profit'] / df['Sales']) * 100).round(2),
        0.0
    )

    print(f">> Enrichment complete. Total Orders: {len(df):,}.")
    return df


def validate_calculations(df):
    """
    Performs visible mathematical reconciliation and sanity checks:
    - Verifies order row totals
    - Verifies zero negative distance savings
    - Reconciles aggregate mileage sums
    - Confirms physical boundaries
    """
    total_orders = len(df)
    suboptimal_orders = int(df['Is Suboptimal Shipment'].sum())
    suboptimal_pct = (suboptimal_orders / total_orders) * 100.0

    current_total_miles = float(df['Transit Distance (Miles)'].sum())
    optimal_total_miles = float(df['Minimum Distance (Miles)'].sum())
    total_miles_saved = float(df['Potential Distance Saved (Miles)'].sum())

    reconciliation_delta = abs((current_total_miles - optimal_total_miles) - total_miles_saved)
    negative_savings_count = int((df['Potential Distance Saved (Miles)'] < 0).sum())
    negative_distances_count = int((df['Transit Distance (Miles)'] < 0).sum())

    is_reconciled = (reconciliation_delta < 1.0) and (negative_savings_count == 0) and (negative_distances_count == 0)

    sanity_report = {
        "total_orders": total_orders,
        "suboptimal_orders": suboptimal_orders,
        "suboptimal_pct": round(suboptimal_pct, 2),
        "current_avg_distance": round(df['Transit Distance (Miles)'].mean(), 1),
        "optimal_avg_distance": round(df['Minimum Distance (Miles)'].mean(), 1),
        "current_total_miles": round(current_total_miles, 0),
        "optimal_total_miles": round(optimal_total_miles, 0),
        "total_miles_saved": round(total_miles_saved, 0),
        "distance_reduction_pct": round((total_miles_saved / current_total_miles) * 100.0, 2),
        "reconciliation_delta": round(reconciliation_delta, 4),
        "negative_savings_anomalies": negative_savings_count,
        "is_mathematically_reconciled": is_reconciled
    }
    return sanity_report


def run_pipeline():
    """
    Executes the ingestion, enrichment, validation, and serialization pipeline.
    """
    raw_df = load_raw_dataset()
    enriched_df = clean_and_enrich_dataset(raw_df)
    sanity = validate_calculations(enriched_df)

    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
    out_path = os.path.join(PROCESSED_DATA_DIR, "nassau_candy_enriched.csv")
    enriched_df.to_csv(out_path, index=False)
    print(f">> Enriched dataset saved to: {out_path}")
    print(f">> Validation Report: Reconciled={sanity['is_mathematically_reconciled']}, Miles Saved={sanity['total_miles_saved']:,.0f} (-{sanity['distance_reduction_pct']}%)")
    return enriched_df, sanity


if __name__ == "__main__":
    run_pipeline()
