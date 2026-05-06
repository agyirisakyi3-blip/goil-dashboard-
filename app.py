import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import json
import os
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Goil Ghana Financial Dashboard",
    page_icon="⛽",
    layout="wide",
    initial_sidebar_state="expanded"
)

PAGE_BG = "#0F172A"
CARD_BG = "#1E293B"
CARD_BORDER = "#334155"
PRIMARY = "#10B981"
SECONDARY = "#F59E0B"
ACCENT = "#3B82F6"
ACCENT2 = "#8B5CF6"
DANGER = "#EF4444"
TEXT_PRIMARY = "#F8FAFC"
TEXT_SECONDARY = "#94A3B8"
TEXT_MUTED = "#64748B"

def inject_css():
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

        * {{
            font-family: 'Inter', sans-serif !important;
        }}

        .stApp {{
            background: linear-gradient(135deg, #0F172A 0%, #1E1B4B 50%, #0F172A 100%);
            color: {TEXT_PRIMARY};
        }}

        [data-testid="stSidebar"] {{
            background: linear-gradient(180deg, #1E293B 0%, #0F172A 100%);
            border-right: 1px solid {CARD_BORDER};
        }}

        [data-testid="stSidebar"] .stRadio > label {{
            color: {TEXT_SECONDARY} !important;
        }}

        .kpi-card {{
            background: linear-gradient(135deg, {CARD_BG} 0%, #2D3A4F 100%);
            border: 1px solid {CARD_BORDER};
            border-radius: 16px;
            padding: 24px;
            margin: 8px 0;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }}

        .kpi-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, {PRIMARY}, {SECONDARY}, {ACCENT});
            opacity: 0;
            transition: opacity 0.3s ease;
        }}

        .kpi-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 20px 40px rgba(0,0,0,0.3);
            border-color: {PRIMARY};
        }}

        .kpi-card:hover::before {{
            opacity: 1;
        }}

        .kpi-icon {{
            font-size: 32px;
            margin-bottom: 12px;
        }}

        .kpi-label {{
            color: {TEXT_SECONDARY};
            font-size: 14px;
            font-weight: 500;
            margin-bottom: 8px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}

        .kpi-value {{
            color: {TEXT_PRIMARY};
            font-size: 32px;
            font-weight: 700;
            margin-bottom: 8px;
        }}

        .kpi-delta {{
            font-size: 14px;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: 4px;
            padding: 4px 8px;
            border-radius: 6px;
        }}

        .delta-positive {{
            color: {PRIMARY};
            background: rgba(16, 185, 129, 0.1);
        }}

        .delta-negative {{
            color: {DANGER};
            background: rgba(239, 68, 68, 0.1);
        }}

        .section-title {{
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 8px;
            background: linear-gradient(135deg, {TEXT_PRIMARY}, {TEXT_SECONDARY});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .section-subtitle {{
            color: {TEXT_SECONDARY};
            font-size: 16px;
            margin-bottom: 32px;
        }}

        .chart-container {{
            background: {CARD_BG};
            border: 1px solid {CARD_BORDER};
            border-radius: 16px;
            padding: 24px;
            margin: 12px 0;
        }}

        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
        }}

        .stTabs [data-baseweb="tab"] {{
            background: {CARD_BG};
            border: 1px solid {CARD_BORDER};
            border-radius: 12px;
            padding: 12px 24px;
            color: {TEXT_SECONDARY};
            font-weight: 500;
            transition: all 0.3s ease;
        }}

        .stTabs [aria-selected="true"] {{
            background: linear-gradient(135deg, {PRIMARY}, #059669);
            border-color: {PRIMARY};
            color: white;
            box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
        }}

        .stSelectbox > div > div {{
            background: {CARD_BG} !important;
            border: 1px solid {CARD_BORDER} !important;
            border-radius: 12px !important;
            color: {TEXT_PRIMARY} !important;
        }}

        .stMultiSelect > div > div {{
            background: {CARD_BG} !important;
            border: 1px solid {CARD_BORDER} !important;
            border-radius: 12px !important;
        }}

        .stSlider > div > div {{
            color: {PRIMARY} !important;
        }}

        .progress-bar {{
            background: {CARD_BG};
            border: 1px solid {CARD_BORDER};
            border-radius: 12px;
            padding: 16px;
            margin: 8px 0;
        }}

        .progress-label {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 8px;
            color: {TEXT_SECONDARY};
            font-size: 14px;
        }}

        .progress-track {{
            background: #334155;
            border-radius: 8px;
            height: 8px;
            overflow: hidden;
        }}

        .progress-fill {{
            height: 100%;
            border-radius: 8px;
            transition: width 1s ease;
        }}

        .metric-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 16px;
            background: {CARD_BG};
            border: 1px solid {CARD_BORDER};
            border-radius: 12px;
            margin: 8px 0;
            transition: all 0.2s ease;
        }}

        .metric-row:hover {{
            border-color: {ACCENT};
            background: #253347;
        }}

        .badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
        }}

        .badge-success {{ background: rgba(16, 185, 129, 0.2); color: {PRIMARY}; }}
        .badge-warning {{ background: rgba(245, 158, 11, 0.2); color: {SECONDARY}; }}
        .badge-info {{ background: rgba(59, 130, 246, 0.2); color: {ACCENT}; }}

        [data-testid="stExpander"] {{
            background: {CARD_BG};
            border: 1px solid {CARD_BORDER};
            border-radius: 12px;
        }}

        .stDataFrame {{
            border-radius: 12px;
            overflow: hidden;
        }}

        @keyframes pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.5; }}
        }}

        .live-indicator {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 8px 16px;
            background: rgba(16, 185, 129, 0.1);
            border: 1px solid rgba(16, 185, 129, 0.3);
            border-radius: 20px;
            font-size: 14px;
            color: {PRIMARY};
        }}

        .live-dot {{
            width: 8px;
            height: 8px;
            background: {PRIMARY};
            border-radius: 50%;
            animation: pulse 2s infinite;
        }}

        .footer {{
            text-align: center;
            padding: 32px 0;
            color: {TEXT_MUTED};
            font-size: 14px;
            border-top: 1px solid {CARD_BORDER};
            margin-top: 48px;
        }}
        </style>
    """, unsafe_allow_html=True)

inject_css()

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

def load_data(filename):
    with open(os.path.join(DATA_DIR, filename), "r") as f:
        return json.load(f)

revenue_data = load_data("revenue.json")
expenses_data = load_data("expenses.json")
fuel_data = load_data("fuel_sales_volume.json")
ops_data = load_data("operational_metrics.json")
bs_data = load_data("balance_sheet.json")
cf_data = load_data("cash_flow.json")

def format_ghs(value):
    if value >= 1e9:
        return f"GHS {value/1e9:.2f}B"
    elif value >= 1e6:
        return f"GHS {value/1e6:.2f}M"
    elif value >= 1e3:
        return f"GHS {value/1e3:.2f}K"
    return f"GHS {value:,.0f}"

def kpi_card(icon, label, value, delta=None, delta_type="positive"):
    delta_html = ""
    if delta:
        cls = "delta-positive" if delta_type == "positive" else "delta-negative"
        arrow = "↑" if delta_type == "positive" else "↓"
        delta_html = f'<span class="kpi-delta {cls}">{arrow} {delta}</span>'

    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">{icon}</div>
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            {delta_html}
        </div>
    """, unsafe_allow_html=True)

