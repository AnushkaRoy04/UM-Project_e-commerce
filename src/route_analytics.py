"""
Unsupervised Route Clustering & 24-Month Historical Trend Analytics Engine
Author: Anushka Roy
Unified Mentor Machine Learning Internship
"""

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from src.config import DEFAULT_FREIGHT_RATE_PER_MILE


def perform_kmeans_route_clustering(df, n_clusters=3, random_state=42):
    """
    Performs unsupervised K-Means route clustering to isolate shipping corridors:
    - Local / High-Efficiency Corridors
    - Moderate Regional Routes
    - Severe Cross-Country Bottlenecks (Prime Reallocation Targets)

    Features:
        - Transit Distance (Miles)
        - Units
        - Cost
        - Sales
    """
    df_clustered = df.copy()
    feature_cols = ['Transit Distance (Miles)', 'Units', 'Cost', 'Sales']
    X = df_clustered[feature_cols].copy()

    # Standardize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Fit K-Means
    kmeans = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=10)
    df_clustered['Cluster_ID'] = kmeans.fit_predict(X_scaled)

    # Rank clusters by average transit distance
    cluster_ranks = (
        df_clustered.groupby('Cluster_ID')['Transit Distance (Miles)']
        .mean()
        .sort_values()
        .index.tolist()
    )

    cluster_name_map = {
        cluster_ranks[0]: "Low-Distance Local Route",
        cluster_ranks[1]: "Moderate Regional Corridor",
        cluster_ranks[2]: "High-Latency Bottleneck Corridor"
    }
    df_clustered['Cluster_Label'] = df_clustered['Cluster_ID'].map(cluster_name_map)

    # Cluster summary
    summary = df_clustered.groupby('Cluster_Label').agg(
        Order_Count=('Row ID', 'count'),
        Avg_Distance_Miles=('Transit Distance (Miles)', 'mean'),
        Avg_Units=('Units', 'mean'),
        Avg_Cost=('Cost', 'mean'),
        Avg_Gross_Profit=('Gross Profit', 'mean'),
        Suboptimal_Share=('Is Suboptimal Shipment', 'mean')
    ).reset_index()

    total_orders = len(df_clustered)
    summary['Order_Share_%'] = (summary['Order_Count'] / total_orders * 100.0).round(1)
    summary['Suboptimal_Share_%'] = (summary['Suboptimal_Share'] * 100.0).round(1)
    summary['Avg_Distance_Miles'] = summary['Avg_Distance_Miles'].round(1)
    summary['Avg_Cost'] = summary['Avg_Cost'].round(2)
    summary['Avg_Gross_Profit'] = summary['Avg_Gross_Profit'].round(2)
    summary = summary.drop(columns=['Suboptimal_Share'])

    return df_clustered, summary


def compute_historical_monthly_trends(df, freight_rate_per_mile=DEFAULT_FREIGHT_RATE_PER_MILE):
    """
    Analyzes historical performance over the entire 24-month horizon (Jan 2024 to Dec 2025).
    Computes monthly volume, baseline vs. optimal transit miles, freight expenditure, and margins.
    """
    monthly = df.groupby('Order Year-Month').agg(
        Order_Count=('Row ID', 'count'),
        Total_Units=('Units', 'sum'),
        Total_Sales=('Sales', 'sum'),
        Total_Production_Cost=('Cost', 'sum'),
        Total_Gross_Profit=('Gross Profit', 'sum'),
        Baseline_Total_Miles=('Transit Distance (Miles)', 'sum'),
        Optimal_Total_Miles=('Minimum Distance (Miles)', 'sum'),
        Total_Miles_Saved=('Potential Distance Saved (Miles)', 'sum'),
        Suboptimal_Orders=('Is Suboptimal Shipment', 'sum'),
        Avg_Distance=('Transit Distance (Miles)', 'mean')
    ).reset_index()

    monthly['Freight_Cost_Baseline ($)'] = (monthly['Baseline_Total_Miles'] * freight_rate_per_mile).round(2)
    monthly['Freight_Cost_Optimal ($)'] = (monthly['Optimal_Total_Miles'] * freight_rate_per_mile).round(2)
    monthly['Freight_Savings ($)'] = (monthly['Total_Miles_Saved'] * freight_rate_per_mile).round(2)

    monthly['Gross_Margin_%'] = np.where(
        monthly['Total_Sales'] > 0,
        (monthly['Total_Gross_Profit'] / monthly['Total_Sales'] * 100.0).round(2),
        0.0
    )
    monthly['Mileage_Reduction_%'] = np.where(
        monthly['Baseline_Total_Miles'] > 0,
        (monthly['Total_Miles_Saved'] / monthly['Baseline_Total_Miles'] * 100.0).round(1),
        0.0
    )
    monthly['Suboptimal_Share_%'] = (monthly['Suboptimal_Orders'] / monthly['Order_Count'] * 100.0).round(1)

    return monthly


def compute_quarterly_trends(df, freight_rate_per_mile=DEFAULT_FREIGHT_RATE_PER_MILE):
    """
    Computes quarterly aggregated trends across the 2-year transactional horizon.
    """
    quarterly = df.groupby(['Order Year', 'Order Quarter']).agg(
        Order_Count=('Row ID', 'count'),
        Total_Sales=('Sales', 'sum'),
        Total_Gross_Profit=('Gross Profit', 'sum'),
        Baseline_Miles=('Transit Distance (Miles)', 'sum'),
        Optimal_Miles=('Minimum Distance (Miles)', 'sum'),
        Miles_Saved=('Potential Distance Saved (Miles)', 'sum')
    ).reset_index()

    quarterly['Miles_Saved_%'] = (quarterly['Miles_Saved'] / quarterly['Baseline_Miles'] * 100.0).round(1)
    quarterly['Est_Freight_Savings ($)'] = (quarterly['Miles_Saved'] * freight_rate_per_mile).round(0)
    quarterly['Gross_Margin_%'] = (quarterly['Total_Gross_Profit'] / quarterly['Total_Sales'] * 100.0).round(1)

    return quarterly


def get_top_bottleneck_corridors(df, top_n=10):
    """
    Identifies the top N most inefficient Factory -> Customer State corridors
    ranked by total transit miles wasted.
    """
    routes = df.groupby(['Current Factory', 'State/Province', 'Region']).agg(
        Order_Count=('Row ID', 'count'),
        Avg_Distance=('Transit Distance (Miles)', 'mean'),
        Avg_Optimal=('Minimum Distance (Miles)', 'mean'),
        Total_Miles_Saved=('Potential Distance Saved (Miles)', 'sum'),
        Closer_Available_Share=('Is Suboptimal Shipment', 'mean')
    ).reset_index()

    routes['Closer_Available_%'] = (routes['Closer_Available_Share'] * 100.0).round(1)
    routes['Miles_Wasted_Per_Order'] = (routes['Avg_Distance'] - routes['Avg_Optimal']).round(1)
    routes['Avg_Distance'] = routes['Avg_Distance'].round(1)
    routes['Avg_Optimal'] = routes['Avg_Optimal'].round(1)

    routes = routes.sort_values(by='Total_Miles_Saved', ascending=False).head(top_n).reset_index(drop=True)
    return routes
