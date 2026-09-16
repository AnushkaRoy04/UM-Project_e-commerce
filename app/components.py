"""
Bespoke UI Components & Executive Design System
Author: Anushka Roy
Unified Mentor Machine Learning Internship
"""

import streamlit as st
from src.config import THEME_TOKENS


def inject_custom_css():
    """
    Injects high-contrast corporate design tokens:
    - High-visibility sidebar panel
    - Architectural card surfaces with top accent borders
    - Legible typography and sharp contrast
    - Zero emojis and zero saturated AI-style gradients
    """
    st.html("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600;700&display=swap');

        :root {
            --bg-dark: #0F141C;
            --surface: #171E2B;
            --sidebar-bg: #131926;
            --border: #263147;
            --border-light: #334155;
            --text-primary: #FFFFFF;
            --text-secondary: #94A3B8;
        }

        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            color: var(--text-primary);
        }

        .stApp {
            background-color: var(--bg-dark);
        }

        /* ------------------------------------------------------------- */
        /* HIGH-VISIBILITY SIDEBAR                                      */
        /* ------------------------------------------------------------- */
        [data-testid="stSidebar"] {
            background-color: var(--sidebar-bg) !important;
            border-right: 1px solid var(--border) !important;
        }
        [data-testid="stSidebarContent"] {
            padding-top: 1.5rem !important;
            padding-bottom: 1.5rem !important;
            padding-left: 1.1rem !important;
            padding-right: 1.1rem !important;
        }
        [data-testid="stSidebar"] .stRadio label {
            color: #E2E8F0 !important;
            font-size: 0.90rem !important;
            font-weight: 500 !important;
            padding-top: 4px !important;
            padding-bottom: 4px !important;
        }
        [data-testid="stSidebar"] .stRadio > div {
            gap: 4px !important;
        }
        [data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label:hover {
            color: #FFFFFF !important;
            background: rgba(37, 99, 235, 0.08);
            border-radius: 6px;
        }
        [data-testid="stSidebar"] hr {
            border-color: var(--border) !important;
        }
        [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
            color: #F8FAFC !important;
            font-weight: 600 !important;
            font-size: 0.88rem !important;
        }

        /* ------------------------------------------------------------- */
        /* HEADERS & TYPOGRAPHY                                          */
        /* ------------------------------------------------------------- */
        .main-header {
            font-size: 2.1rem;
            font-weight: 800;
            letter-spacing: -0.025em;
            color: #FFFFFF;
            margin-bottom: 0.25rem;
            line-height: 1.2;
        }
        .sub-header {
            font-size: 0.95rem;
            font-weight: 400;
            color: #94A3B8;
            margin-bottom: 1.4rem;
            line-height: 1.5;
        }
        .section-title {
            font-size: 1.15rem;
            font-weight: 700;
            color: #FFFFFF !important;
            margin-top: 1.1rem;
            margin-bottom: 0.25rem;
            letter-spacing: -0.015em;
        }
        .section-subtitle {
            font-size: 0.84rem;
            font-weight: 400;
            color: #94A3B8 !important;
            margin-top: -0.1rem;
            margin-bottom: 0.85rem;
            line-height: 1.4;
        }

        /* ------------------------------------------------------------- */
        /* ARCHITECTURAL METRIC CARDS                                   */
        /* ------------------------------------------------------------- */
        .card-container {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 16px 14px;
            min-height: 105px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: flex-start;
            position: relative;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.25);
            transition: border-color 0.15s ease;
        }
        .card-container:hover {
            border-color: var(--border-light);
        }
        .card-accent-blue { border-top: 3px solid #2563EB; }
        .card-accent-emerald { border-top: 3px solid #059669; }
        .card-accent-crimson { border-top: 3px solid #BE123C; }
        .card-accent-amber { border-top: 3px solid #D97706; }
        .card-accent-steel { border-top: 3px solid #64748B; }

        .card-label {
            font-size: 0.70rem;
            font-weight: 700;
            color: #94A3B8;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 4px;
        }
        .card-value {
            font-size: 1.65rem;
            font-weight: 800;
            letter-spacing: -0.02em;
            line-height: 1.1;
            color: #FFFFFF;
            font-family: 'Inter', sans-serif;
        }
        .card-delta {
            font-size: 0.75rem;
            font-weight: 600;
            margin-top: 4px;
            color: #94A3B8;
        }

        /* ------------------------------------------------------------- */
        /* RECONCILIATION & AUDIT LEDGER BOX                             */
        /* ------------------------------------------------------------- */
        .audit-panel {
            background: var(--surface);
            border: 1px solid var(--border);
            border-left: 4px solid #2563EB;
            border-radius: 8px;
            padding: 16px 20px;
            margin-top: 14px;
            margin-bottom: 18px;
            color: #E2E8F0;
        }
        .audit-title {
            font-size: 0.80rem;
            font-weight: 700;
            color: #94A3B8;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 8px;
        }
        .audit-tag {
            display: inline-block;
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.05em;
            text-transform: uppercase;
        }
        .tag-success {
            background: rgba(5, 150, 105, 0.15);
            border: 1px solid #059669;
            color: #34D399;
        }
        .tag-danger {
            background: rgba(190, 18, 60, 0.15);
            border: 1px solid #BE123C;
            color: #FDA4AF;
        }
        .tag-warning {
            background: rgba(217, 119, 6, 0.15);
            border: 1px solid #D97706;
            color: #FCD34D;
        }

        /* ------------------------------------------------------------- */
        /* CORPORATE CAPACITY ADVISORY BANNER                           */
        /* ------------------------------------------------------------- */
        .advisory-box {
            background: #1C1917;
            border: 1px solid #7F1D1D;
            border-left: 4px solid #DC2626;
            border-radius: 8px;
            padding: 16px 20px;
            margin: 14px 0;
            color: #E2E8F0;
        }
        .advisory-header {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 0.92rem;
            font-weight: 700;
            color: #FCA5A5;
            margin-bottom: 6px;
        }

        /* ------------------------------------------------------------- */
        /* STRATEGIC TAKEAWAY CALLOUT BOX                                */
        /* ------------------------------------------------------------- */
        .takeaway-box {
            background: var(--surface);
            border: 1px solid var(--border);
            border-left: 4px solid #059669;
            border-radius: 8px;
            padding: 16px 20px;
            margin-top: 18px;
            margin-bottom: 18px;
            font-size: 0.90rem;
            line-height: 1.6;
            color: #CBD5E1;
        }
        .takeaway-box b {
            color: #FFFFFF;
        }

        /* Audit Table */
        .audit-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 6px;
        }
        .audit-table th {
            padding: 8px 12px;
            font-size: 0.72rem;
            color: #94A3B8;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            border-bottom: 1px solid #334155;
            text-align: left;
        }
        .audit-table td {
            padding: 8px 12px;
            font-size: 0.86rem;
            color: #CBD5E1;
            border-bottom: 1px solid #263147;
        }

        /* Tables */
        .stDataFrame {
            border: 1px solid #263147;
            border-radius: 6px;
            overflow: hidden;
        }
    </style>
    """)


def render_kpi_card(value, label, delta=None, accent="blue"):
    """
    Renders an architectural metric card with clean typography and top accent.
    Accent choices: 'blue', 'emerald', 'crimson', 'amber', 'steel'.
    Strictly unindented to prevent markdown pre/code block parsing.
    """
    accent_class = f"card-accent-{accent}"
    delta_html = f'<div class="card-delta">{delta}</div>' if delta else ''
    return f'<div class="card-container {accent_class}"><div class="card-label">{label}</div><div class="card-value">{value}</div>{delta_html}</div>'


def render_audit_ledger(reconciliation_data):
    """
    Renders an executive mathematical audit and reconciliation ledger.
    Uses native st.html to guarantee that raw HTML tables render as styled HTML,
    never as markdown code blocks.
    """
    rows = []
    for r in reconciliation_data:
        rows.append(
            f'<tr>'
            f'<td style="padding: 8px 12px; color: #CBD5E1; font-size: 0.86rem; border-bottom: 1px solid #263147;">{r["field"]}</td>'
            f'<td style="padding: 8px 12px; font-weight: 700; color: #FFFFFF; font-size: 0.86rem; border-bottom: 1px solid #263147;">{r["value"]}</td>'
            f'<td style="padding: 8px 12px; font-size: 0.86rem; border-bottom: 1px solid #263147;"><span class="audit-tag {r["tag_class"]}">{r["status"]}</span></td>'
            f'</tr>'
        )
    table_body = "".join(rows)

    html = (
        f'<div class="audit-panel">'
        f'<div class="audit-title">Optimization Calculation Audit &amp; Sanity Reconciliation</div>'
        f'<table class="audit-table" style="width: 100%; border-collapse: collapse; margin-top: 6px;">'
        f'<thead><tr>'
        f'<th style="padding: 8px 12px; font-size: 0.72rem; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.06em; border-bottom: 1px solid #334155; text-align: left;">Audit Dimension</th>'
        f'<th style="padding: 8px 12px; font-size: 0.72rem; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.06em; border-bottom: 1px solid #334155; text-align: left;">Numerical Value</th>'
        f'<th style="padding: 8px 12px; font-size: 0.72rem; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.06em; border-bottom: 1px solid #334155; text-align: left;">Reconciliation Status</th>'
        f'</tr></thead>'
        f'<tbody>{table_body}</tbody>'
        f'</table></div>'
    )
    st.html(html)


def render_capacity_advisory(warnings):
    """
    Renders a formal corporate advisory banner for capacity breaches.
    Zero emojis, native HTML rendering.
    """
    if not warnings:
        return

    items = []
    for w in warnings:
        items.append(
            f'<li><b>{w["hub"]}</b> ({w["location"]}): Projected volume of <b>{w["projected_volume"]:,} orders</b> '
            f'exceeds rated capacity of <b>{w["rated_capacity"]:,} orders</b> by <b>+{w["excess_orders"]:,} orders</b> '
            f'({w["utilization_pct"]}% utilization).</li>'
        )
    items_html = "".join(items)

    html = (
        f'<div class="advisory-box">'
        f'<div class="advisory-header">'
        f'<span class="audit-tag tag-danger">CAPACITY ADVISORY</span> '
        f'<span style="font-weight:700;color:#FCA5A5;">Production Ceiling Exceeded at Selected Facilities</span>'
        f'</div>'
        f'<div style="font-size:0.86rem;color:#E2E8F0;margin-top:6px;">'
        f'Unconstrained closest-hub reallocation breaches rated operational limits at the following facilities:'
        f'</div>'
        f'<ul style="margin:8px 0;padding-left:20px;font-size:0.86rem;line-height:1.5;">'
        f'{items_html}'
        f'</ul>'
        f'<div style="font-size:0.80rem;color:#94A3B8;margin-top:6px;">'
        f'<b>Operational Directive:</b> Review Module 3 to enable balanced overflow rerouting, distributing surplus orders to adjacent regional nodes with minimal mileage penalty.'
        f'</div>'
        f'</div>'
    )
    st.html(html)


def style_plotly_figure(fig, show_legend=True, legend_bottom=False):
    """
    Applies consistent executive corporate styling to Plotly figures:
    - High-contrast axis typography
    - Subtle structural grid lines
    - Zero title overlaps
    - Responsive layout
    """
    layout_update = dict(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(23, 30, 43, 0.65)',
        font=dict(family="Inter", size=11, color="#CBD5E1"),
        margin=dict(l=40, r=25, t=25, b=35),
        showlegend=show_legend
    )

    if show_legend and legend_bottom:
        layout_update['legend'] = dict(
            orientation="h",
            yanchor="top",
            y=-0.22,
            xanchor="center",
            x=0.5,
            font=dict(size=11, color="#E2E8F0")
        )
        layout_update['margin'] = dict(l=40, r=25, t=25, b=75)
    elif show_legend:
        layout_update['legend'] = dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=11, color="#E2E8F0")
        )
        layout_update['margin'] = dict(l=40, r=25, t=45, b=35)

    fig.update_layout(**layout_update)
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='#263147',
        tickfont=dict(size=11, color="#94A3B8"),
        title_font=dict(size=11, color="#CBD5E1"),
        zeroline=False
    )
    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='#263147',
        tickfont=dict(size=11, color="#94A3B8"),
        title_font=dict(size=11, color="#CBD5E1"),
        zeroline=False
    )
    return fig