def progress_bar(label, value, max_val, color=PRIMARY):
    pct = min(100, (value / max_val) * 100)
    st.markdown(f"""
        <div class="progress-bar">
            <div class="progress-label">
                <span>{label}</span>
                <span style="color: {TEXT_PRIMARY}; font-weight: 600;">{pct:.1f}%</span>
            </div>
            <div class="progress-track">
                <div class="progress-fill" style="width: {pct}%; background: linear-gradient(90deg, {color}, {SECONDARY});"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def metric_row(label, value, badge_text=None, badge_type="info"):
    badge = f'<span class="badge badge-{badge_type}">{badge_text}</span>' if badge_text else ""
    st.markdown(f"""
        <div class="metric-row">
            <span style="color: {TEXT_SECONDARY};">{label}</span>
            <div style="display: flex; align-items: center; gap: 12px;">
                {badge}
                <span style="color: {TEXT_PRIMARY}; font-weight: 600;">{value}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

def create_chart_template():
    return dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=TEXT_SECONDARY, family="Inter"),
        xaxis=dict(gridcolor=CARD_BORDER, zerolinecolor=CARD_BORDER),
        yaxis=dict(gridcolor=CARD_BORDER, zerolinecolor=CARD_BORDER),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color=TEXT_SECONDARY))
    )

# SIDEBAR
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding: 20px 0;">
            <div style="font-size: 48px; margin-bottom: 8px;">⛽</div>
            <div style="font-size: 24px; font-weight: 700; color: #F8FAFC;">GOIL GHANA</div>
            <div style="font-size: 12px; color: #94A3B8; text-transform: uppercase; letter-spacing: 2px;">Financial Dashboard</div>
        </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown('<div style="color: #94A3B8; font-size: 12px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 12px;">Time Period</div>', unsafe_allow_html=True)
    years = st.multiselect("Select Year", [2023, 2024, 2025], default=[2023, 2024, 2025], label_visibility="collapsed")

    st.markdown('<div style="color: #94A3B8; font-size: 12px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 12px; margin-top: 16px;">Quarters</div>', unsafe_allow_html=True)
    quarters = st.multiselect("Select Quarters", ["Q1", "Q2", "Q3", "Q4"], default=["Q1", "Q2", "Q3", "Q4"], label_visibility="collapsed")

    st.divider()

    st.markdown("""
        <div class="live-indicator">
            <span class="live-dot"></span>
            Live Data
        </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown(f"""
        <div style="color: {TEXT_MUTED}; font-size: 12px; text-align: center; margin-top: 16px;">
            Currency: <span style="color: {TEXT_PRIMARY}; font-weight: 600;">GHS (₵)</span><br>
            Last Updated: <span style="color: {TEXT_PRIMARY};">{datetime.now().strftime("%b %d, %Y")}</span>
        </div>
    """, unsafe_allow_html=True)

# MAIN CONTENT
rev_summary = revenue_data["revenue"]["annual_summary"]
exp_summary = expenses_data["expenses"]["annual_summary"]
selected = [y for y in years if str(y) in rev_summary]

if not selected:
    st.warning("No data for selected years. Please adjust your filters.")
    st.stop()

latest_year = str(max(selected))

# HEADER
st.markdown(f"""
    <div style="margin-bottom: 32px;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <div class="section-title">Financial Performance Dashboard</div>
                <div class="section-subtitle">Comprehensive analytics for Goil Ghana Limited • {latest_year}</div>
            </div>
            <div class="live-indicator">
                <span class="live-dot"></span>
                FY {latest_year}
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# TABS
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "📊 Overview",
    "💰 Revenue",
    "💸 Expenses",
    "📈 Profitability",
    "⛽ Fuel Sales",
    "🏦 Balance Sheet",
    "💵 Cash Flow",
    "⚙️ Operations"
])

