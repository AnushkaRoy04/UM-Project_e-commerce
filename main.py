"""
Master CLI Orchestrator: Nassau Candy Supply Chain Optimization System
=============================================================================
Author: Anushka Roy
Repository: https://github.com/AnushkaRoy04/UM-Project_e-commerce
Unified Mentor Machine Learning Internship Project

Description:
------------
Executes the end-to-end data pipeline, multi-criteria optimization engine,
automated PDF report generation, and launches the Streamlit executive dashboard.

Usage:
------
    # Run full end-to-end pipeline and compile reports
    python main.py --all

    # Run specific stages
    python main.py --step data
    python main.py --step optimize
    python main.py --step report

    # Launch Streamlit dashboard directly
    python main.py --app
"""

import os
import sys
import argparse
import subprocess
import time

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.data_pipeline import run_pipeline
from src.optimization_engine import generate_optimization_recommendations
from src.report_generator import build_pdf_report
from src.config import PROCESSED_DATA_DIR, REPORTS_DIR


def print_banner():
    """Prints system executive header."""
    print("=" * 80)
    print("  NASSAU CANDY DISTRIBUTOR: GEOSPATIAL DECISION INTELLIGENCE PLATFORM")
    print("  Executive Operations, Freight Optimization & Hub Capacity Guardrails")
    print("  Author: Anushka Roy | Unified Mentor Machine Learning Internship")
    print("  Repository: AnushkaRoy04/UM-Project_e-commerce")
    print("=" * 80)


def step_data():
    """Step 1: Ingestion, cleaning, Haversine geospatial calculations."""
    print("\n" + "=" * 80)
    print(">> [STEP 1/3] INGESTION, DATA CLEANING & GEOSPATIAL ENRICHMENT")
    print("=" * 80)
    start = time.time()
    enriched_df, sanity = run_pipeline()
    elapsed = time.time() - start
    print(f">> [STEP 1 COMPLETED] Processed {len(enriched_df):,} orders in {elapsed:.2f}s.")
    print(f">> Reconciled: {sanity['is_mathematically_reconciled']} | Total Miles Saved: {sanity['total_miles_saved']:,.0f} (-{sanity['distance_reduction_pct']}%)")
    return enriched_df


def step_optimize(enriched_df=None):
    """Step 2: Multi-criteria Pareto optimization."""
    print("\n" + "=" * 80)
    print(">> [STEP 2/3] MULTI-CRITERIA PARETO OPTIMIZATION POLICY GENERATION")
    print("=" * 80)
    start = time.time()
    if enriched_df is None:
        data_path = os.path.join(PROCESSED_DATA_DIR, "nassau_candy_enriched.csv")
        if not os.path.exists(data_path):
            enriched_df, _ = run_pipeline()
        else:
            import pandas as pd
            enriched_df = pd.read_csv(data_path)

    recs_df = generate_optimization_recommendations(enriched_df)
    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
    out_path = os.path.join(PROCESSED_DATA_DIR, "top_recommendations.csv")
    recs_df.to_csv(out_path, index=False)
    elapsed = time.time() - start
    print(f">> [STEP 2 COMPLETED] Generated {len(recs_df):,} policy rules in {elapsed:.2f}s.")
    print(f">> Saved recommendations to: {out_path}")
    return recs_df


def step_report():
    """Step 3: Automated formal PDF report compilation."""
    print("\n" + "=" * 80)
    print(">> [STEP 3/3] FORMAL PDF PROJECT REPORT COMPILATION")
    print("=" * 80)
    start = time.time()
    pdf_path = build_pdf_report()
    elapsed = time.time() - start
    print(f">> [STEP 3 COMPLETED] Compiled PDF report in {elapsed:.2f}s.")
    print(f">> Artifact: {pdf_path}")
    return pdf_path


def launch_app():
    """Launches the Streamlit executive web application."""
    print("\n" + "=" * 80)
    print(">> LAUNCHING STREAMLIT EXECUTIVE DASHBOARD...")
    print(">> Open your browser at: http://localhost:8501")
    print("=" * 80)
    app_path = os.path.join("app", "main_dashboard.py")
    subprocess.run([sys.executable, "-m", "streamlit", "run", app_path])


def main():
    parser = argparse.ArgumentParser(description="Nassau Candy Supply Chain Decision Intelligence Platform")
    parser.add_argument("--all", action="store_true", help="Run all pipeline stages and generate PDF report")
    parser.add_argument("--step", choices=["data", "optimize", "report"], help="Run a specific pipeline step")
    parser.add_argument("--app", action="store_true", help="Launch the Streamlit executive dashboard")

    args = parser.parse_args()

    if len(sys.argv) == 1 or args.all:
        print_banner()
        df = step_data()
        step_optimize(df)
        step_report()
        print("\n" + "=" * 80)
        print(">> ALL PIPELINE DELIVERABLES COMPILED SUCCESSFULLY!")
        print(">> To view interactive dashboard: python main.py --app")
        print("=" * 80)
    elif args.step == "data":
        print_banner()
        step_data()
    elif args.step == "optimize":
        print_banner()
        step_optimize()
    elif args.step == "report":
        print_banner()
        step_report()
    elif args.app:
        print_banner()
        launch_app()


if __name__ == "__main__":
    main()
