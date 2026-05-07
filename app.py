import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
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

# Dynamic color system
C = {
    "bg": "#0F172A",
    "card": "rgba(30, 41, 59, 0.7)",
    "border": "#334155",
    "primary": "#10B981",
    "primary_d": "rgba(16, 185, 129, 0.15)",
    "secondary": "#F59E0B",
    "secondary_d": "rgba(245, 158, 11, 0.15)",
    "accent": "#3B82F6",
    "accent_d": "rgba(59, 130, 246, 0.15)",
    "purple": "#8B5CF6",
    "purple_d": "rgba(139, 92, 246, 0.15)",
    "danger": "#EF4444",
    "danger_d": "rgba(239, 68, 68, 0.15)",
    "text": "#F8FAFC",
    "text2": "#94A3B8",
    "muted": "#64748B",
}

def inject_css():
    c = C
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    * {{ font-family: 'Inter', sans-serif !important; }}
    .stApp {{
        background: linear-gradient(135deg, {c["bg"]} 0%, #1E1B4B 50%, {c["bg"]} 100%);
        color: {c["text"]};
    }}
    [data-testid="stSidebar"] {{
        background: rgba(15, 23, 42, 0.95);
        backdrop-filter: blur(20px);
        border-right: 1px solid {c["border"]};
    }}
    .glass-card {{
        background: {c["card"]};
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 24px;
        margin: 8px 0;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }}
    .glass-card::before {{
        content: '';
        position: absolute; top: 0; left: 0; right: 0; height: 3px;
        background: linear-gradient(90deg, {c["primary"]}, {c["secondary"]}, {c["accent"]});
        opacity: 0; transition: opacity 0.4s ease;
    }}
    .glass-card:hover {{ transform: translateY(-6px); box-shadow: 0 25px 50px rgba(0,0,0,0.4); border-color: {c["primary"]}; }}
    .glass-card:hover::before {{ opacity: 1; }}
    .kpi-icon {{ font-size: 34px; margin-bottom: 12px; display: inline-block; animation: float 3s ease-in-out infinite; }}
    @keyframes float {{ 0%,100% {{ transform: translateY(0px); }} 50% {{ transform: translateY(-6px); }} }}
    .kpi-label {{ color: {c["text2"]}; font-size: 13px; font-weight: 600; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 1.5px; }}
    .kpi-value {{ color: {c["text"]}; font-size: 28px; font-weight: 800; margin-bottom: 8px; }}
    .kpi-delta {{ font-size: 13px; font-weight: 600; display: inline-flex; align-items: center; gap: 5px; padding: 5px 10px; border-radius: 8px; }}
    .delta-positive {{ color: {c["primary"]}; background: {c["primary_d"]}; }}
    .delta-negative {{ color: {c["danger"]}; background: {c["danger_d"]}; }}
    .section-title {{ font-size: 30px; font-weight: 800; margin-bottom: 8px; background: linear-gradient(135deg, {c["text"]}, {c["text2"]}); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
    .section-subtitle {{ color: {c["text2"]}; font-size: 15px; margin-bottom: 32px; }}
    .chart-container {{
        background: {c["card"]}; backdrop-filter: blur(16px);
        border: 1px solid rgba(255,255,255,0.08); border-radius: 20px; padding: 24px; margin: 12px 0;
    }}
    .stTabs [data-baseweb="tab-list"] {{ gap: 10px; margin-bottom: 20px; }}
    .stTabs [data-baseweb="tab"] {{
        background: {c["card"]}; backdrop-filter: blur(10px); border: 1px solid {c["border"]};
        border-radius: 14px; padding: 10px 20px; color: {c["text2"]}; font-weight: 600; font-size: 13px; transition: all 0.3s ease;
    }}
    .stTabs [aria-selected="true"] {{ background: linear-gradient(135deg, {c["primary"]}, #059669); border-color: {c["primary"]}; color: white; box-shadow: 0 6px 20px rgba(16,185,129,0.4); }}
    .stTabs [data-baseweb="tab"]:hover:not([aria-selected="true"]) {{ border-color: {c["primary"]}; color: {c["text"]}; }}
    .metric-row {{
        display: flex; justify-content: space-between; align-items: center;
        padding: 12px 16px; background: {c["card"]}; backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.08); border-radius: 14px; margin: 6px 0; transition: all 0.3s ease;
    }}
    .metric-row:hover {{ border-color: {c["accent"]}; background: {c["accent_d"]}; transform: translateX(4px); }}
    .badge {{ display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; }}
    .badge-success {{ background: {c["primary_d"]}; color: {c["primary"]}; }}
    .badge-warning {{ background: {c["secondary_d"]}; color: {c["secondary"]}; }}
    .badge-info {{ background: {c["accent_d"]}; color: {c["accent"]}; }}
    .badge-danger {{ background: {c["danger_d"]}; color: {c["danger"]}; }}
    .live-indicator {{
        display: inline-flex; align-items: center; gap: 8px; padding: 8px 16px;
        background: {c["primary_d"]}; border: 1px solid rgba(16,185,129,0.3); border-radius: 24px; font-size: 13px; color: {c["primary"]}; font-weight: 600;
    }}
    .live-dot {{ width: 10px; height: 10px; background: {c["primary"]}; border-radius: 50%; animation: pulse 2s infinite; box-shadow: 0 0 10px {c["primary"]}; }}
    @keyframes pulse {{ 0%,100% {{ opacity: 1; box-shadow: 0 0 10px {c["primary"]}; }} 50% {{ opacity: 0.5; box-shadow: 0 0 20px {c["primary"]}; }} }}
    .footer {{ text-align: center; padding: 36px 0; color: {c["muted"]}; font-size: 13px; border-top: 1px solid {c["border"]}; margin-top: 48px; }}
    div[data-testid="stExpander"] {{ background: {c["card"]}; border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; }}
    div[data-testid="stExpander"] > div:first-child {{ color: {c["text"]}; font-weight: 600; }}
    ::-webkit-scrollbar {{ width: 8px; height: 8px; }}
    ::-webkit-scrollbar-track {{ background: {c["bg"]}; }}
    ::-webkit-scrollbar-thumb {{ background: {c["border"]}; border-radius: 4px; }}
    ::-webkit-scrollbar-thumb:hover {{ background: {c["muted"]}; }}
    </style>
    """, unsafe_allow_html=True)

inject_css()

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

def load_data(filename):
    filepath = os.path.join(DATA_DIR, filename)
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"Missing data file: {filename}")
        st.stop()
    except json.JSONDecodeError:
        st.error(f"Invalid JSON in {filename}")
        st.stop()
    except Exception as e:
        st.error(f"Error loading {filename}: {str(e)}")
        st.stop()

def get_years(data, *keys):
    """Dynamically extract available years from nested data"""
    d = data
    for k in keys:
        d = d.get(k, {})
    return sorted([int(k) for k in d.keys() if k.isdigit() and len(k) == 4])

revenue_data = load_data("revenue.json")
expenses_data = load_data("expenses.json")
fuel_data = load_data("fuel_sales_volume.json")
ops_data = load_data("operational_metrics.json")
bs_data = load_data("balance_sheet.json")
cf_data = load_data("cash_flow.json")

# Dynamic year detection
ALL_YEARS = sorted(set(
    get_years(revenue_data, "revenue", "annual_summary") +
    get_years(expenses_data, "expenses", "annual_summary") +
    get_years(fuel_data, "fuel_sales_volume", "annual_summary") +
    get_years(bs_data, "balance_sheet", "annual") +
    get_years(cf_data, "cash_flow", "annual_summary")
))

def format_ghs(value):
    if value >= 1e9: return f"GHS {value/1e9:.2f}B"
    elif value >= 1e6: return f"GHS {value/1e6:.2f}M"
    elif value >= 1e3: return f"GHS {value/1e3:.2f}K"
    return f"GHS {value:,.0f}"

def safe_div(a, b, default=0):
    return a / b if b != 0 else default

def kpi_card(icon, label, value, delta=None, delta_type="positive"):
    cls = "delta-positive" if delta_type == "positive" else "delta-negative"
    arrow = "↑" if delta_type == "positive" else "↓"
    delta_html = f'<span class="kpi-delta {cls}">{arrow} {delta}</span>' if delta else ""
    st.markdown(f'<div class="glass-card"><div class="kpi-icon">{icon}</div><div class="kpi-label">{label}</div><div class="kpi-value">{value}</div>{delta_html}</div>', unsafe_allow_html=True)

def progress_bar(label, value, max_val, color=None):
    color = color or C["primary"]
    pct = min(100, (value / max_val * 100) if max_val else 0)
    st.markdown(f'''
    <div style="margin: 10px 0;">
        <div style="display:flex;justify-content:space-between;margin-bottom:6px;color:{C["text2"]};font-size:12px;font-weight:500;">
            <span>{label}</span><span style="color:{C["text"]};font-weight:700;">{pct:.1f}%</span>
        </div>
        <div style="background:rgba(255,255,255,0.08);border-radius:10px;height:10px;overflow:hidden;">
            <div style="width:{pct}%;background:linear-gradient(90deg,{color},{C["secondary"]});height:100%;border-radius:10px;transition:width 1s cubic-bezier(0.4,0,0.2,1);"></div>
        </div>
    </div>''', unsafe_allow_html=True)

def metric_row(label, value, badge=None, badge_type="info"):
    badge_html = f'<span class="badge badge-{badge_type}">{badge}</span>' if badge else ""
    st.markdown(f'<div class="metric-row"><span style="color:{C["text2"]};font-size:13px;">{label}</span><div style="display:flex;align-items:center;gap:10px;">{badge_html}<span style="color:{C["text"]};font-weight:700;font-size:13px;">{value}</span></div></div>', unsafe_allow_html=True)

def chart_cfg():
    return dict(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=C["text2"], family="Inter", size=11),
        xaxis=dict(gridcolor=C["border"], zeroline=False),
        yaxis=dict(gridcolor=C["border"], zeroline=False),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color=C["text2"], size=10))
    )

# SIDEBAR
with st.sidebar:
    st.markdown('''
    <div style="text-align:center;padding:20px 0;">
        <div style="font-size:48px;margin-bottom:8px;">⛽</div>
        <div style="font-size:22px;font-weight:800;color:#F8FAFC;">GOIL GHANA</div>
        <div style="font-size:11px;color:#94A3B8;text-transform:uppercase;letter-spacing:2px;">Financial Dashboard</div>
    </div>''', unsafe_allow_html=True)
    st.divider()

    st.markdown(f'<div style="color:{C["muted"]};font-size:11px;text-transform:uppercase;letter-spacing:1px;margin-bottom:10px;">Time Period</div>', unsafe_allow_html=True)
    years = st.multiselect("Select Year", ALL_YEARS, default=ALL_YEARS, label_visibility="collapsed")

    st.markdown(f'<div style="color:{C["muted"]};font-size:11px;text-transform:uppercase;letter-spacing:1px;margin:14px 0 10px;">Quarters</div>', unsafe_allow_html=True)
    quarters = st.multiselect("Select Quarters", ["Q1","Q2","Q3","Q4"], default=["Q1","Q2","Q3","Q4"], label_visibility="collapsed")

    st.divider()
    st.markdown(f'''
    <div class="live-indicator"><span class="live-dot"></span>Live Data</div>''', unsafe_allow_html=True)
    st.divider()
    st.markdown(f'''
    <div style="color:{C["muted"]};font-size:11px;text-align:center;margin-top:14px;">
        Currency: <span style="color:{C["text"]};font-weight:600;">GHS (₵)</span><br>
        Last Updated: <span style="color:{C["text"]};">{datetime.now().strftime("%b %d, %Y")}</span>
    </div>''', unsafe_allow_html=True)

# MAIN CONTENT
rev_sum = revenue_data["revenue"]["annual_summary"]
exp_sum = expenses_data["expenses"]["annual_summary"]
selected_years = [str(y) for y in years if str(y) in rev_sum]

if not selected_years:
    st.warning("No data for selected years. Please adjust your filters.")
    st.stop()

latest_year = str(max(int(y) for y in selected_years))

# HEADER
st.markdown(f'''
<div style="margin-bottom:28px;">
    <div style="display:flex;justify-content:space-between;align-items:center;">
        <div>
            <div class="section-title">Financial Performance Dashboard</div>
            <div class="section-subtitle">Comprehensive analytics for Goil Ghana Limited • {latest_year}</div>
        </div>
        <div class="live-indicator"><span class="live-dot"></span>FY {latest_year}</div>
    </div>
</div>''', unsafe_allow_html=True)

# TABS
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "📊 Overview", "💰 Revenue", "💸 Expenses", "📈 Profitability",
    "⛽ Fuel Sales", "🏦 Balance Sheet", "💵 Cash Flow", "⚙️ Operations"
])

# TAB 1: OVERVIEW
with tab1:
    lr = rev_sum[latest_year]
    le = exp_sum[latest_year]
    profit = lr["total_revenue"] - le["total_expenses"]
    margin = safe_div(profit, lr["total_revenue"]) * 100
    rev_growth = lr.get("yoy_growth")
    stations = ops_data["operational_metrics"]["station_network"][latest_year]["total_stations"]
    fuel_vol = fuel_data["fuel_sales_volume"]["annual_summary"][latest_year]["total_liters"]
    employees = ops_data["operational_metrics"]["employee_metrics"][latest_year]["total_employees"]

    cols = st.columns(6)
    with cols[0]: kpi_card("💰", "Total Revenue", format_ghs(lr["total_revenue"]), f"{rev_growth:.1f}% YoY" if rev_growth else "Base Year", "positive")
    with cols[1]: kpi_card("📈", "Net Profit", format_ghs(profit), f"{margin:.1f}% Margin", "positive" if profit >= 0 else "negative")
    with cols[2]: kpi_card("💸", "Total Expenses", format_ghs(le["total_expenses"]), f"{safe_div(le['total_expenses'], lr['total_revenue'])*100:.1f}% of Rev", "negative")
    with cols[3]: kpi_card("⛽", "Stations", f"{stations:,}", "+34 New Sites", "positive")
    with cols[4]: kpi_card("🛢️", "Fuel Volume", f"{fuel_vol/1e9:.2f}B L", "+19.1% YoY", "positive")
    with cols[5]: kpi_card("👥", "Employees", f"{employees:,}", "+240 Added", "positive")

    st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)
    col_l, col_r = st.columns([2, 1])

    with col_l:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        df = pd.DataFrame(revenue_data["revenue"]["quarterly"])
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df["quarter"], y=df["total_revenue"], name="Total Revenue", mode="lines+markers", line=dict(color=C["primary"], width=3), fill="tozeroy", fillcolor=C["primary_d"]))
        fig.add_trace(go.Scatter(x=df["quarter"], y=df["fuel_sales"], name="Fuel Sales", mode="lines+markers", line=dict(color=C["secondary"], width=2)))
        fig.update_layout(title=dict(text="Revenue Trajectory", font=dict(size=17, color=C["text"])), height=370, **chart_cfg())
        st.plotly_chart(fig, use_container_width=True, key="ov_rev")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_r:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown(f'<div style="color:{C["text"]};font-size:15px;font-weight:600;margin-bottom:14px;">Revenue Composition</div>', unsafe_allow_html=True)
        fig = px.pie(values=[lr[k] for k in ["fuel_sales","lubricants","convenience_store","fleet_services","other_income"]],
                      names=["Fuel Sales","Lubricants","Convenience","Fleet","Other"], hole=0.6,
                      color_discrete_sequence=[C["primary"],C["secondary"],C["accent"],C["purple"],C["danger"]])
        fig.update_traces(textposition="inside", textinfo="percent+label", textfont=dict(color=C["text"]))
        fig.update_layout(height=370, showlegend=False, **chart_cfg())
        st.plotly_chart(fig, use_container_width=True, key="ov_pie")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div style="height:16px;"></div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        yrs = [y for y in ["2023","2024","2025"] if y in rev_sum and int(y) in years]
        fig = go.Figure()
        fig.add_trace(go.Bar(name="Revenue", x=yrs, y=[rev_sum[y]["total_revenue"] for y in yrs], marker_color=C["primary"]))
        fig.add_trace(go.Bar(name="Expenses", x=yrs, y=[exp_sum[y]["total_expenses"] for y in yrs], marker_color=C["danger"]))
        fig.add_trace(go.Bar(name="Profit", x=yrs, y=[rev_sum[y]["total_revenue"]-exp_sum[y]["total_expenses"] for y in yrs], marker_color=C["secondary"]))
        fig.update_layout(title=dict(text="P&L Comparison", font=dict(size=15, color=C["text"])), barmode="group", height=300, **chart_cfg())
        st.plotly_chart(fig, use_container_width=True, key="ov_pl")
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown(f'<div style="color:{C["text"]};font-size:15px;font-weight:600;margin-bottom:14px;">Key Performance Indicators</div>', unsafe_allow_html=True)
        df_kpi = pd.DataFrame(ops_data["operational_metrics"]["kpis"]["quarterly"])
        df_kpi["year"] = df_kpi["quarter"].str.extract(r"(\d{4})").astype(int)
        latest_kpi = df_kpi[df_kpi["year"] == int(latest_year)].iloc[-1]
        progress_bar("Gross Margin", latest_kpi["gross_profit_margin"], 100, C["primary"])
        progress_bar("Net Margin", latest_kpi["net_profit_margin"], 100, C["secondary"])
        progress_bar("EBITDA Margin", latest_kpi["ebitda_margin"], 100, C["accent"])
        progress_bar("ROE", latest_kpi["return_on_equity"], 100, C["purple"])
        st.markdown('</div>', unsafe_allow_html=True)

    with c3:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown(f'<div style="color:{C["text"]};font-size:15px;font-weight:600;margin-bottom:14px;">Quick Stats</div>', unsafe_allow_html=True)
        cm = ops_data["operational_metrics"]["customer_metrics"][latest_year]
        metric_row("Customer Satisfaction", f"{cm['customer_satisfaction_score']:.1f}/100", "Excellent", "success")
        metric_row("NPS Score", str(cm['nps_score']), "Strong", "success")
        metric_row("Station Uptime", f"{ops_data['operational_metrics']['station_network'][latest_year]['operational_uptime_percent']:.1f}%", "99%+", "success")
        metric_row("Inventory Turnover", f"{latest_kpi['inventory_turnover']:.1f}x", "Healthy", "info")
        metric_row("Safety Incidents", str(ops_data['operational_metrics']['employee_metrics'][latest_year]['safety_incidents']), "↓ Improving", "success")
        st.markdown('</div>', unsafe_allow_html=True)

# TAB 2: REVENUE
with tab2:
    st.markdown('<div class="section-title">Revenue Analytics</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Detailed breakdown of revenue streams and growth trends</div>', unsafe_allow_html=True)
    sel = [y for y in years if str(y) in rev_sum]
    ly = str(max(sel)) if sel else latest_year
    lr = rev_sum[ly]

    cols = st.columns(3)
    with cols[0]: kpi_card("📊", "Annual Revenue", format_ghs(lr["total_revenue"]), f"{lr.get('yoy_growth',0):.1f}% Growth", "positive")
    with cols[1]: kpi_card("⛽", "Fuel Revenue", format_ghs(lr["fuel_sales"]), f"{safe_div(lr['fuel_sales'], lr['total_revenue'])*100:.1f}% of Total", "positive")
    with cols[2]: kpi_card("🛢️", "Non-Fuel Revenue", format_ghs(lr["lubricants"]+lr["convenience_store"]+lr["fleet_services"]+lr["other_income"]), "Diversifying", "positive")

    st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    df = pd.DataFrame(revenue_data["revenue"]["quarterly"])
    fig = go.Figure()
    for seg, lbl, clr in zip(["fuel_sales","lubricants","convenience_store","fleet_services","other_income"],
                              ["Fuel Sales","Lubricants","Convenience","Fleet","Other"],
                              [C["primary"],C["secondary"],C["accent"],C["purple"],C["danger"]]):
        fig.add_trace(go.Bar(name=lbl, x=df["quarter"], y=df[seg], marker_color=clr))
    fig.update_layout(title=dict(text="Quarterly Revenue Breakdown", font=dict(size=17, color=C["text"])), barmode="stack", height=430, **chart_cfg())
    st.plotly_chart(fig, use_container_width=True, key="rev_stack")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div style="height:14px;"></div>', unsafe_allow_html=True)
    cl, cr = st.columns(2)

    with cl:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        df["year"] = df["quarter"].str.extract(r"(\d{4})").astype(int)
        df = df.sort_values("year")
        df["qtr_rev"] = df["total_revenue"].pct_change() * 100
        fig = go.Figure(go.Bar(x=df["quarter"], y=df["qtr_rev"], marker_color=[C["primary"] if v >= 0 else C["danger"] for v in df["qtr_rev"]]))
        fig.update_layout(title=dict(text="Quarter-over-Quarter Growth", font=dict(size=15, color=C["text"])), height=310, **chart_cfg())
        st.plotly_chart(fig, use_container_width=True, key="rev_growth")
        st.markdown('</div>', unsafe_allow_html=True)

    with cr:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown(f'<div style="color:{C["text"]};font-size:15px;font-weight:600;margin-bottom:14px;">Revenue by Region (Top 6)</div>', unsafe_allow_html=True)
        regions = rev_sum[ly].get("revenue_by_region", {}) or revenue_data["revenue"].get("revenue_by_region", {}).get(ly, {})
        if regions:
            top = sorted(regions.items(), key=lambda x: x[1], reverse=True)[:6]
            fig = go.Figure(go.Bar(x=[r[0].replace("_"," ").title() for r in top], y=[r[1] for r in top], marker_color=C["primary"]))
            fig.update_layout(height=310, **chart_cfg())
            fig.update_xaxes(tickangle=-45)
            st.plotly_chart(fig, use_container_width=True, key="rev_region")
        st.markdown('</div>', unsafe_allow_html=True)

    with st.expander("📋 Revenue Detail Table"):
        df_d = df[["quarter","fuel_sales","lubricants","convenience_store","fleet_services","other_income","total_revenue"]].copy()
        for c in df_d.columns[1:]: df_d[c] = df_d[c].apply(format_ghs)
        st.dataframe(df_d, use_container_width=True, hide_index=True)

# TAB 3: EXPENSES
with tab3:
    st.markdown('<div class="section-title">Expense Management</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Track and analyze cost structure and spending patterns</div>', unsafe_allow_html=True)
    sel = [y for y in years if str(y) in exp_sum]
    ly = str(max(sel)) if sel else latest_year
    le = exp_sum[ly]

    cols = st.columns(4)
    with cols[0]: kpi_card("💸", "Total Expenses", format_ghs(le["total_expenses"]), f"{safe_div(le['total_expenses'], rev_sum[ly]['total_revenue'])*100:.1f}% of Revenue", "negative")
    with cols[1]: kpi_card("🏭", "COGS", format_ghs(le["cost_of_goods_sold"]), f"{le['cogs_percentage']:.1f}%", "positive")
    with cols[2]: kpi_card("👥", "Employee Costs", format_ghs(le["employee_costs"]), f"{safe_div(le['employee_costs'], le['total_expenses'])*100:.1f}% of OpEx", "negative")
    with cols[3]: kpi_card("📦", "OPEX", format_ghs(le["total_expenses"]-le["cost_of_goods_sold"]), f"{le['opex_percentage']:.1f}%", "positive")

    st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)
    cl, cr = st.columns(2)

    with cl:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        cats = ["cost_of_goods_sold","employee_costs","transport_logistics","marketing_advertising","maintenance_repairs","utilities","depreciation","other_expenses"]
        labels = ["COGS","Employee","Transport","Marketing","Maintenance","Utilities","Depreciation","Other"]
        fig = px.pie(values=[le[k] for k in cats], names=labels, hole=0.5, color_discrete_sequence=px.colors.qualitative.Set2)
        fig.update_traces(textposition="inside", textinfo="percent+label", textfont=dict(color=C["text"]))
        fig.update_layout(title=dict(text=f"Expense Breakdown ({ly})", font=dict(size=15, color=C["text"])), height=390, showlegend=False, **chart_cfg())
        st.plotly_chart(fig, use_container_width=True, key="exp_pie")
        st.markdown('</div>', unsafe_allow_html=True)

    with cr:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        df = pd.DataFrame(expenses_data["expenses"]["quarterly"])
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df["quarter"], y=df["total_expenses"], name="Total", mode="lines+markers", line=dict(color=C["danger"], width=3), fill="tozeroy", fillcolor=C["danger_d"]))
        fig.add_trace(go.Scatter(x=df["quarter"], y=df["cost_of_goods_sold"], name="COGS", mode="lines+markers", line=dict(color=C["secondary"], width=2)))
        fig.add_trace(go.Scatter(x=df["quarter"], y=df["employee_costs"], name="Employees", mode="lines+markers", line=dict(color=C["accent"], width=2)))
        fig.update_layout(title=dict(text="Expense Trends", font=dict(size=15, color=C["text"])), height=390, **chart_cfg())
        st.plotly_chart(fig, use_container_width=True, key="exp_trend")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div style="height:14px;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown(f'<div style="color:{C["text"]};font-size:15px;font-weight:600;margin-bottom:14px;">Expense Efficiency Metrics</div>', unsafe_allow_html=True)
    ca, cb, cc = st.columns(3)
    with ca:
        progress_bar("COGS Efficiency", 100-le["cogs_percentage"], 100, C["primary"])
        progress_bar("OpEx Control", 100-le["opex_percentage"], 100, C["secondary"])
    with cb:
        progress_bar("Marketing ROI", safe_div(rev_sum[ly]["total_revenue"], le["marketing_advertising"])*10, 100, C["accent"])
        progress_bar("Admin Efficiency", safe_div(le["administrative"], le["total_expenses"])*100, 20, C["purple"])
    with cc:
        profit = rev_sum[ly]["total_revenue"] - le["total_expenses"]
        metric_row("Interest Coverage", f"{safe_div(profit, le['interest_expense']):.1f}x", "Healthy", "success")
        metric_row("Tax Rate", f"{safe_div(le['taxes_levies'], profit)*100:.1f}%", "Normal", "info")
    st.markdown('</div>', unsafe_allow_html=True)

# TAB 4: PROFITABILITY
with tab4:
    st.markdown('<div class="section-title">Profitability Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Margins, returns, and profitability metrics across periods</div>', unsafe_allow_html=True)
    df_kpi = pd.DataFrame(ops_data["operational_metrics"]["kpis"]["quarterly"])
    df_kpi["year"] = df_kpi["quarter"].str.extract(r"(\d{4})").astype(int)
    sel = [y for y in years if str(y) in rev_sum]
    ly = str(max(sel)) if sel else latest_year
    lk = df_kpi[df_kpi["year"] == int(ly)].iloc[-1]

    cols = st.columns(4)
    with cols[0]: kpi_card("📊", "Gross Margin", f"{lk['gross_profit_margin']:.1f}%", "+3.3 pts from 2023", "positive")
    with cols[1]: kpi_card("💰", "Net Margin", f"{lk['net_profit_margin']:.1f}%", "+2.4 pts from 2023", "positive")
    with cols[2]: kpi_card("📈", "EBITDA Margin", f"{lk['ebitda_margin']:.1f}%", "+2.7 pts from 2023", "positive")
    with cols[3]: kpi_card("🏦", "ROE", f"{lk['return_on_equity']:.1f}%", "+4.4 pts from 2023", "positive")

    st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_kpi["quarter"], y=df_kpi["gross_profit_margin"], name="Gross Margin", mode="lines+markers", line=dict(color=C["primary"], width=3)))
    fig.add_trace(go.Scatter(x=df_kpi["quarter"], y=df_kpi["ebitda_margin"], name="EBITDA Margin", mode="lines+markers", line=dict(color=C["secondary"], width=3)))
    fig.add_trace(go.Scatter(x=df_kpi["quarter"], y=df_kpi["net_profit_margin"], name="Net Margin", mode="lines+markers", line=dict(color=C["accent"], width=3)))
    fig.update_layout(title=dict(text="Margin Expansion Over Time", font=dict(size=17, color=C["text"])), height=370, **chart_cfg())
    st.plotly_chart(fig, use_container_width=True, key="prof_margins")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div style="height:14px;"></div>', unsafe_allow_html=True)
    cl, cr = st.columns(2)

    with cl:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        yrs = [y for y in ["2023","2024","2025"] if y in rev_sum and int(y) in years]
        fig = go.Figure()
        fig.add_trace(go.Bar(name="Gross Profit", x=yrs, y=[rev_sum[y]["total_revenue"]-exp_sum[y]["cost_of_goods_sold"] for y in yrs], marker_color=C["primary"]))
        fig.add_trace(go.Bar(name="Operating Profit", x=yrs, y=[rev_sum[y]["total_revenue"]-exp_sum[y]["total_expenses"]+exp_sum[y]["interest_expense"]+exp_sum[y]["depreciation"] for y in yrs], marker_color=C["secondary"]))
        fig.add_trace(go.Bar(name="Net Profit", x=yrs, y=[rev_sum[y]["total_revenue"]-exp_sum[y]["total_expenses"] for y in yrs], marker_color=C["accent"]))
        fig.update_layout(title=dict(text="Annual Profit Layers", font=dict(size=15, color=C["text"])), barmode="group", height=310, **chart_cfg())
        st.plotly_chart(fig, use_container_width=True, key="prof_bar")
        st.markdown('</div>', unsafe_allow_html=True)

    with cr:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_kpi["quarter"], y=df_kpi["return_on_equity"], name="ROE", mode="lines+markers", line=dict(color=C["purple"], width=3)))
        fig.add_trace(go.Scatter(x=df_kpi["quarter"], y=df_kpi["return_on_assets"], name="ROA", mode="lines+markers", line=dict(color=C["danger"], width=3)))
        fig.add_shape(type="line", x0=0, x1=11, y0=15, y1=15, line=dict(color=C["muted"], width=1, dash="dash"))
        fig.add_annotation(x=11, y=15, text="Target", showarrow=False, font=dict(color=C["muted"], size=11))
        fig.update_layout(title=dict(text="Returns vs Target", font=dict(size=15, color=C["text"])), height=310, **chart_cfg())
        st.plotly_chart(fig, use_container_width=True, key="prof_ret")
        st.markdown('</div>', unsafe_allow_html=True)

# TAB 5: FUEL SALES
with tab5:
    st.markdown('<div class="section-title">Fuel Sales Volume</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Track liters sold, fuel mix, and LPG performance</div>', unsafe_allow_html=True)
    fs = fuel_data["fuel_sales_volume"]["annual_summary"]
    sel = [y for y in years if str(y) in fs]
    ly = str(max(sel)) if sel else latest_year

    cols = st.columns(4)
    with cols[0]: kpi_card("🛢️", "Total Volume", f"{fs[ly]['total_liters']/1e9:.2f}B Liters", "+19.1% YoY", "positive")
    with cols[1]: kpi_card("📊", "Avg Daily", f"{fs[ly]['avg_daily_liters']/1e6:.2f}M L", "Growing", "positive")
    with cols[2]: kpi_card("🔥", "LPG Sales", f"{fs[ly]['lpg_tons']:,} Tons", "+21.6% YoY", "positive")
    with cols[3]: kpi_card("⛽", "PMS Share", f"{fuel_data['fuel_sales_volume']['fuel_type_mix'][ly]['pms_percent']:.1f}%", "Dominant", "positive")

    st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    df = pd.DataFrame(fuel_data["fuel_sales_volume"]["monthly"])
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["month"], y=df["pms_liters"], name="PMS", mode="lines+markers", line=dict(color=C["primary"], width=2)))
    fig.add_trace(go.Scatter(x=df["month"], y=df["diesel_liters"], name="Diesel", mode="lines+markers", line=dict(color=C["secondary"], width=2)))
    fig.add_trace(go.Scatter(x=df["month"], y=df["kerosene_liters"], name="Kerosene", mode="lines+markers", line=dict(color=C["accent"], width=2, dash="dash")))
    fig.update_layout(title=dict(text="Monthly Volume Trends", font=dict(size=17, color=C["text"])), height=410, **chart_cfg())
    st.plotly_chart(fig, use_container_width=True, key="fuel_trend")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div style="height:14px;"></div>', unsafe_allow_html=True)
    cl, cr = st.columns(2)

    with cl:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        mix = fuel_data["fuel_sales_volume"]["fuel_type_mix"]
        fig = px.pie(values=[mix[ly]["pms_percent"], mix[ly]["diesel_percent"], mix[ly]["kerosene_percent"]],
                      names=["PMS (Petrol)","Diesel","Kerosene"], hole=0.6,
                      color_discrete_sequence=[C["primary"],C["secondary"],C["accent"]])
        fig.update_traces(textposition="inside", textinfo="percent+label", textfont=dict(color=C["text"]))
        fig.update_layout(title=dict(text=f"Fuel Mix ({ly})", font=dict(size=15, color=C["text"])), height=370, showlegend=False, **chart_cfg())
        st.plotly_chart(fig, use_container_width=True, key="fuel_mix")
        st.markdown('</div>', unsafe_allow_html=True)

    with cr:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig = go.Figure(go.Bar(x=df["month"], y=df["lpg_tons"], marker_color=C["secondary"], name="LPG Tons"))
        fig.update_layout(title=dict(text="LPG Sales Trend", font=dict(size=15, color=C["text"])), height=370, **chart_cfg())
        st.plotly_chart(fig, use_container_width=True, key="fuel_lpg")
        st.markdown('</div>', unsafe_allow_html=True)

# TAB 6: BALANCE SHEET
with tab6:
    st.markdown('<div class="section-title">Balance Sheet</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Assets, liabilities, equity positions and financial health</div>', unsafe_allow_html=True)
    bs = bs_data["balance_sheet"]["annual"]
    ratios = bs_data["balance_sheet"]["key_ratios"]
    sel = [y for y in years if str(y) in bs]
    ly = str(max(sel)) if sel else latest_year

    cols = st.columns(4)
    with cols[0]: kpi_card("🏦", "Total Assets", format_ghs(bs[ly]["assets"]["total_assets"]), f"{safe_div(bs[ly]['assets']['total_assets'], bs.get('2023',{}).get('assets',{}).get('total_assets',1))-1:.1%} since 2023", "positive")
    with cols[1]: kpi_card("💎", "Total Equity", format_ghs(bs[ly]["equity"]["total_equity"]), f"{safe_div(bs[ly]['equity']['total_equity'], bs.get('2023',{}).get('equity',{}).get('total_equity',1))-1:.1%} growth", "positive")
    with cols[2]: kpi_card("💵", "Working Capital", format_ghs(ratios[ly]["working_capital"]), f"+{safe_div(ratios[ly]['working_capital'], ratios.get('2023',{}).get('working_capital',1))-1:.1%}", "positive")
    with cols[3]: kpi_card("📊", "Debt/Equity", f"{ratios[ly]['debt_to_equity']:.2f}", f"-{safe_div(ratios.get('2023',{}).get('debt_to_equity',1)-ratios[ly]['debt_to_equity'], ratios.get('2023',{}).get('debt_to_equity',1))*100:.1f}%", "positive")

    st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    yrs = [y for y in ["2023","2024","2025"] if y in bs and int(y) in years]
    fig = go.Figure()
    fig.add_trace(go.Bar(name="Assets", x=yrs, y=[bs[y]["assets"]["total_assets"] for y in yrs], marker_color=C["primary"]))
    fig.add_trace(go.Bar(name="Liabilities", x=yrs, y=[bs[y]["liabilities"]["total_liabilities"] for y in yrs], marker_color=C["danger"]))
    fig.add_trace(go.Bar(name="Equity", x=yrs, y=[bs[y]["equity"]["total_equity"] for y in yrs], marker_color=C["secondary"]))
    fig.update_layout(title=dict(text="Balance Sheet Evolution", font=dict(size=17, color=C["text"])), barmode="group", height=370, **chart_cfg())
    st.plotly_chart(fig, use_container_width=True, key="bs_chart")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div style="height:14px;"></div>', unsafe_allow_html=True)
    cl, cr = st.columns(2)

    with cl:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig = px.pie(values=[bs[ly]["assets"]["current_assets"]["total_current_assets"], bs[ly]["assets"]["non_current_assets"]["net_ppe"],
                         bs[ly]["assets"]["non_current_assets"]["intangible_assets"], bs[ly]["assets"]["non_current_assets"]["long_term_investments"]],
                      names=["Current Assets","Net PPE","Intangibles","Long-term Investments"], hole=0.5,
                      color_discrete_sequence=px.colors.qualitative.Set2)
        fig.update_traces(textposition="inside", textinfo="percent+label", textfont=dict(color=C["text"]))
        fig.update_layout(title=dict(text=f"Asset Composition ({ly})", font=dict(size=15, color=C["text"])), height=350, showlegend=False, **chart_cfg())
        st.plotly_chart(fig, use_container_width=True, key="bs_asset")
        st.markdown('</div>', unsafe_allow_html=True)

    with cr:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=yrs, y=[ratios[y]["current_ratio"] for y in yrs], name="Current Ratio", mode="lines+markers", line=dict(color=C["primary"], width=3)))
        fig.add_trace(go.Scatter(x=yrs, y=[ratios[y]["quick_ratio"] for y in yrs], name="Quick Ratio", mode="lines+markers", line=dict(color=C["accent"], width=3)))
        fig.add_shape(type="line", x0=0, x1=2, y0=1.5, y1=1.5, line=dict(color=C["muted"], width=1, dash="dash"))
        fig.update_layout(title=dict(text="Liquidity Trends", font=dict(size=15, color=C["text"])), height=350, **chart_cfg())
        st.plotly_chart(fig, use_container_width=True, key="bs_liq")
        st.markdown('</div>', unsafe_allow_html=True)

    with st.expander("📋 Detailed Balance Sheet"):
        bl = bs[ly]
        items = [
            ("Cash & Equivalents", bl["assets"]["current_assets"]["cash_and_equivalents"]),
            ("Accounts Receivable", bl["assets"]["current_assets"]["accounts_receivable"]),
            ("Inventory", bl["assets"]["current_assets"]["inventory"]),
            ("Net PPE", bl["assets"]["non_current_assets"]["net_ppe"]),
            ("Long-term Debt", bl["liabilities"]["non_current_liabilities"]["long_term_debt"])
        ]
        for label, val in items:
            metric_row(label, format_ghs(val))
        st.markdown('</div>', unsafe_allow_html=True)

# TAB 7: CASH FLOW
with tab7:
    st.markdown('<div class="section-title">Cash Flow Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Operating, investing, and financing cash movements</div>', unsafe_allow_html=True)
    cf = cf_data["cash_flow"]["annual_summary"]
    sel = [y for y in years if str(y) in cf]
    ly = str(max(sel)) if sel else latest_year

    cols = st.columns(3)
    with cols[0]: kpi_card("💵", "Operating CF", format_ghs(cf[ly]["net_cash_from_operations"]), f"+{safe_div(cf[ly]['net_cash_from_operations'], cf.get('2023',{}).get('net_cash_from_operations',1))-1:.1%} vs 2023", "positive")
    with cols[1]: kpi_card("📈", "Free Cash Flow", format_ghs(cf[ly]["free_cash_flow"]), f"+{safe_div(cf[ly]['free_cash_flow'], cf.get('2023',{}).get('free_cash_flow',1))-1:.1%} vs 2023", "positive")
    with cols[2]: kpi_card("🏗️", "CapEx", format_ghs(abs(cf[ly]["capex"])), "Investing in Growth", "positive")

    st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    yrs = [y for y in ["2023","2024","2025"] if y in cf and int(y) in years]
    fig = go.Figure()
    fig.add_trace(go.Bar(name="Operating", x=yrs, y=[cf[y]["net_cash_from_operations"] for y in yrs], marker_color=C["primary"]))
    fig.add_trace(go.Bar(name="Investing", x=yrs, y=[cf[y]["net_cash_from_investing"] for y in yrs], marker_color=C["danger"]))
    fig.add_trace(go.Bar(name="Financing", x=yrs, y=[cf[y]["net_cash_from_financing"] for y in yrs], marker_color=C["accent"]))
    fig.update_layout(title=dict(text="Cash Flow Components", font=dict(size=17, color=C["text"])), barmode="group", height=370, **chart_cfg())
    st.plotly_chart(fig, use_container_width=True, key="cf_comp")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div style="height:14px;"></div>', unsafe_allow_html=True)
    cl, cr = st.columns(2)

    with cl:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        df_fcf = pd.DataFrame({k: v["free_cash_flow"] for k, v in cf.items() if int(k) in years}, index=["FCF"]).T
        df_fcf["year"] = df_fcf.index
        fig = go.Figure(go.Scatter(x=df_fcf["year"], y=df_fcf["FCF"], name="Free Cash Flow", mode="lines+markers", line=dict(color=C["secondary"], width=3), fill="tozeroy", fillcolor=C["secondary_d"]))
        fig.update_layout(title=dict(text="Free Cash Flow Growth", font=dict(size=15, color=C["text"])), height=330, **chart_cfg())
        st.plotly_chart(fig, use_container_width=True, key="cf_fcf")
        st.markdown('</div>', unsafe_allow_html=True)

    with cr:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        df_q = pd.DataFrame(cf_data["cash_flow"]["quarterly"])
        fig = go.Figure(go.Bar(x=df_q["quarter"], y=df_q["free_cash_flow"], marker_color=[C["primary"] if v >= 0 else C["danger"] for v in df_q["free_cash_flow"]], name="Quarterly FCF"))
        fig.update_layout(title=dict(text="Quarterly Free Cash Flow", font=dict(size=15, color=C["text"])), height=330, **chart_cfg())
        st.plotly_chart(fig, use_container_width=True, key="cf_qfcf")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div style="height:14px;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown(f'<div style="color:{C["text"]};font-size:15px;font-weight:600;margin-bottom:14px;">Cash Flow Health Check</div>', unsafe_allow_html=True)
    ca, cb, cc = st.columns(3)
    with ca:
        progress_bar("Operating CF Margin", safe_div(cf[ly]["net_cash_from_operations"], rev_sum[ly]["total_revenue"])*100, 20, C["primary"])
        progress_bar("FCF Conversion", safe_div(cf[ly]["free_cash_flow"], cf[ly]["net_cash_from_operations"])*100, 100, C["secondary"])
    with cb:
        metric_row("Dividends Paid", format_ghs(cf[ly]["dividends_paid"]), "Consistent", "info")
        metric_row("Debt Reduction", format_ghs(abs(cf[ly]["net_cash_from_financing"])), "Active", "success")
    with cc:
        metric_row("CapEx / Revenue", f"{safe_div(abs(cf[ly]['capex']), rev_sum[ly]['total_revenue'])*100:.1f}%", "Reinvesting", "info")
        profit = rev_sum[ly]["total_revenue"] - exp_sum[ly]["total_expenses"]
        metric_row("Cash Conversion", f"{safe_div(cf[ly]['net_cash_from_operations'], profit)*100:.1f}%", "Strong", "success")
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
    yrs = [y for y in ["2023","2024","2025"] if y in stations and int(y) in years]

    cols = st.columns(4)
    with cols[0]: kpi_card("⛽", "Total Stations", f"{stations[ly]['total_stations']:,}", f"+{stations[ly]['new_stations_opened']} new", "positive")
    with cols[1]: kpi_card("⏱️", "Uptime", f"{stations[ly]['operational_uptime_percent']:.1f}%", "Excellent", "positive")
    with cols[2]: kpi_card("😊", "Satisfaction", f"{customers[ly]['customer_satisfaction_score']:.1f}/100", "+5.3 pts", "positive")
    with cols[3]: kpi_card("🎯", "NPS Score", str(customers[ly]['nps_score']), "+10 pts", "positive")

    st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)
    cl, cr = st.columns(2)

    with cl:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_trace(go.Bar(name="Company Owned", x=yrs, y=[stations[y]["company_owned"] for y in yrs], marker_color=C["primary"]))
        fig.add_trace(go.Bar(name="Dealer Owned", x=yrs, y=[stations[y]["dealer_owned"] for y in yrs], marker_color=C["secondary"]))
        fig.add_trace(go.Bar(name="Franchise", x=yrs, y=[stations[y]["franchise"] for y in yrs], marker_color=C["accent"]))
        fig.update_layout(title=dict(text="Station Network Growth", font=dict(size=15, color=C["text"])), barmode="stack", height=330, **chart_cfg())
        st.plotly_chart(fig, use_container_width=True, key="ops_stations")
        st.markdown('</div>', unsafe_allow_html=True)

    with cr:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=yrs, y=[employees[y]["total_employees"] for y in yrs], name="Employees", mode="lines+markers", line=dict(color=C["primary"], width=3), fill="tozeroy", fillcolor=C["primary_d"]))
        fig.add_trace(go.Scatter(x=yrs, y=[employees[y]["avg_salary_ghs"] for y in yrs], name="Avg Salary", mode="lines+markers", line=dict(color=C["secondary"], width=2, dash="dash"), yaxis="y2"))
        fig.update_layout(title=dict(text="Workforce Growth & Compensation", font=dict(size=15, color=C["text"])), height=330, **chart_cfg(), yaxis2=dict(overlaying="y", side="right", showgrid=False))
        st.plotly_chart(fig, use_container_width=True, key="ops_emp")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div style="height:14px;"></div>', unsafe_allow_html=True)
    ca, cb, cc = st.columns(3)

    with ca:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig = go.Figure(go.Scatter(x=yrs, y=[customers[y]["loyalty_program_members"] for y in yrs], name="Members", mode="lines+markers", line=dict(color=C["purple"], width=3), fill="tozeroy", fillcolor=C["purple_d"]))
        fig.update_layout(title=dict(text="Loyalty Program Growth", font=dict(size=13, color=C["text"])), height=290, **chart_cfg())
        st.plotly_chart(fig, use_container_width=True, key="ops_loyalty")
        st.markdown('</div>', unsafe_allow_html=True)

    with cb:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig = go.Figure(go.Bar(x=yrs, y=[employees[y]["safety_incidents"] for y in yrs], marker_color=C["danger"], name="Incidents"))
        fig.update_layout(title=dict(text="Safety Incidents", font=dict(size=13, color=C["text"])), height=290, **chart_cfg())
        st.plotly_chart(fig, use_container_width=True, key="ops_safety")
        st.markdown('</div>', unsafe_allow_html=True)

    with cc:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown(f'<div style="color:{C["text"]};font-size:13px;font-weight:600;margin-bottom:14px;">Training & Development</div>', unsafe_allow_html=True)
        progress_bar("Training hrs/emp", employees[ly]["training_hours_per_employee"], 60, C["primary"])
        progress_bar("Turnover (inverse)", 100-employees[ly]["employee_turnover_percent"], 100, C["secondary"])
        metric_row("Fleet Accounts", f"{customers[ly]['active_fleet_accounts']:,}", "+800", "success")
        metric_row("Avg Transaction", f"GHS {customers[ly]['avg_transaction_value_ghs']:,}", "+18%", "positive")
        st.markdown('</div>', unsafe_allow_html=True)

# FOOTER
st.markdown("<div style='height:48px;'></div>", unsafe_allow_html=True)
st.markdown(f"""
<div class="footer">
    Goil Ghana Limited • Financial Dashboard • Data Period: {ALL_YEARS[0] if ALL_YEARS else 2023} - {ALL_YEARS[-1] if ALL_YEARS else 2025}<br>
    <span style="color:{C["muted"]};font-size:12px;">All figures in Ghana Cedis (GHS) • Mock data for demonstration purposes</span>
</div>""", unsafe_allow_html=True)