# TAB 1: OVERVIEW
with tab1:
    latest_rev = rev_summary[latest_year]["total_revenue"]
    latest_exp = exp_summary[latest_year]["total_expenses"]
    latest_profit = latest_rev - latest_exp
    latest_margin = (latest_profit / latest_rev) * 100
    rev_growth = rev_summary[latest_year].get("yoy_growth")
    stations = ops_data["operational_metrics"]["station_network"][latest_year]["total_stations"]
    fuel_vol = fuel_data["fuel_sales_volume"]["annual_summary"][latest_year]["total_liters"]
    employees = ops_data["operational_metrics"]["employee_metrics"][latest_year]["total_employees"]

    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        kpi_card("💰", "Total Revenue", format_ghs(latest_rev), f"{rev_growth:.1f}% YoY" if rev_growth else "Base Year", "positive")
    with col2:
        kpi_card("📈", "Net Profit", format_ghs(latest_profit), f"{latest_margin:.1f}% Margin", "positive")
    with col3:
        kpi_card("💸", "Total Expenses", format_ghs(latest_exp), f"{(latest_exp/latest_rev*100):.1f}% of Rev", "positive")
    with col4:
        kpi_card("⛽", "Stations", f"{stations:,}", "+34 New Sites", "positive")
    with col5:
        kpi_card("🛢️", "Fuel Volume", f"{fuel_vol/1e9:.2f}B L", "+19.1% YoY", "positive")
    with col6:
        kpi_card("👥", "Employees", f"{employees:,}", "+240 Added", "positive")

    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        rev_q = revenue_data["revenue"]["quarterly"]
        df_rev = pd.DataFrame(rev_q)

        fig_rev = go.Figure()
        fig_rev.add_trace(go.Scatter(
            x=df_rev["quarter"], y=df_rev["total_revenue"],
            name="Total Revenue", mode="lines+markers",
            line=dict(color=PRIMARY, width=3),
            fill="tozeroy", fillcolor=f"rgba(16, 185, 129, 0.1)"
        ))
        fig_rev.add_trace(go.Scatter(
            x=df_rev["quarter"], y=df_rev["fuel_sales"],
            name="Fuel Sales", mode="lines+markers",
            line=dict(color=SECONDARY, width=2)
        ))
        fig_rev.update_layout(
            title=dict(text="Revenue Trajectory", font=dict(size=18, color=TEXT_PRIMARY)),
            height=380,
            **create_chart_template()
        )
        st.plotly_chart(fig_rev, use_container_width=True, key="overview_rev")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div style="color: #F8FAFC; font-size: 16px; font-weight: 600; margin-bottom: 16px;">Revenue Composition</div>', unsafe_allow_html=True)

        fig_pie = px.pie(
            values=[rev_summary[latest_year][k] for k in ["fuel_sales", "lubricants", "convenience_store", "fleet_services", "other_income"]],
            names=["Fuel Sales", "Lubricants", "Convenience", "Fleet", "Other"],
            hole=0.6,
            color_discrete_sequence=[PRIMARY, SECONDARY, ACCENT, ACCENT2, DANGER]
        )
        fig_pie.update_traces(textposition="inside", textinfo="percent+label", textfont=dict(color=TEXT_PRIMARY))
        fig_pie.update_layout(height=380, showlegend=False, **create_chart_template())
        st.plotly_chart(fig_pie, use_container_width=True, key="overview_pie")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        years_avail = [y for y in ["2023", "2024", "2025"] if y in rev_summary and int(y) in selected]
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(name="Revenue", x=years_avail, y=[rev_summary[y]["total_revenue"] for y in years_avail], marker_color=PRIMARY))
        fig_bar.add_trace(go.Bar(name="Expenses", x=years_avail, y=[exp_summary[y]["total_expenses"] for y in years_avail], marker_color=DANGER))
        fig_bar.add_trace(go.Bar(name="Profit", x=years_avail, y=[rev_summary[y]["total_revenue"] - exp_summary[y]["total_expenses"] for y in years_avail], marker_color=SECONDARY))
        fig_bar.update_layout(
            title=dict(text="P&L Comparison", font=dict(size=16, color=TEXT_PRIMARY)),
            barmode="group", height=320, **create_chart_template()
        )
        st.plotly_chart(fig_bar, use_container_width=True, key="overview_pl")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div style="color: #F8FAFC; font-size: 16px; font-weight: 600; margin-bottom: 16px;">Key Performance Indicators</div>', unsafe_allow_html=True)

        kpis_q = ops_data["operational_metrics"]["kpis"]["quarterly"]
        df_kpi = pd.DataFrame(kpis_q)
        df_kpi["year"] = df_kpi["quarter"].str.extract(r"(\d{4})").astype(int)
        latest_kpi = df_kpi[df_kpi["year"] == int(latest_year)].iloc[-1]

        progress_bar("Gross Margin", latest_kpi["gross_profit_margin"], 100, PRIMARY)
        progress_bar("Net Margin", latest_kpi["net_profit_margin"], 100, SECONDARY)
        progress_bar("EBITDA Margin", latest_kpi["ebitda_margin"], 100, ACCENT)
        progress_bar("ROE", latest_kpi["return_on_equity"], 100, ACCENT2)

        st.markdown('</div>', unsafe_allow_html=True)

    with col_c:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div style="color: #F8FAFC; font-size: 16px; font-weight: 600; margin-bottom: 16px;">Quick Stats</div>', unsafe_allow_html=True)

        metric_row("Customer Satisfaction", f"{ops_data['operational_metrics']['customer_metrics'][latest_year]['customer_satisfaction_score']:.1f}/100", "Excellent", "success")
        metric_row("NPS Score", str(ops_data['operational_metrics']['customer_metrics'][latest_year]['nps_score']), "Strong", "success")
        metric_row("Station Uptime", f"{ops_data['operational_metrics']['station_network'][latest_year]['operational_uptime_percent']:.1f}%", "99%+", "success")
        metric_row("Inventory Turnover", f"{latest_kpi['inventory_turnover']:.1f}x", "Healthy", "info")
        metric_row("Safety Incidents", str(ops_data['operational_metrics']['employee_metrics'][latest_year]['safety_incidents']), "↓ Improving", "success")

        st.markdown('</div>', unsafe_allow_html=True)

