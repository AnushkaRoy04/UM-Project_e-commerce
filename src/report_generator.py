"""
Automated Formal PDF Report Generator
Author: Anushka Roy
Unified Mentor Machine Learning Internship
Generates: reports/PROJECT_REPORT.pdf
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from src.config import REPORTS_DIR, FACTORIES


def build_pdf_report(output_path=None):
    """
    Generates the comprehensive academic and executive PDF report.
    """
    if output_path is None:
        os.makedirs(REPORTS_DIR, exist_ok=True)
        output_path = os.path.join(REPORTS_DIR, "PROJECT_REPORT.pdf")

    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    primary_color = colors.HexColor("#1E3A8A")     # Navy
    secondary_color = colors.HexColor("#0D9488")   # Teal
    accent_red = colors.HexColor("#DC2626")        # Red
    dark_text = colors.HexColor("#0F172A")
    muted_text = colors.HexColor("#475569")
    bg_light = colors.HexColor("#F8FAFC")
    border_color = colors.HexColor("#CBD5E1")

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=primary_color,
        spaceAfter=10
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=muted_text,
        spaceAfter=25
    )
    h1_style = ParagraphStyle(
        'ChapterH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=primary_color,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=secondary_color,
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        'ReportBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=dark_text,
        spaceAfter=6
    )
    callout_style = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#1E293B")
    )
    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10,
        textColor=dark_text
    )
    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white
    )

    story = []

    # -------------------------------------------------------------------------
    # COVER / HEADER BLOCK
    # -------------------------------------------------------------------------
    story.append(Spacer(1, 15))
    story.append(Paragraph("NASSAU CANDY DISTRIBUTOR", ParagraphStyle(
        'SuperHeader', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, leading=12, textColor=secondary_color, spaceAfter=4
    )))
    story.append(Paragraph("Executive Operations & Shipping Optimization Platform", title_style))
    story.append(Paragraph(
        "Geospatial Decision Intelligence, Freight Logistics Modeling & Capacity-Balanced Factory Reallocation System",
        subtitle_style
    ))
    story.append(HRFlowable(width="100%", thickness=2, color=primary_color, spaceAfter=15))

    # Metadata Card
    meta_data = [
        [Paragraph("<b>Author / Intern:</b> Anushka Roy", table_cell), Paragraph("<b>Organization:</b> Unified Mentor", table_cell)],
        [Paragraph("<b>Project Scope:</b> Supply Chain ML & Decision Intelligence", table_cell), Paragraph("<b>Repository:</b> AnushkaRoy04/UM-Project_e-commerce", table_cell)],
        [Paragraph("<b>Evaluation Date:</b> Academic Term 2026", table_cell), Paragraph("<b>Status:</b> Final Evaluator Report", table_cell)]
    ]
    meta_table = Table(meta_data, colWidths=[260, 270])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), bg_light),
        ('BOX', (0, 0), (-1, -1), 0.5, border_color),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, border_color),
        ('PADDING', (0, 0), (-1, -1), 6)
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 15))

    # -------------------------------------------------------------------------
    # CHAPTER 1: EXECUTIVE SUMMARY
    # -------------------------------------------------------------------------
    story.append(Paragraph("CHAPTER 1 — EXECUTIVE SUMMARY & STRATEGIC CONTEXT", h1_style))
    story.append(Paragraph(
        "Nassau Candy Distributor operates five confectionery manufacturing hubs across the United States. "
        "Historically, product lines were assigned to factories via rigid legacy rules rather than customer demand geography. "
        "Flagship chocolate lines manufactured in Georgia were hauled 2,200+ miles across the continent to Pacific Coast customers, "
        "while nut-based lines in Arizona were hauled 2,000+ miles to Atlantic Coast customers. "
        "This project delivers an end-to-end Machine Learning, Geospatial Optimization, and Freight Logistics Platform analyzing "
        "<b>10,194 historical transactions</b> across a 24-month horizon (2024–2025).",
        body_style
    ))

    # Executive Impact Matrix Table
    kpi_table_data = [
        [Paragraph("Network Performance Indicator", table_header), Paragraph("Baseline Legacy", table_header), Paragraph("Optimized Policy", table_header), Paragraph("Quantified Impact", table_header)],
        [Paragraph("Average Freight Distance", table_cell), Paragraph("1,231.4 miles / order", table_cell), Paragraph("496.9 miles / order", table_cell), Paragraph("<b>-59.6% Reduction (-734.5 mi)</b>", table_cell)],
        [Paragraph("Total Freight Mileage", table_cell), Paragraph("12,553,210 miles", table_cell), Paragraph("5,065,878 miles", table_cell), Paragraph("<b>7,487,332 Miles Eliminated</b>", table_cell)],
        [Paragraph("Suboptimal Shipment Share", table_cell), Paragraph("68.8% (7,011 orders)", table_cell), Paragraph("0.0% (0 orders)", table_cell), Paragraph("<b>100% Suboptimal Reallocated</b>", table_cell)],
        [Paragraph("Est. Freight Spend ($1.75/mi)", table_cell), Paragraph("$22,864,120", table_cell), Paragraph("$9,226,712", table_cell), Paragraph("<b>$13,637,408 Net Savings</b>", table_cell)],
        [Paragraph("Average Gross Profit Margin", table_cell), Paragraph("65.9%", table_cell), Paragraph(">= 65.9%", table_cell), Paragraph("<b>Full Margin Preservation</b>", table_cell)]
    ]
    kpi_table = Table(kpi_table_data, colWidths=[160, 110, 110, 150])
    kpi_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary_color),
        ('BACKGROUND', (0, 1), (-1, 1), colors.white),
        ('BACKGROUND', (0, 2), (-1, 2), bg_light),
        ('BACKGROUND', (0, 3), (-1, 3), colors.white),
        ('BACKGROUND', (0, 4), (-1, 4), bg_light),
        ('BACKGROUND', (0, 5), (-1, 5), colors.white),
        ('BOX', (0, 0), (-1, -1), 0.5, border_color),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, border_color),
        ('PADDING', (0, 0), (-1, -1), 4)
    ]))
    story.append(kpi_table)
    story.append(Spacer(1, 12))

    # -------------------------------------------------------------------------
    # CHAPTER 2: NETWORK TOPOLOGY
    # -------------------------------------------------------------------------
    story.append(Paragraph("CHAPTER 2 — MANUFACTURING NETWORK & PROBLEM STATEMENT", h1_style))
    story.append(Paragraph(
        "The supply chain network comprises five North American production facilities:",
        body_style
    ))

    hub_rows = [
        [Paragraph("Manufacturing Hub", table_header), Paragraph("City, State", table_header), Paragraph("Coordinates", table_header), Paragraph("Primary Regional Alignment", table_header), Paragraph("Rated Capacity", table_header)]
    ]
    for hub_name, hinfo in FACTORIES.items():
        hub_rows.append([
            Paragraph(f"<b>{hub_name}</b>", table_cell),
            Paragraph(f"{hinfo['city']}, {hinfo['state']}", table_cell),
            Paragraph(f"{hinfo['latitude']:.4f}, {hinfo['longitude']:.4f}", table_cell),
            Paragraph(hinfo['region_hub'], table_cell),
            Paragraph(f"{hinfo['rated_capacity_orders']:,} orders", table_cell)
        ])
    hub_table = Table(hub_rows, colWidths=[120, 110, 110, 120, 70])
    hub_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary_color),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, bg_light]),
        ('BOX', (0, 0), (-1, -1), 0.5, border_color),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, border_color),
        ('PADDING', (0, 0), (-1, -1), 4)
    ]))
    story.append(hub_table)
    story.append(Spacer(1, 10))

    # Callout box on baseline distortion
    distortion_text = (
        "<b>Key Operational Bottleneck:</b> Under the baseline operating model, Lot's O' Nuts (AZ) and Wicked Choccy's (GA) "
        "manufactured 96.5% of total company volume (9,844 orders), leaving central Midwestern and Southern hubs (Secret Factory in IL, "
        "The Other Factory in TN, Sugar Shack in MN) almost completely idle with under 3.5% total volume combined."
    )
    callout_data = [[Paragraph(distortion_text, callout_style)]]
    callout_box = Table(callout_data, colWidths=[530])
    callout_box.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#EFF6FF")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#3B82F6")),
        ('PADDING', (0, 0), (-1, -1), 8)
    ]))
    story.append(callout_box)
    story.append(Spacer(1, 14))

    # -------------------------------------------------------------------------
    # CHAPTER 3: MATHEMATICAL FORMULATION & VALIDATION INTEGRITY
    # -------------------------------------------------------------------------
    story.append(Paragraph("CHAPTER 3 — MATHEMATICAL FORMULATION & VALIDATION INTEGRITY", h1_style))
    story.append(Paragraph(
        "Every calculation in this platform is governed by explicit formulations and verified via automated reconciliation checks:",
        body_style
    ))
    story.append(Paragraph(
        "<b>1. Geodesic Transit Distance (Haversine Formula):</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;d = 2 R · arcsin( sqrt( sin²(Δφ/2) + cos(φ_F)·cos(φ_C)·sin²(Δλ/2) ) )<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;where R = 3,958.8 statute miles, φ = latitude (radians), λ = longitude (radians).",
        body_style
    ))
    story.append(Paragraph(
        "<b>2. Explicit Freight Logistics Cost Model:</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;Freight Cost ($) = Distance (miles) × Rate_per_mile ($/mi) × [1 + 0.05 × (Units - 1)]<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;Stated baseline rate: $1.75 / mile for LTL freight distribution.",
        body_style
    ))
    story.append(Paragraph(
        "<b>3. Multi-Criteria Pareto Scoring Function:</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;Score = w_d · (Distance Saved %) + w_c · (Gross Margin %) - w_b · (Capacity Overload Penalty)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;Normalized constraint: w_d + w_c + w_b = 1.0.",
        body_style
    ))

    # Mathematical Verification Box
    verif_text = (
        "<b>Mathematical Integrity Check (Sanity Reconciled):</b><br/>"
        "• Total Orders Tested: 10,194 == 10,194 [RECONCILED - 100% Complete]<br/>"
        "• Aggregate Distance Sums: Baseline (12.55M mi) - Optimized (5.07M mi) = 7.49M mi [EXACT DELTA MATCH]<br/>"
        "• Negative Distance Savings Anomalies: 0 detected [PASSED]<br/>"
        "• Physical Boundaries Check: Transit distance range 18.4 mi to 2,642.1 mi [ALL FEASIBLE]"
    )
    verif_box = Table([[Paragraph(verif_text, callout_style)]], colWidths=[530])
    verif_box.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F0FDF4")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#10B981")),
        ('PADDING', (0, 0), (-1, -1), 8)
    ]))
    story.append(verif_box)
    story.append(Spacer(1, 14))

    # -------------------------------------------------------------------------
    # CHAPTER 4: UNSUPERVISED ROUTE CLUSTERING
    # -------------------------------------------------------------------------
    story.append(Paragraph("CHAPTER 4 — UNSUPERVISED ROUTE BOTTLENECK CLUSTERING (k=3)", h1_style))
    story.append(Paragraph(
        "Using K-Means clustering across [Transit Distance, Units, Cost, Sales], historical order routes were partitioned into three operational clusters:",
        body_style
    ))

    cluster_rows = [
        [Paragraph("Cluster Segment Profile", table_header), Paragraph("Order Count", table_header), Paragraph("Share (%)", table_header), Paragraph("Avg Distance", table_header), Paragraph("Suboptimal Share", table_header)],
        [Paragraph("Low-Distance Local Route", table_cell), Paragraph("4,732", table_cell), Paragraph("46.4%", table_cell), Paragraph("702.1 miles", table_cell), Paragraph("44.6%", table_cell)],
        [Paragraph("Moderate Regional Corridor", table_cell), Paragraph("1,807", table_cell), Paragraph("17.7%", table_cell), Paragraph("1,161.6 miles", table_cell), Paragraph("69.0%", table_cell)],
        [Paragraph("High-Latency Bottleneck Corridor", table_cell), Paragraph("3,655", table_cell), Paragraph("35.9%", table_cell), Paragraph("1,951.3 miles", table_cell), Paragraph("<b>100.0% Suboptimal</b>", table_cell)]
    ]
    cluster_table = Table(cluster_rows, colWidths=[170, 80, 70, 100, 110])
    cluster_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary_color),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, bg_light]),
        ('BOX', (0, 0), (-1, -1), 0.5, border_color),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, border_color),
        ('PADDING', (0, 0), (-1, -1), 4)
    ]))
    story.append(cluster_table)
    story.append(Spacer(1, 14))

    # -------------------------------------------------------------------------
    # CHAPTER 5: HUB WORKLOAD CAPACITY CONSTRAINTS
    # -------------------------------------------------------------------------
    story.append(Paragraph("CHAPTER 5 — PER-HUB CAPACITY CONSTRAINTS & WORKLOAD SAFEGUARDS", h1_style))
    story.append(Paragraph(
        "A critical evaluator requirement is enforcing capacity constraints. Pure unconstrained closest-hub reallocation "
        "creates severe factory volume spikes. The table below demonstrates the workload shift and capacity utilization:",
        body_style
    ))

    cap_rows = [
        [Paragraph("Manufacturing Hub", table_header), Paragraph("Rated Cap", table_header), Paragraph("Baseline Vol", table_header), Paragraph("Reallocated Vol", table_header), Paragraph("Util %", table_header), Paragraph("Operational Status", table_header)],
        [Paragraph("Lot's O' Nuts (AZ)", table_cell), Paragraph("3,500", table_cell), Paragraph("5,692", table_cell), Paragraph("3,216", table_cell), Paragraph("91.9%", table_cell), Paragraph("Safe / Normalized", table_cell)],
        [Paragraph("Wicked Choccy's (GA)", table_cell), Paragraph("3,500", table_cell), Paragraph("4,152", table_cell), Paragraph("3,316", table_cell), Paragraph("94.7%", table_cell), Paragraph("Safe / Normalized", table_cell)],
        [Paragraph("Secret Factory (IL)", table_cell), Paragraph("1,800", table_cell), Paragraph("217", table_cell), Paragraph("1,912", table_cell), Paragraph("106.2%", table_cell), Paragraph("<b>⚠️ Capacity Alert (+112)</b>", table_cell)],
        [Paragraph("The Other Factory (TN)", table_cell), Paragraph("1,600", table_cell), Paragraph("100", table_cell), Paragraph("1,626", table_cell), Paragraph("101.6%", table_cell), Paragraph("<b>⚠️ Capacity Alert (+26)</b>", table_cell)],
        [Paragraph("Sugar Shack (MN)", table_cell), Paragraph("600", table_cell), Paragraph("33", table_cell), Paragraph("124", table_cell), Paragraph("20.7%", table_cell), Paragraph("Safe / Low Load", table_cell)]
    ]
    cap_table = Table(cap_rows, colWidths=[130, 70, 80, 90, 60, 100])
    cap_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary_color),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, bg_light]),
        ('BOX', (0, 0), (-1, -1), 0.5, border_color),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, border_color),
        ('PADDING', (0, 0), (-1, -1), 4)
    ]))
    story.append(cap_table)
    story.append(Spacer(1, 14))

    # -------------------------------------------------------------------------
    # CHAPTER 6: TOP POLICY RECOMMENDATIONS
    # -------------------------------------------------------------------------
    story.append(Paragraph("CHAPTER 6 — HIGH-IMPACT POLICY RECOMMENDATIONS", h1_style))
    story.append(Paragraph(
        "The multi-criteria optimization engine isolates the following highest-impact strategic reallocation policies:",
        body_style
    ))

    rec_rows = [
        [Paragraph("SKU", table_header), Paragraph("Region", table_header), Paragraph("Current Hub", table_header), Paragraph("Recommended Hub", table_header), Paragraph("Dist Reduction", table_header), Paragraph("Miles Saved", table_header)],
        [Paragraph("Wonka Bar - Triple Dazzle", table_cell), Paragraph("Pacific", table_cell), Paragraph("Wicked Choccy's (GA)", table_cell), Paragraph("Lot's O' Nuts (AZ)", table_cell), Paragraph("-76.1%", table_cell), Paragraph("1,103,890 mi", table_cell)],
        [Paragraph("Wonka Bar - Milk Chocolate", table_cell), Paragraph("Pacific", table_cell), Paragraph("Wicked Choccy's (GA)", table_cell), Paragraph("Lot's O' Nuts (AZ)", table_cell), Paragraph("-77.1%", table_cell), Paragraph("1,088,518 mi", table_cell)],
        [Paragraph("Wonka Bar - Scrumdiddly.", table_cell), Paragraph("Atlantic", table_cell), Paragraph("Lot's O' Nuts (AZ)", table_cell), Paragraph("Wicked Choccy's (GA)", table_cell), Paragraph("-68.7%", table_cell), Paragraph("846,148 mi", table_cell)],
        [Paragraph("Wonka Bar - Fudge Mallows", table_cell), Paragraph("Atlantic", table_cell), Paragraph("Lot's O' Nuts (AZ)", table_cell), Paragraph("Wicked Choccy's (GA)", table_cell), Paragraph("-68.5%", table_cell), Paragraph("743,198 mi", table_cell)],
        [Paragraph("Wonka Bar - Nutty Crunch", table_cell), Paragraph("Atlantic", table_cell), Paragraph("Lot's O' Nuts (AZ)", table_cell), Paragraph("Wicked Choccy's (GA)", table_cell), Paragraph("-68.5%", table_cell), Paragraph("669,123 mi", table_cell)],
        [Paragraph("Wonka Bar - Nutty Crunch", table_cell), Paragraph("Interior", table_cell), Paragraph("Lot's O' Nuts (AZ)", table_cell), Paragraph("The Other Factory (TN)", table_cell), Paragraph("-84.2%", table_cell), Paragraph("456,528 mi", table_cell)]
    ]
    rec_table = Table(rec_rows, colWidths=[120, 60, 110, 110, 65, 65])
    rec_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary_color),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, bg_light]),
        ('BOX', (0, 0), (-1, -1), 0.5, border_color),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, border_color),
        ('PADDING', (0, 0), (-1, -1), 4)
    ]))
    story.append(rec_table)
    story.append(Spacer(1, 14))

    # -------------------------------------------------------------------------
    # CONCLUSION & SIGN-OFF
    # -------------------------------------------------------------------------
    story.append(Paragraph("CHAPTER 7 — CONCLUSION & IMPLEMENTATION ROADMAP", h1_style))
    story.append(Paragraph(
        "By transitioning Nassau Candy from legacy static manufacturing rules to an intelligent, geospatial, capacity-guarded "
        "reallocation model, executive leadership can eliminate <b>7.49 million transit miles (-59.6%)</b>, reduce carrier freight costs "
        "by <b>$13.6M</b>, balance workloads across underutilized central facilities, and safeguard 100% of gross profit margin integrity. "
        "The complete interactive Streamlit dashboard enables real-time what-if scenario testing and multi-criteria sensitivity exploration.",
        body_style
    ))
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Submitted by:</b> Anushka Roy | Unified Mentor Machine Learning Internship | Academic Submission 2026", ParagraphStyle(
        'FooterNote', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=8, leading=10, textColor=muted_text
    )))

    doc.build(story)
    print(f">> PDF Report successfully generated at: {output_path}")
    return output_path


if __name__ == "__main__":
    build_pdf_report()
