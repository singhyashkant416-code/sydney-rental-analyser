import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from data import get_sydney_data

st.set_page_config(
    page_title="PropLens — Sydney Property Intelligence",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=DM+Serif+Display&display=swap');

/* Base */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Hide default Streamlit elements */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 0rem; padding-bottom: 2rem; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: #0f1923;
    border-right: 1px solid #1e2d3d;
}
[data-testid="stSidebar"] * { color: #94a3b8 !important; }
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stSlider label { 
    color: #64748b !important; 
    font-size: 11px !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 500;
}
[data-testid="stSidebar"] h1, 
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: #e2e8f0 !important; }

/* Logo area */
.proplens-logo {
    padding: 2rem 1rem 1.5rem;
    border-bottom: 1px solid #1e2d3d;
    margin-bottom: 1.5rem;
}
.proplens-logo .brand {
    font-family: 'DM Serif Display', serif;
    font-size: 22px;
    color: #f1f5f9 !important;
    letter-spacing: -0.02em;
}
.proplens-logo .brand span { color: #3b82f6 !important; }
.proplens-logo .tagline {
    font-size: 11px;
    color: #475569 !important;
    margin-top: 3px;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

/* Top header bar */
.top-header {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    border-bottom: 1px solid #1e2d3d;
    padding: 1.25rem 2rem;
    margin: -1rem -1rem 2rem -1rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.top-header .page-title {
    font-size: 13px;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-weight: 500;
}
.top-header .data-badge {
    background: #0f2744;
    border: 1px solid #1e3a5f;
    border-radius: 6px;
    padding: 5px 12px;
    font-size: 11px;
    color: #3b82f6;
    font-weight: 500;
}

/* KPI Cards */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin-bottom: 2rem;
}
.kpi-card {
    background: #0f1923;
    border: 1px solid #1e2d3d;
    border-radius: 10px;
    padding: 1.25rem 1.5rem;
    position: relative;
    overflow: hidden;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: #3b82f6;
}
.kpi-card.green::before { background: #10b981; }
.kpi-card.amber::before { background: #f59e0b; }
.kpi-card.purple::before { background: #8b5cf6; }
.kpi-label {
    font-size: 11px;
    color: #475569;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 500;
    margin-bottom: 8px;
}
.kpi-value {
    font-size: 26px;
    font-weight: 700;
    color: #f1f5f9;
    letter-spacing: -0.02em;
    line-height: 1;
}
.kpi-sub {
    font-size: 11px;
    color: #475569;
    margin-top: 6px;
}

/* Section headers */
.section-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 1rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid #1e2d3d;
}
.section-header .section-title {
    font-size: 13px;
    font-weight: 600;
    color: #e2e8f0;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}
.section-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #3b82f6;
}

/* Data source footer */
.data-footer {
    background: #0a1628;
    border: 1px solid #1e2d3d;
    border-radius: 8px;
    padding: 1rem 1.5rem;
    margin-top: 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.data-footer .source-label {
    font-size: 11px;
    color: #334155;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
.data-footer .source-value {
    font-size: 12px;
    color: #475569;
    margin-top: 3px;
}

/* Yield badges */
.badge {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 11px;
    font-weight: 600;
}
.badge-high { background: #052e16; color: #34d399; }
.badge-good { background: #0c1a2e; color: #60a5fa; }
.badge-med { background: #1c1003; color: #fbbf24; }
.badge-low { background: #1a0a0a; color: #f87171; }

/* Search box */
.stTextInput input {
    background: #0f1923 !important;
    border: 1px solid #1e2d3d !important;
    border-radius: 8px !important;
    color: #e2e8f0 !important;
    font-size: 13px !important;
}

/* Divider */
.prop-divider {
    border: none;
    border-top: 1px solid #1e2d3d;
    margin: 2rem 0;
}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="proplens-logo">
        <div class="brand">Prop<span>Lens</span></div>
        <div class="tagline">Sydney Property Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### Filters")

    df_raw = get_sydney_data()

    regions = ["All Regions"] + sorted(df_raw["region"].unique().tolist())
    selected_region = st.selectbox("Region", regions)

    min_yield, max_yield = st.slider(
        "Gross Yield Range (%)",
        min_value=float(df_raw["gross_yield_pct"].min()),
        max_value=float(df_raw["gross_yield_pct"].max()),
        value=(float(df_raw["gross_yield_pct"].min()), float(df_raw["gross_yield_pct"].max())),
        step=0.1
    )

    max_price = st.slider(
        "Max Property Price ($)",
        min_value=int(df_raw["median_price"].min()),
        max_value=int(df_raw["median_price"].max()),
        value=int(df_raw["median_price"].max()),
        step=50000,
        format="$%d"
    )

    search = st.text_input("Search suburb", placeholder="e.g. Parramatta")

    st.markdown("---")
    st.markdown("""
    <div style="font-size:11px; color:#334155; line-height:1.7;">
    <strong style="color:#475569;">Data Sources</strong><br>
    Rental: NSW Fair Trading<br>
    Mar 2026 Quarter<br><br>
    Sales: NSW Valuer General<br>
    Dec 2025 Quarter
    </div>
    """, unsafe_allow_html=True)

# ── Filter data ───────────────────────────────────────────────────────────────
df = df_raw.copy()
if selected_region != "All Regions":
    df = df[df["region"] == selected_region]
df = df[
    (df["gross_yield_pct"] >= min_yield) &
    (df["gross_yield_pct"] <= max_yield) &
    (df["median_price"] <= max_price)
]
if search:
    df = df[df["suburb"].str.contains(search, case=False, na=False)]

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="top-header">
    <div class="page-title">Market Overview — Greater Sydney</div>
    <div class="data-badge">Live NSW Gov Data · Q1 2026</div>
</div>
""", unsafe_allow_html=True)

# ── KPI Cards ─────────────────────────────────────────────────────────────────
avg_yield = df["gross_yield_pct"].mean()
avg_price = df["median_price"].mean()
avg_rent = df["median_weekly_rent"].mean()
suburb_count = len(df)

st.markdown(f"""
<div class="kpi-grid">
    <div class="kpi-card">
        <div class="kpi-label">Suburbs Analysed</div>
        <div class="kpi-value">{suburb_count}</div>
        <div class="kpi-sub">Greater Sydney coverage</div>
    </div>
    <div class="kpi-card green">
        <div class="kpi-label">Avg Gross Yield</div>
        <div class="kpi-value">{avg_yield:.2f}%</div>
        <div class="kpi-sub">All dwelling types</div>
    </div>
    <div class="kpi-card amber">
        <div class="kpi-label">Avg Median Price</div>
        <div class="kpi-value">${avg_price:,.0f}</div>
        <div class="kpi-sub">Dec 2025 quarter</div>
    </div>
    <div class="kpi-card purple">
        <div class="kpi-label">Avg Weekly Rent</div>
        <div class="kpi-value">${avg_rent:,.0f}</div>
        <div class="kpi-sub">Mar 2026 quarter</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Chart theme ───────────────────────────────────────────────────────────────
CHART_BG = "#0a1628"
CHART_PAPER = "#0a1628"
GRID_COLOR = "#1e2d3d"
TEXT_COLOR = "#64748b"
FONT = "Inter"

def style_chart(fig, height=380):
    fig.update_layout(
        height=height,
        paper_bgcolor=CHART_PAPER,
        plot_bgcolor=CHART_BG,
        font=dict(family=FONT, color=TEXT_COLOR, size=11),
        margin=dict(l=10, r=10, t=30, b=10),
        legend=dict(
            bgcolor="#0f1923",
            bordercolor="#1e2d3d",
            borderwidth=1,
            font=dict(size=10, color="#64748b")
        ),
        xaxis=dict(gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR),
        yaxis=dict(gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR),
    )
    return fig

# ── Row 1: Top yields + Scatter ───────────────────────────────────────────────
st.markdown("""
<div class="section-header">
    <div class="section-dot"></div>
    <div class="section-title">Yield Analysis</div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    top10 = df.nlargest(10, "gross_yield_pct")
    fig1 = px.bar(
        top10,
        x="gross_yield_pct",
        y="suburb",
        orientation="h",
        color="gross_yield_pct",
        color_continuous_scale=[[0, "#1d4ed8"], [0.5, "#3b82f6"], [1, "#34d399"]],
        text="gross_yield_pct"
    )
    fig1.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside",
        textfont=dict(size=10, color="#94a3b8"),
        marker_line_width=0
    )
    fig1.update_layout(
        title=dict(text="Top 10 suburbs by gross yield", font=dict(size=12, color="#94a3b8"), x=0),
        coloraxis_showscale=False,
        yaxis=dict(tickfont=dict(size=10, color="#64748b"), categoryorder="total ascending"),
        xaxis=dict(ticksuffix="%", tickfont=dict(size=10))
    )
    style_chart(fig1)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.scatter(
        df,
        x="median_price",
        y="gross_yield_pct",
        color="region",
        hover_name="suburb",
        size="median_weekly_rent",
        size_max=18,
        color_discrete_sequence=px.colors.qualitative.Set2,
        labels={
            "median_price": "Median Sale Price ($)",
            "gross_yield_pct": "Gross Yield (%)",
            "region": "Region"
        }
    )
    fig2.update_traces(marker=dict(line=dict(width=0)))
    fig2.update_layout(
        title=dict(text="Price vs yield — bubble size = weekly rent", font=dict(size=12, color="#94a3b8"), x=0),
        xaxis=dict(tickprefix="$", tickformat=","),
        yaxis=dict(ticksuffix="%")
    )
    style_chart(fig2)
    st.plotly_chart(fig2, use_container_width=True)

# ── Row 2: Investment score + Region box ─────────────────────────────────────
st.markdown('<hr class="prop-divider">', unsafe_allow_html=True)
st.markdown("""
<div class="section-header">
    <div class="section-dot" style="background:#10b981"></div>
    <div class="section-title">Investment Score</div>
</div>
""", unsafe_allow_html=True)

col3, col4 = st.columns(2)

with col3:
    top15 = df.nlargest(15, "investment_score")
    fig3 = px.bar(
        top15,
        x="suburb",
        y="investment_score",
        color="region",
        text="investment_score",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig3.update_traces(
        texttemplate="%{text:.1f}",
        textposition="outside",
        textfont=dict(size=9, color="#94a3b8"),
        marker_line_width=0
    )
    fig3.update_layout(
        title=dict(text="Top 15 suburbs — investment score (yield 60% + affordability 40%)", font=dict(size=12, color="#94a3b8"), x=0),
        xaxis=dict(tickangle=-35, tickfont=dict(size=9)),
        showlegend=False
    )
    style_chart(fig3)
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    fig4 = px.box(
        df,
        x="region",
        y="gross_yield_pct",
        color="region",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig4.update_layout(
        title=dict(text="Yield distribution by region", font=dict(size=12, color="#94a3b8"), x=0),
        xaxis=dict(tickangle=-25, tickfont=dict(size=9)),
        yaxis=dict(ticksuffix="%"),
        showlegend=False
    )
    style_chart(fig4)
    st.plotly_chart(fig4, use_container_width=True)

# ── Data table ────────────────────────────────────────────────────────────────
st.markdown('<hr class="prop-divider">', unsafe_allow_html=True)
st.markdown("""
<div class="section-header">
    <div class="section-dot" style="background:#8b5cf6"></div>
    <div class="section-title">Suburb Data</div>
</div>
""", unsafe_allow_html=True)

display_df = df[[
    "postcode", "suburb", "region", "median_price",
    "median_weekly_rent", "gross_yield_pct", "yield_category", "investment_score"
]].sort_values("gross_yield_pct", ascending=False).reset_index(drop=True)

display_df.columns = [
    "Postcode", "Suburb", "Region", "Median Price",
    "Weekly Rent", "Gross Yield", "Category", "Score"
]
display_df["Median Price"] = display_df["Median Price"].apply(lambda x: f"${x:,.0f}")
display_df["Weekly Rent"] = display_df["Weekly Rent"].apply(lambda x: f"${x:,.0f}")
display_df["Gross Yield"] = display_df["Gross Yield"].apply(lambda x: f"{x:.2f}%")

st.dataframe(
    display_df,
    use_container_width=True,
    height=420,
    hide_index=True
)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="data-footer">
    <div>
        <div class="source-label">Data Sources</div>
        <div class="source-value">
            Rental data — NSW Fair Trading Rental Bond Board (Mar 2026 Quarter) &nbsp;·&nbsp;
            Sale prices — NSW Valuer General (Dec 2025 Quarter)
        </div>
    </div>
    <div style="text-align:right;">
        <div class="source-label">Built by</div>
        <div class="source-value" style="color:#3b82f6;">PropLens Analytics</div>
    </div>
</div>
""", unsafe_allow_html=True)