# TAB 2: REVENUE
with tab2:
    st.markdown('<div class="section-title">Revenue Analytics</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Detailed breakdown of revenue streams and growth trends</div>', unsafe_allow_html=True)

    sel = [y for y in years if str(y) in rev_summary]
    ly = str(max(sel)) if sel else latest_year

    col1, col2, col3 = st.columns(3)
    with col1:
        kpi_card("📊", "Annual Revenue", format_ghs(rev_summary[ly]["total_revenue"]), f"{rev_summary[ly].get('yoy_growth', 0):.1f}% Growth", "positive")
    with col2:
        kpi_card("⛽", "Fuel Revenue", format_ghs(rev_summary[ly]["fuel_sales"]), f"{rev_summary[ly]['fuel_sales']/rev_summary[ly]['total_revenue']*100:.1f}% of Total", "positive")
    with col3:
        kpi_card("🛢️", "Non-Fuel Revenue", format_ghs(rev_summary[ly]["lubricants"] + rev_summary[ly]["convenience_store"] + rev_summary[ly]["fleet_services"] + rev_summary[ly]["other_income"]), "Diversifying", "positive")

    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    df_rev = pd.DataFrame(revenue_data["revenue"]["quarterly"])

    fig = go.Figure()
    segments = ["fuel_sales", "lubricants", "convenience_store", "fleet_services", "other_income"]
    labels = ["Fuel Sales", "Lubricants", "Convenience Store", "Fleet Services", "Other Income"]
    colors = [PRIMARY, SECONDARY, ACCENT, ACCENT2, DANGER]

    for seg, label, color in zip(segments, labels, colors):
        fig.add_trace(go.Bar(name=label, x=df_rev["quarter"], y=df_rev[seg], marker_color=color, hovertemplate=f"<b>{label}</b><br>Quarter: %{{x}}<br>Revenue: %{{y:,.0f}}<extra></extra>"))

    fig.update_layout(
        title=dict(text="Quarterly Revenue Breakdown", font=dict(size=18, color=TEXT_PRIMARY)),
        barmode="stack", height=450, **create_chart_template()
    )
    st.plotly_chart(fig, use_container_width=True, key="revenue_stacked")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig_growth = go.Figure()
        df_rev["year"] = df_rev["quarter"].str.extract(r"(\d{4})").astype(int)
        df_rev_sorted = df_rev.sort_values("year")
        df_rev_sorted["qtr_rev"] = df_rev_sorted["total_revenue"].pct_change() * 100
        fig_growth.add_trace(go.Bar(
            x=df_rev_sorted["quarter"], y=df_rev_sorted["qtr_rev"],
            marker_color=[PRIMARY if v >= 0 else DANGER for v in df_rev_sorted["qtr_rev"]],
            name="QoQ Growth"
        ))
        fig_growth.update_layout(
            title=dict(text="Quarter-over-Quarter Growth", font=dict(size=16, color=TEXT_PRIMARY)),
            height=320, **create_chart_template()
        )
        st.plotly_chart(fig_growth, use_container_width=True, key="revenue_growth")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div style="color: #F8FAFC; font-size: 16px; font-weight: 600; margin-bottom: 16px;">Revenue by Region (Top 6)</div>', unsafe_allow_html=True)

        regions = rev_summary[ly].get("revenue_by_region", {})
        if not regions:
            regions = revenue_data["revenue"].get("revenue_by_region", {}).get(ly, {})

        if regions:
            sorted_regions = sorted(regions.items(), key=lambda x: x[1], reverse=True)[:6]
            fig_region = go.Figure()
            fig_region.add_trace(go.Bar(
                x=[r[0].replace("_", " ").title() for r in sorted_regions],
                y=[r[1] for r in sorted_regions],
                marker_color=PRIMARY,
                orientation="v"
            ))
            fig_region.update_layout(height=320, **create_chart_template())
            fig_region.update_xaxes(tickangle=-45)
            st.plotly_chart(fig_region, use_container_width=True, key="revenue_region")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    with st.expander("📋 Revenue Detail Table"):
        df_display = df_rev[["quarter", "fuel_sales", "lubricants", "convenience_store", "fleet_services", "other_income", "total_revenue"]].copy()
        for c in df_display.columns[1:]:
            df_display[c] = df_display[c].apply(format_ghs)
        st.dataframe(df_display, use_container_width=True, hide_index=True)

# TAB 3: EXPENSES
with tab3:
    st.markdown('<div class="section-title">Expense Management</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Track and analyze cost structure and spending patterns</div>', unsafe_allow_html=True)

    sel = [y for y in years if str(y) in exp_summary]
    ly = str(max(sel)) if sel else latest_year

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        kpi_card("💸", "Total Expenses", format_ghs(exp_summary[ly]["total_expenses"]), f"{(exp_summary[ly]['total_expenses']/rev_summary[ly]['total_revenue']*100):.1f}% of Revenue")
    with col2:
        kpi_card("🏭", "COGS", format_ghs(exp_summary[ly]["cost_of_goods_sold"]), f"{exp_summary[ly]['cogs_percentage']:.1f}%", "positive")
    with col3:
        kpi_card("👥", "Employee Costs", format_ghs(exp_summary[ly]["employee_costs"]), f"{(exp_summary[ly]['employee_costs']/exp_summary[ly]['total_expenses']*100):.1f}% of OpEx")
    with col4:
        kpi_card("📦", "OPEX", format_ghs(exp_summary[ly]["total_expenses"] - exp_summary[ly]["cost_of_goods_sold"]), f"{exp_summary[ly]['opex_percentage']:.1f}%", "positive")

    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        exp_categories = ["cost_of_goods_sold", "employee_costs", "transport_logistics", "marketing_advertising", "maintenance_repairs", "utilities", "depreciation", "other_expenses"]
        exp_labels = ["COGS", "Employee Costs", "Transport", "Marketing", "Maintenance", "Utilities", "Depreciation", "Other"]

        fig_pie = px.pie(
            values=[exp_summary[ly][k] for k in exp_categories],
            names=exp_labels,
            hole=0.5,
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_pie.update_traces(textposition="inside", textinfo="percent+label", textfont=dict(color=TEXT_PRIMARY))
        fig_pie.update_layout(
            title=dict(text=f"Expense Breakdown ({ly})", font=dict(size=16, color=TEXT_PRIMARY)),
            height=400, showlegend=False, **create_chart_template()
        )
        st.plotly_chart(fig_pie, use_container_width=True, key="expense_pie")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        df_exp = pd.DataFrame(expenses_data["expenses"]["quarterly"])

        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(x=df_exp["quarter"], y=df_exp["total_expenses"], name="Total", mode="lines+markers", line=dict(color=DANGER, width=3), fill="tozeroy", fillcolor="rgba(239, 68, 68, 0.1)"))
        fig_line.add_trace(go.Scatter(x=df_exp["quarter"], y=df_exp["cost_of_goods_sold"], name="COGS", mode="lines+markers", line=dict(color=SECONDARY, width=2)))
        fig_line.add_trace(go.Scatter(x=df_exp["quarter"], y=df_exp["employee_costs"], name="Employees", mode="lines+markers", line=dict(color=ACCENT, width=2)))
        fig_line.update_layout(
            title=dict(text="Expense Trends", font=dict(size=16, color=TEXT_PRIMARY)),
            height=400, **create_chart_template()
        )
        st.plotly_chart(fig_line, use_container_width=True, key="expense_trend")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<div style="color: #F8FAFC; font-size: 16px; font-weight: 600; margin-bottom: 16px;">Expense Efficiency Metrics</div>', unsafe_allow_html=True)

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        progress_bar("COGS Efficiency", 100 - exp_summary[ly]["cogs_percentage"], 100, PRIMARY)
        progress_bar("OpEx Control", 100 - exp_summary[ly]["opex_percentage"], 100, SECONDARY)
    with col_b:
        progress_bar("Marketing ROI", (rev_summary[ly]["total_revenue"] / exp_summary[ly]["marketing_advertising"]) * 10, 100, ACCENT)
        progress_bar("Admin Efficiency", (exp_summary[ly]["administrative"] / exp_summary[ly]["total_expenses"]) * 100, 20, ACCENT2)
    with col_c:
        profit_for_year = rev_summary[ly]["total_revenue"] - exp_summary[ly]["total_expenses"]
        metric_row("Interest Coverage", f"{(profit_for_year / exp_summary[ly]['interest_expense']):.1f}x", "Healthy", "success")
        metric_row("Tax Rate", f"{(exp_summary[ly]['taxes_levies'] / profit_for_year * 100):.1f}%", "Normal", "info")
    st.markdown('</div>', unsafe_allow_html=True)

# TAB 4: PROFITABILITY
with tab4:
    st.markdown('<div class="section-title">Profitability Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Margins, returns, and profitability metrics across periods</div>', unsafe_allow_html=True)

    kpis = ops_data["operational_metrics"]["kpis"]["quarterly"]
    df_kpi = pd.DataFrame(kpis)
    df_kpi["year"] = df_kpi["quarter"].str.extract(r"(\d{4})").astype(int)

    sel = [y for y in years if str(y) in rev_summary]
    ly = str(max(sel)) if sel else latest_year
    latest_kpi = df_kpi[df_kpi["year"] == int(ly)].iloc[-1]

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        kpi_card("📊", "Gross Margin", f"{latest_kpi['gross_profit_margin']:.1f}%", "+3.3 pts from 2023", "positive")
    with col2:
        kpi_card("💰", "Net Margin", f"{latest_kpi['net_profit_margin']:.1f}%", "+2.4 pts from 2023", "positive")
    with col3:
        kpi_card("📈", "EBITDA Margin", f"{latest_kpi['ebitda_margin']:.1f}%", "+2.7 pts from 2023", "positive")
    with col4:
        kpi_card("🏦", "ROE", f"{latest_kpi['return_on_equity']:.1f}%", "+4.4 pts from 2023", "positive")

    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    fig_margins = go.Figure()
    fig_margins.add_trace(go.Scatter(x=df_kpi["quarter"], y=df_kpi["gross_profit_margin"], name="Gross Margin", mode="lines+markers", line=dict(color=PRIMARY, width=3)))
    fig_margins.add_trace(go.Scatter(x=df_kpi["quarter"], y=df_kpi["ebitda_margin"], name="EBITDA Margin", mode="lines+markers", line=dict(color=SECONDARY, width=3)))
    fig_margins.add_trace(go.Scatter(x=df_kpi["quarter"], y=df_kpi["net_profit_margin"], name="Net Margin", mode="lines+markers", line=dict(color=ACCENT, width=3)))
    fig_margins.update_layout(
        title=dict(text="Margin Expansion Over Time", font=dict(size=18, color=TEXT_PRIMARY)),
        height=380, **create_chart_template()
    )
    st.plotly_chart(fig_margins, use_container_width=True, key="profit_margins")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        years_avail = [y for y in ["2023", "2024", "2025"] if y in rev_summary and int(y) in selected]
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(name="Gross Profit", x=years_avail, y=[rev_summary[y]["total_revenue"] - exp_summary[y]["cost_of_goods_sold"] for y in years_avail], marker_color=PRIMARY))
        fig_bar.add_trace(go.Bar(name="Operating Profit", x=years_avail, y=[rev_summary[y]["total_revenue"] - exp_summary[y]["total_expenses"] + exp_summary[y]["interest_expense"] + exp_summary[y]["depreciation"] for y in years_avail], marker_color=SECONDARY))
        fig_bar.add_trace(go.Bar(name="Net Profit", x=years_avail, y=[rev_summary[y]["total_revenue"] - exp_summary[y]["total_expenses"] for y in years_avail], marker_color=ACCENT))
        fig_bar.update_layout(
            title=dict(text="Annual Profit Layers", font=dict(size=16, color=TEXT_PRIMARY)),
            barmode="group", height=320, **create_chart_template()
        )
        st.plotly_chart(fig_bar, use_container_width=True, key="profit_bar")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig_returns = go.Figure()
        fig_returns.add_trace(go.Scatter(x=df_kpi["quarter"], y=df_kpi["return_on_equity"], name="ROE", mode="lines+markers", line=dict(color=ACCENT2, width=3)))
        fig_returns.add_trace(go.Scatter(x=df_kpi["quarter"], y=df_kpi["return_on_assets"], name="ROA", mode="lines+markers", line=dict(color=DANGER, width=3)))
        fig_returns.add_shape(type="line", x0=0, x1=11, y0=15, y1=15, line=dict(color=TEXT_MUTED, width=1, dash="dash"))
        fig_returns.add_annotation(x=11, y=15, text="Target", showarrow=False, font=dict(color=TEXT_MUTED, size=12))
        fig_returns.update_layout(
            title=dict(text="Returns vs Target", font=dict(size=16, color=TEXT_PRIMARY)),
            height=320, **create_chart_template()
        )
        st.plotly_chart(fig_returns, use_container_width=True, key="profit_returns")
        st.markdown('</div>', unsafe_allow_html=True)

# TAB 5: FUEL SALES
with tab5:
    st.markdown('<div class="section-title">Fuel Sales Volume</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Track liters sold, fuel mix, and LPG performance</div>', unsafe_allow_html=True)

    fuel_summary = fuel_data["fuel_sales_volume"]["annual_summary"]
    sel = [y for y in years if str(y) in fuel_summary]
    ly = str(max(sel)) if sel else latest_year

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        kpi_card("🛢️", "Total Volume", f"{fuel_summary[ly]['total_liters']/1e9:.2f}B Liters", "+19.1% YoY", "positive")
    with col2:
        kpi_card("📊", "Avg Daily", f"{fuel_summary[ly]['avg_daily_liters']/1e6:.2f}M L", "Growing", "positive")
    with col3:
        kpi_card("🔥", "LPG Sales", f"{fuel_summary[ly]['lpg_tons']:,} Tons", "+21.6% YoY", "positive")
    with col4:
        kpi_card("⛽", "PMS Share", f"{fuel_data['fuel_sales_volume']['fuel_type_mix'][ly]['pms_percent']:.1f}%", "Dominant", "positive")

    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    df_fuel = pd.DataFrame(fuel_data["fuel_sales_volume"]["monthly"])

    fig_fuel = go.Figure()
    fig_fuel.add_trace(go.Scatter(x=df_fuel["month"], y=df_fuel["pms_liters"], name="PMS", mode="lines+markers", line=dict(color=PRIMARY, width=2)))
    fig_fuel.add_trace(go.Scatter(x=df_fuel["month"], y=df_fuel["diesel_liters"], name="Diesel", mode="lines+markers", line=dict(color=SECONDARY, width=2)))
    fig_fuel.add_trace(go.Scatter(x=df_fuel["month"], y=df_fuel["kerosene_liters"], name="Kerosene", mode="lines+markers", line=dict(color=ACCENT, width=2, dash="dash")))
    fig_fuel.update_layout(
        title=dict(text="Monthly Volume Trends", font=dict(size=18, color=TEXT_PRIMARY)),
        height=420, **create_chart_template()
    )
    st.plotly_chart(fig_fuel, use_container_width=True, key="fuel_trend")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fuel_mix = fuel_data["fuel_sales_volume"]["fuel_type_mix"]
        fig_mix = px.pie(
            values=[fuel_mix[ly]["pms_percent"], fuel_mix[ly]["diesel_percent"], fuel_mix[ly]["kerosene_percent"]],
            names=["PMS (Petrol)", "Diesel", "Kerosene"],
            hole=0.6,
            color_discrete_sequence=[PRIMARY, SECONDARY, ACCENT]
        )
        fig_mix.update_traces(textposition="inside", textinfo="percent+label", textfont=dict(color=TEXT_PRIMARY))
        fig_mix.update_layout(
            title=dict(text=f"Fuel Mix ({ly})", font=dict(size=16, color=TEXT_PRIMARY)),
            height=380, showlegend=False, **create_chart_template()
        )
        st.plotly_chart(fig_mix, use_container_width=True, key="fuel_mix")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig_lpg = go.Figure()
        fig_lpg.add_trace(go.Bar(x=df_fuel["month"], y=df_fuel["lpg_tons"], marker_color=SECONDARY, name="LPG Tons"))
        fig_lpg.update_layout(
            title=dict(text="LPG Sales Trend", font=dict(size=16, color=TEXT_PRIMARY)),
            height=380, **create_chart_template()
        )
        st.plotly_chart(fig_lpg, use_container_width=True, key="fuel_lpg")
        st.markdown('</div>', unsafe_allow_html=True)

# TAB 6: BALANCE SHEET
with tab6:
    st.markdown('<div class="section-title">Balance Sheet</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Assets, liabilities, equity positions and financial health</div>', unsafe_allow_html=True)

    bs = bs_data["balance_sheet"]["annual"]
    ratios = bs_data["balance_sheet"]["key_ratios"]
    sel = [y for y in years if str(y) in bs]
    ly = str(max(sel)) if sel else latest_year

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        kpi_card("🏦", "Total Assets", format_ghs(bs[ly]["assets"]["total_assets"]), f"{((bs[ly]['assets']['total_assets']/bs['2023']['assets']['total_assets'])-1)*100:.1f}% since 2023", "positive")
    with col2:
        kpi_card("💎", "Total Equity", format_ghs(bs[ly]["equity"]["total_equity"]), f"{((bs[ly]['equity']['total_equity']/bs['2023']['equity']['total_equity'])-1)*100:.1f}% growth", "positive")
    with col3:
        kpi_card("💵", "Working Capital", format_ghs(ratios[ly]["working_capital"]), f"+{((ratios[ly]['working_capital']/ratios['2023']['working_capital'])-1)*100:.1f}%", "positive")
    with col4:
        kpi_card("📊", "Debt/Equity", f"{ratios[ly]['debt_to_equity']:.2f}", f"-{((ratios['2023']['debt_to_equity']-ratios[ly]['debt_to_equity'])/ratios['2023']['debt_to_equity']*100):.1f}%", "positive")

    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    years_avail = [y for y in ["2023", "2024", "2025"] if y in bs and int(y) in selected]
    fig_bs = go.Figure()
    fig_bs.add_trace(go.Bar(name="Assets", x=years_avail, y=[bs[y]["assets"]["total_assets"] for y in years_avail], marker_color=PRIMARY))
    fig_bs.add_trace(go.Bar(name="Liabilities", x=years_avail, y=[bs[y]["liabilities"]["total_liabilities"] for y in years_avail], marker_color=DANGER))
    fig_bs.add_trace(go.Bar(name="Equity", x=years_avail, y=[bs[y]["equity"]["total_equity"] for y in years_avail], marker_color=SECONDARY))
    fig_bs.update_layout(
        title=dict(text="Balance Sheet Evolution", font=dict(size=18, color=TEXT_PRIMARY)),
        barmode="group", height=380, **create_chart_template()
    )
    st.plotly_chart(fig_bs, use_container_width=True, key="bs_chart")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig_asset = px.pie(
            values=[bs[ly]["assets"]["current_assets"]["total_current_assets"], bs[ly]["assets"]["non_current_assets"]["net_ppe"], bs[ly]["assets"]["non_current_assets"]["intangible_assets"], bs[ly]["assets"]["non_current_assets"]["long_term_investments"]],
            names=["Current Assets", "Net PPE", "Intangibles", "Long-term Investments"],
            hole=0.5,
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_asset.update_traces(textposition="inside", textinfo="percent+label", textfont=dict(color=TEXT_PRIMARY))
        fig_asset.update_layout(
            title=dict(text=f"Asset Composition ({ly})", font=dict(size=16, color=TEXT_PRIMARY)),
            height=360, showlegend=False, **create_chart_template()
        )
        st.plotly_chart(fig_asset, use_container_width=True, key="bs_asset")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig_liq = go.Figure()
        fig_liq.add_trace(go.Scatter(x=years_avail, y=[ratios[y]["current_ratio"] for y in years_avail], name="Current Ratio", mode="lines+markers", line=dict(color=PRIMARY, width=3)))
        fig_liq.add_trace(go.Scatter(x=years_avail, y=[ratios[y]["quick_ratio"] for y in years_avail], name="Quick Ratio", mode="lines+markers", line=dict(color=ACCENT, width=3)))
        fig_liq.add_shape(type="line", x0=0, x1=2, y0=1.5, y1=1.5, line=dict(color=TEXT_MUTED, width=1, dash="dash"))
        fig_liq.update_layout(
            title=dict(text="Liquidity Trends", font=dict(size=16, color=TEXT_PRIMARY)),
            height=360, **create_chart_template()
        )
        st.plotly_chart(fig_liq, use_container_width=True, key="bs_liq")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    with st.expander("📋 Detailed Balance Sheet"):
        st.markdown(f"""
            <div class="metric-row">
                <span style="color: {TEXT_SECONDARY};">Cash & Equivalents</span>
                <span style="color: {TEXT_PRIMARY}; font-weight: 600;">{format_ghs(bs[ly]['assets']['current_assets']['cash_and_equivalents'])}</span>
            </div>
            <div class="metric-row">
                <span style="color: {TEXT_SECONDARY};">Accounts Receivable</span>
                <span style="color: {TEXT_PRIMARY}; font-weight: 600;">{format_ghs(bs[ly]['assets']['current_assets']['accounts_receivable'])}</span>
            </div>
            <div class="metric-row">
                <span style="color: {TEXT_SECONDARY};">Inventory</span>
                <span style="color: {TEXT_PRIMARY}; font-weight: 600;">{format_ghs(bs[ly]['assets']['current_assets']['inventory'])}</span>
            </div>
            <div class="metric-row">
                <span style="color: {TEXT_SECONDARY};">Net PPE</span>
                <span style="color: {TEXT_PRIMARY}; font-weight: 600;">{format_ghs(bs[ly]['assets']['non_current_assets']['net_ppe'])}</span>
            </div>
            <div class="metric-row">
                <span style="color: {TEXT_SECONDARY};">Long-term Debt</span>
                <span style="color: {TEXT_PRIMARY}; font-weight: 600;">{format_ghs(bs[ly]['liabilities']['non_current_liabilities']['long_term_debt'])}</span>
            </div>
        """, unsafe_allow_html=True)

# TAB 7: CASH FLOW
with tab7:
    st.markdown('<div class="section-title">Cash Flow Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Operating, investing, and financing cash movements</div>', unsafe_allow_html=True)

    cf_summary = cf_data["cash_flow"]["annual_summary"]
    sel = [y for y in years if str(y) in cf_summary]
    ly = str(max(sel)) if sel else latest_year

    col1, col2, col3 = st.columns(3)
    with col1:
        kpi_card("💵", "Operating CF", format_ghs(cf_summary[ly]["net_cash_from_operations"]), f"+{((cf_summary[ly]['net_cash_from_operations']/cf_summary['2023']['net_cash_from_operations'])-1)*100:.1f}% vs 2023", "positive")
    with col2:
        kpi_card("📈", "Free Cash Flow", format_ghs(cf_summary[ly]["free_cash_flow"]), f"+{((cf_summary[ly]['free_cash_flow']/cf_summary['2023']['free_cash_flow'])-1)*100:.1f}% vs 2023", "positive")
    with col3:
        kpi_card("🏗️", "CapEx", format_ghs(abs(cf_summary[ly]["capex"])), "Investing in Growth", "positive")

    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    years_avail = [y for y in ["2023", "2024", "2025"] if y in cf_summary and int(y) in selected]
    fig_cf = go.Figure()
    fig_cf.add_trace(go.Bar(name="Operating", x=years_avail, y=[cf_summary[y]["net_cash_from_operations"] for y in years_avail], marker_color=PRIMARY))
    fig_cf.add_trace(go.Bar(name="Investing", x=years_avail, y=[cf_summary[y]["net_cash_from_investing"] for y in years_avail], marker_color=DANGER))
    fig_cf.add_trace(go.Bar(name="Financing", x=years_avail, y=[cf_summary[y]["net_cash_from_financing"] for y in years_avail], marker_color=ACCENT))
    fig_cf.update_layout(
        title=dict(text="Cash Flow Components", font=dict(size=18, color=TEXT_PRIMARY)),
        barmode="group", height=380, **create_chart_template()
    )
    st.plotly_chart(fig_cf, use_container_width=True, key="cf_components")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        df_fcf = pd.DataFrame({k: v["free_cash_flow"] for k, v in cf_summary.items() if int(k) in selected}, index=["FCF"]).T
        df_fcf["year"] = df_fcf.index
        fig_fcf = go.Figure()
        fig_fcf.add_trace(go.Scatter(x=df_fcf["year"], y=df_fcf["FCF"], name="Free Cash Flow", mode="lines+markers", line=dict(color=SECONDARY, width=3), fill="tozeroy", fillcolor="rgba(245, 158, 11, 0.15)"))
        fig_fcf.update_layout(
            title=dict(text="Free Cash Flow Growth", font=dict(size=16, color=TEXT_PRIMARY)),
            height=340, **create_chart_template()
        )
        st.plotly_chart(fig_fcf, use_container_width=True, key="cf_fcf")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        cf_q = cf_data["cash_flow"]["quarterly"]
        df_cf_q = pd.DataFrame(cf_q)
        fig_qcf = go.Figure()
        fig_qcf.add_trace(go.Bar(x=df_cf_q["quarter"], y=df_cf_q["free_cash_flow"], marker_color=[PRIMARY if v >= 0 else DANGER for v in df_cf_q["free_cash_flow"]], name="Quarterly FCF"))
        fig_qcf.update_layout(
            title=dict(text="Quarterly Free Cash Flow", font=dict(size=16, color=TEXT_PRIMARY)),
            height=340, **create_chart_template()
        )
        st.plotly_chart(fig_qcf, use_container_width=True, key="cf_quarterly")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<div style="color: #F8FAFC; font-size: 16px; font-weight: 600; margin-bottom: 16px;">Cash Flow Health Check</div>', unsafe_allow_html=True)
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        progress_bar("Operating CF Margin", (cf_summary[ly]["net_cash_from_operations"] / rev_summary[ly]["total_revenue"]) * 100, 20, PRIMARY)
        progress_bar("FCF Conversion", (cf_summary[ly]["free_cash_flow"] / cf_summary[ly]["net_cash_from_operations"]) * 100, 100, SECONDARY)
    with col_b:
        metric_row("Dividends Paid", format_ghs(cf_summary[ly]["dividends_paid"]), "Consistent", "info")
        metric_row("Debt Reduction", format_ghs(abs(cf_summary[ly]["net_cash_from_financing"])), "Active", "success")
    with col_c:
        metric_row("CapEx / Revenue", f"{(abs(cf_summary[ly]['capex']) / rev_summary[ly]['total_revenue'] * 100):.1f}%", "Reinvesting", "info")
        metric_row("Cash Conversion", f"{(cf_summary[ly]['net_cash_from_operations'] / (rev_summary[ly]['total_revenue'] - exp_summary[ly]['total_expenses']) * 100):.1f}%", "Strong", "success")
    st.markdown('</div>', unsafe_allow_html=True)

# TAB 8: OPERATIONS
with tab8:
    st.markdown('<div class="section-title">Operations Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Station network, workforce, customer metrics, and safety</div>', unsafe_allow_html=True)

    stations = ops_data["operational_metrics"]["station_network"]
    employees = ops_data["operational_metrics"]["employee_metrics"]
    customers = ops_data["operational_metrics"]["customer_metrics"]
    sel = [y for y in years if str(y) in stations]
    ly = str(max(sel)) if sel else latest_year

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        kpi_card("⛽", "Total Stations", f"{stations[ly]['total_stations']:,}", f"+{stations[ly]['new_stations_opened']} new", "positive")
    with col2:
        kpi_card("⏱️", "Uptime", f"{stations[ly]['operational_uptime_percent']:.1f}%", "Excellent", "positive")
    with col3:
        kpi_card("😊", "Satisfaction", f"{customers[ly]['customer_satisfaction_score']:.1f}/100", "+5.3 pts", "positive")
    with col4:
        kpi_card("🎯", "NPS Score", str(customers[ly]['nps_score']), "+10 pts", "positive")

    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        years_avail = [y for y in ["2023", "2024", "2025"] if y in stations and int(y) in selected]
        fig_station = go.Figure()
        fig_station.add_trace(go.Bar(name="Company Owned", x=years_avail, y=[stations[y]["company_owned"] for y in years_avail], marker_color=PRIMARY))
        fig_station.add_trace(go.Bar(name="Dealer Owned", x=years_avail, y=[stations[y]["dealer_owned"] for y in years_avail], marker_color=SECONDARY))
        fig_station.add_trace(go.Bar(name="Franchise", x=years_avail, y=[stations[y]["franchise"] for y in years_avail], marker_color=ACCENT))
        fig_station.update_layout(
            title=dict(text="Station Network Growth", font=dict(size=16, color=TEXT_PRIMARY)),
            barmode="stack", height=340, **create_chart_template()
        )
        st.plotly_chart(fig_station, use_container_width=True, key="ops_stations")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig_emp = go.Figure()
        fig_emp.add_trace(go.Scatter(x=years_avail, y=[employees[y]["total_employees"] for y in years_avail], name="Employees", mode="lines+markers", line=dict(color=PRIMARY, width=3), fill="tozeroy", fillcolor="rgba(16, 185, 129, 0.1)"))
        fig_emp.add_trace(go.Scatter(x=years_avail, y=[employees[y]["avg_salary_ghs"] for y in years_avail], name="Avg Salary (scaled)", mode="lines+markers", line=dict(color=SECONDARY, width=2, dash="dash"), yaxis="y2"))
        fig_emp.update_layout(
            title=dict(text="Workforce Growth & Compensation", font=dict(size=16, color=TEXT_PRIMARY)),
            height=340, **create_chart_template(),
            yaxis2=dict(overlaying="y", side="right", showgrid=False)
        )
        st.plotly_chart(fig_emp, use_container_width=True, key="ops_employees")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig_loyalty = go.Figure()
        fig_loyalty.add_trace(go.Scatter(x=years_avail, y=[customers[y]["loyalty_program_members"] for y in years_avail], name="Members", mode="lines+markers", line=dict(color=ACCENT2, width=3), fill="tozeroy", fillcolor="rgba(139, 92, 246, 0.1)"))
        fig_loyalty.update_layout(
            title=dict(text="Loyalty Program Growth", font=dict(size=14, color=TEXT_PRIMARY)),
            height=300, **create_chart_template()
        )
        st.plotly_chart(fig_loyalty, use_container_width=True, key="ops_loyalty")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig_safety = go.Figure()
        fig_safety.add_trace(go.Bar(x=years_avail, y=[employees[y]["safety_incidents"] for y in years_avail], marker_color=DANGER, name="Incidents"))
        fig_safety.update_layout(
            title=dict(text="Safety Incidents", font=dict(size=14, color=TEXT_PRIMARY)),
            height=300, **create_chart_template()
        )
        st.plotly_chart(fig_safety, use_container_width=True, key="ops_safety")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_c:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div style="color: #F8FAFC; font-size: 14px; font-weight: 600; margin-bottom: 16px;">Training & Development</div>', unsafe_allow_html=True)
        progress_bar("Training hrs/emp", employees[ly]["training_hours_per_employee"], 60, PRIMARY)
        progress_bar("Turnover (inverse)", 100 - employees[ly]["employee_turnover_percent"], 100, SECONDARY)
        metric_row("Fleet Accounts", f"{customers[ly]['active_fleet_accounts']:,}", "+800", "success")
        metric_row("Avg Transaction", f"GHS {customers[ly]['avg_transaction_value_ghs']:,}", "+18%", "positive")
        st.markdown('</div>', unsafe_allow_html=True)

# FOOTER
st.markdown("<div style='height: 48px;'></div>", unsafe_allow_html=True)
st.markdown(f"""
    <div class="footer">
        Goil Ghana Limited • Financial Dashboard • Data Period: 2023 - 2025<br>
        <span style="color: {TEXT_MUTED}; font-size: 12px;">All figures in Ghana Cedis (GHS) • Mock data for demonstration purposes</span>
    </div>
""", unsafe_allow_html=True)
