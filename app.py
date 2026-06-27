import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from data import get_sydney_data

st.set_page_config(
    page_title="PropLens — Sydney Property Intelligence",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═════════════════════════════════════════════════════════════════════════════
# EDITORIAL DAYLIGHT THEME — companion to landing page
# Background: warm paper #f5f0e6
# Accents: brass gold (signature), forest (positive), terracotta (price), ink
# ═════════════════════════════════════════════════════════════════════════════

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,300;9..144,400;9..144,500;9..144,600&family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

/* ──── Base — warm paper background ──── */
.stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stMain"] {
    background: #f5f0e6 !important;
}

html, body, [class*="css"], .stMarkdown, .stMarkdown p {
    font-family: 'Inter', -apple-system, sans-serif !important;
    color: #2a2520 !important;
    font-weight: 400 !important;
}

#MainMenu, footer, header[data-testid="stHeader"] { 
    visibility: hidden !important; 
    height: 0 !important;
}

.block-container { 
    padding-top: 1rem !important; 
    padding-bottom: 4rem !important;
    max-width: 1400px !important;
}

::selection { background: #c8a96a; color: #fff; }

/* ──── Sidebar — sister cream tone ──── */
[data-testid="stSidebar"] {
    background: #ebe4d6 !important;
    border-right: 1px solid rgba(138, 111, 63, 0.18) !important;
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 0 !important;
}

[data-testid="stSidebar"] * { 
    color: #2a2520 !important;
    font-weight: 400 !important;
}

[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] .stTextInput label { 
    color: #8a6f3f !important; 
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 10px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.2em !important;
    font-weight: 500 !important;
    margin-bottom: 8px !important;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] h4 { 
    color: #1c1812 !important;
    font-family: 'Fraunces', serif !important;
    font-weight: 400 !important;
}

[data-testid="stSidebar"] [data-baseweb="select"] > div,
[data-testid="stSidebar"] input[type="text"] {
    background: #f5f0e6 !important;
    border: 1px solid rgba(138, 111, 63, 0.25) !important;
    border-radius: 2px !important;
    color: #2a2520 !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 400 !important;
}

[data-testid="stSidebar"] [data-baseweb="select"] > div:hover,
[data-testid="stSidebar"] input[type="text"]:focus {
    border-color: #c8a96a !important;
}

[data-testid="stSidebar"] [data-baseweb="slider"] [role="slider"] {
    background: #c8a96a !important;
    border: 2px solid #8a6f3f !important;
}

[data-testid="stSidebar"] [data-baseweb="slider"] > div > div > div {
    background: #c8a96a !important;
}

/* ──── Brand block ──── */
.brand-block {
    padding: 2rem 0.5rem 2rem;
    border-bottom: 1px solid rgba(138, 111, 63, 0.18);
    margin: -1rem -1rem 2rem -1rem;
    padding-left: 1.75rem;
}

.brand-mark {
    display: flex;
    align-items: baseline;
    gap: 8px;
    margin-bottom: 8px;
}

.brand-diamond {
    color: #8a6f3f;
    font-size: 13px;
}

.brand-name {
    font-family: 'Fraunces', serif !important;
    font-size: 28px !important;
    font-weight: 400 !important;
    color: #1c1812 !important;
    letter-spacing: -0.015em;
    line-height: 1;
}

.brand-name em {
    font-style: italic;
    color: #8a6f3f !important;
    font-weight: 400;
}

.brand-tagline {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 10px !important;
    color: #8a6f3f !important;
    letter-spacing: 0.2em;
    text-transform: uppercase;
}

/* ──── Top bar ──── */
.top-bar {
    background: #fdfaf3;
    border: 1px solid rgba(138, 111, 63, 0.18);
    border-radius: 4px;
    padding: 1.75rem 2.25rem;
    margin-bottom: 2rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: relative;
    overflow: hidden;
    box-shadow: 0 1px 3px rgba(28, 24, 18, 0.04);
}

.top-bar::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    background: linear-gradient(180deg, #c8a96a 0%, #8a6f3f 100%);
}

.top-bar .eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    color: #8a6f3f;
    text-transform: uppercase;
    letter-spacing: 0.25em;
    margin-bottom: 8px;
    font-weight: 500;
}

.top-bar .title {
    font-family: 'Fraunces', serif;
    font-size: 32px;
    font-weight: 400;
    color: #1c1812;
    letter-spacing: -0.025em;
    line-height: 1.1;
}

.top-bar .title em {
    font-style: italic;
    color: #8a6f3f;
    font-weight: 400;
}

.live-pill {
    background: rgba(58, 109, 68, 0.08);
    border: 1px solid rgba(58, 109, 68, 0.25);
    border-radius: 999px;
    padding: 8px 16px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    color: #3a6d44;
    font-weight: 500;
    letter-spacing: 0.15em;
    display: flex;
    align-items: center;
    gap: 10px;
    text-transform: uppercase;
}

.live-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #4a8a55;
    box-shadow: 0 0 8px rgba(74, 138, 85, 0.5);
    animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
}

/* ──── KPI Cards — each with its own role colour ──── */
.kpi-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin-bottom: 3rem;
}

.kpi {
    background: #fdfaf3;
    border: 1px solid rgba(138, 111, 63, 0.18);
    border-radius: 4px;
    padding: 1.5rem 1.5rem 1.5rem;
    position: relative;
    transition: all 0.3s ease;
    box-shadow: 0 1px 3px rgba(28, 24, 18, 0.04);
    overflow: hidden;
}

.kpi::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 2px;
}

.kpi.k-gold::before { background: #c8a96a; }
.kpi.k-forest::before { background: #4a8a55; }
.kpi.k-terra::before { background: #a85d3a; }
.kpi.k-slate::before { background: #5a6b7a; }

.kpi:hover {
    border-color: rgba(138, 111, 63, 0.35);
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(28, 24, 18, 0.08);
}

.kpi-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    color: #8a6f3f;
    text-transform: uppercase;
    letter-spacing: 0.2em;
    font-weight: 500;
    margin-bottom: 1.25rem;
}

.kpi.k-forest .kpi-label { color: #3a6d44; }
.kpi.k-terra .kpi-label { color: #a85d3a; }
.kpi.k-slate .kpi-label { color: #5a6b7a; }

.kpi-value {
    font-family: 'Fraunces', serif;
    font-size: 42px;
    font-weight: 400;
    color: #1c1812;
    letter-spacing: -0.03em;
    line-height: 1;
    margin-bottom: 0.5rem;
}

.kpi-value em {
    color: #8a6f3f;
    font-style: italic;
    font-weight: 400;
}

.kpi.k-forest .kpi-value em { color: #3a6d44; }
.kpi.k-terra .kpi-value em { color: #a85d3a; }

.kpi-value .unit {
    color: #8a7d68;
    font-size: 22px;
    margin-left: 2px;
    font-style: normal;
}

.kpi-sub {
    font-family: 'Fraunces', serif;
    font-style: italic;
    font-size: 12px;
    color: #6b5d4a;
    font-weight: 400;
}

/* ──── Section headers ──── */
.section {
    display: flex;
    align-items: baseline;
    gap: 1.5rem;
    margin: 3rem 0 1.5rem;
}

.section-num {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    color: #8a6f3f;
    font-weight: 500;
    letter-spacing: 0.2em;
}

.section-line {
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, rgba(138, 111, 63, 0.3) 0%, transparent 100%);
}

.section-title {
    font-family: 'Fraunces', serif;
    font-size: 24px;
    color: #1c1812;
    font-weight: 400;
    letter-spacing: -0.015em;
}

.section-title em {
    font-style: italic;
    color: #8a6f3f;
    font-weight: 400;
}

/* ──── Footer ──── */
.proplens-footer {
    background: #fdfaf3;
    border: 1px solid rgba(138, 111, 63, 0.18);
    border-radius: 4px;
    padding: 2rem 2.25rem;
    margin-top: 3rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 1px 3px rgba(28, 24, 18, 0.04);
}

.proplens-footer .label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    color: #8a6f3f;
    text-transform: uppercase;
    letter-spacing: 0.2em;
    margin-bottom: 6px;
}

.proplens-footer .value {
    font-family: 'Fraunces', serif;
    font-style: italic;
    font-size: 13px;
    color: #6b5d4a;
    font-weight: 400;
}

.proplens-footer .brand-foot {
    font-family: 'Fraunces', serif;
    font-size: 16px;
    color: #1c1812;
    font-weight: 400;
}

.proplens-footer .brand-foot em {
    font-style: italic;
    color: #8a6f3f;
}

/* ──── Dataframe ──── */
[data-testid="stDataFrame"] {
    background: #fdfaf3 !important;
    border: 1px solid rgba(138, 111, 63, 0.18) !important;
    border-radius: 4px !important;
    padding: 0.5rem !important;
    box-shadow: 0 1px 3px rgba(28, 24, 18, 0.04);
}

[data-testid="stDataFrame"] * {
    color: #2a2520 !important;
    background: transparent !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 400 !important;
}

[data-testid="stMetric"] { display: none; }

/* Scrollbar */
::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-track { background: #ebe4d6; }
::-webkit-scrollbar-thumb { background: #c8a96a; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #8a6f3f; }

/* Sidebar info box */
.sidebar-data-box {
    margin-top: 2rem;
    padding: 1.25rem;
    background: #f5f0e6;
    border: 1px solid rgba(138, 111, 63, 0.18);
    border-left: 2px solid #c8a96a;
    border-radius: 2px;
}

.sidebar-data-box .label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 9px;
    color: #8a6f3f;
    text-transform: uppercase;
    letter-spacing: 0.25em;
    margin-bottom: 12px;
}

.sidebar-data-box .source {
    margin-bottom: 12px;
}

.sidebar-data-box .source:last-child { margin-bottom: 0; }

.sidebar-data-box .source-name {
    font-family: 'Fraunces', serif;
    font-size: 13px;
    color: #1c1812;
    font-weight: 500;
    margin-bottom: 2px;
}

.sidebar-data-box .source-meta {
    font-family: 'Fraunces', serif;
    font-style: italic;
    font-size: 11px;
    color: #8a6f3f;
    font-weight: 400;
}
</style>
""", unsafe_allow_html=True)

# ──────────────────────── Sidebar ────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="brand-block">
        <div class="brand-mark">
            <span class="brand-diamond">◆</span>
            <span class="brand-name">Prop<em>Lens</em></span>
        </div>
        <div class="brand-tagline">Sydney · Q1 2026</div>
    </div>
    """, unsafe_allow_html=True)

    df_raw = get_sydney_data()

    regions = ["All Regions"] + sorted(df_raw["region"].unique().tolist())
    selected_region = st.selectbox("Region", regions)

    min_yield, max_yield = st.slider(
        "Gross Yield",
        min_value=float(df_raw["gross_yield_pct"].min()),
        max_value=float(df_raw["gross_yield_pct"].max()),
        value=(float(df_raw["gross_yield_pct"].min()), float(df_raw["gross_yield_pct"].max())),
        step=0.1,
        format="%.2f%%"
    )

    max_price = st.slider(
        "Max Price",
        min_value=int(df_raw["median_price"].min()),
        max_value=int(df_raw["median_price"].max()),
        value=int(df_raw["median_price"].max()),
        step=50000,
        format="$%d"
    )

    search = st.text_input("Search Suburb", placeholder="e.g. Parramatta")

    st.markdown("""
    <div class="sidebar-data-box">
        <div class="label">— Data Sources</div>
        <div class="source">
            <div class="source-name">NSW Fair Trading</div>
            <div class="source-meta">Rental · Mar 2026 Q</div>
        </div>
        <div class="source">
            <div class="source-name">NSW Valuer General</div>
            <div class="source-meta">Sales · Dec 2025 Q</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ──────────────────────── Apply filters ────────────────────────
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

# ──────────────────────── Top bar ────────────────────────
region_label = selected_region if selected_region != "All Regions" else "Greater Sydney"

st.markdown(f"""
<div class="top-bar">
    <div>
        <div class="eyebrow">— Market Intelligence · Q1 2026</div>
        <div class="title">{region_label} <em>property data</em></div>
    </div>
    <div class="live-pill">
        <span class="live-dot"></span>
        Live · NSW Gov
    </div>
</div>
""", unsafe_allow_html=True)

# ──────────────────────── KPIs ────────────────────────
if len(df) > 0:
    avg_yield = df["gross_yield_pct"].mean()
    avg_price = df["median_price"].mean()
    avg_rent = df["median_weekly_rent"].mean()
    suburb_count = len(df)
else:
    avg_yield = avg_price = avg_rent = suburb_count = 0

st.markdown(f"""
<div class="kpi-row">
    <div class="kpi k-slate">
        <div class="kpi-label">— Suburbs</div>
        <div class="kpi-value">{suburb_count}</div>
        <div class="kpi-sub">analysed in selection</div>
    </div>
    <div class="kpi k-forest">
        <div class="kpi-label">— Gross Yield</div>
        <div class="kpi-value"><em>{avg_yield:.2f}</em><span class="unit">%</span></div>
        <div class="kpi-sub">average across selection</div>
    </div>
    <div class="kpi k-terra">
        <div class="kpi-label">— Median Price</div>
        <div class="kpi-value"><span class="unit">$</span><em>{avg_price/1000:,.0f}</em><span class="unit">k</span></div>
        <div class="kpi-sub">Dec 2025 quarterly median</div>
    </div>
    <div class="kpi k-gold">
        <div class="kpi-label">— Weekly Rent</div>
        <div class="kpi-value"><span class="unit">$</span><em>{avg_rent:,.0f}</em></div>
        <div class="kpi-sub">Mar 2026 quarterly median</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ──────────────────────── Chart styling — daylight theme ────────────────────────
INK = "#1c1812"
INK_SOFT = "#6b5d4a"
PAPER = "#fdfaf3"
GRID = "rgba(138, 111, 63, 0.12)"
GOLD = "#c8a96a"
GOLD_DEEP = "#8a6f3f"
FOREST = "#4a8a55"
TERRA = "#a85d3a"
SLATE = "#5a6b7a"

def style_chart(fig, title=None, height=420):
    fig.update_layout(
        height=height,
        paper_bgcolor=PAPER,
        plot_bgcolor=PAPER,
        font=dict(family="Inter, sans-serif", color=INK_SOFT, size=11),
        margin=dict(l=10, r=20, t=55 if title else 20, b=10),
        title=dict(
            text=title,
            font=dict(family="Fraunces, serif", size=16, color=INK),
            x=0.02, y=0.97,
        ) if title else None,
        legend=dict(
            bgcolor=PAPER,
            bordercolor=GRID,
            borderwidth=1,
            font=dict(size=10, color=INK_SOFT, family="Inter")
        ),
        xaxis=dict(
            gridcolor=GRID,
            zerolinecolor=GRID,
            linecolor=GRID,
            tickfont=dict(color=INK_SOFT)
        ),
        yaxis=dict(
            gridcolor=GRID,
            zerolinecolor=GRID,
            linecolor=GRID,
            tickfont=dict(color=INK_SOFT)
        ),
    )
    return fig

# Editorial daylight palette for regions — warm, varied, harmonious
REGION_PALETTE = ["#c8a96a", "#4a8a55", "#a85d3a", "#5a6b7a", "#8a6f3f", "#7a8568", "#9d6b8e", "#6a8a8a", "#a89968", "#8a5a4a", "#5a7a5a"]

# ──────────────────────── Section 1: Yield Analysis ────────────────────────
st.markdown("""
<div class="section">
    <span class="section-num">— 01</span>
    <span class="section-title">Yield <em>analysis</em></span>
    <div class="section-line"></div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    # TOP 10 YIELD — clean horizontal bars in forest green
    top10 = df.nlargest(10, "gross_yield_pct").iloc[::-1]
    fig1 = go.Figure(go.Bar(
        x=top10["gross_yield_pct"],
        y=top10["suburb"],
        orientation="h",
        marker=dict(
            color=top10["gross_yield_pct"],
            colorscale=[[0, "#a8c9ad"], [0.5, "#6ba076"], [1, "#3a6d44"]],
            line=dict(width=0)
        ),
        text=[f"{v:.2f}%" for v in top10["gross_yield_pct"]],
        textposition="outside",
        textfont=dict(size=11, color=INK, family="Fraunces"),
        hovertemplate="<b>%{y}</b><br>Gross yield: %{x:.2f}%<extra></extra>"
    ))
    fig1.update_layout(showlegend=False)
    fig1.update_xaxes(ticksuffix="%", showgrid=True, title=None)
    fig1.update_yaxes(showgrid=False, title=None)
    style_chart(fig1, title="Top 10 suburbs by gross yield")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    # LOLLIPOP CHART — Price vs Yield ranked, far more readable than scatter
    rank_df = df.copy()
    rank_df['yield_rank'] = rank_df['gross_yield_pct'].rank(ascending=False)
    top20 = rank_df.nsmallest(20, 'yield_rank').sort_values('gross_yield_pct', ascending=True)
    
    fig2 = go.Figure()
    
    # Vertical lines (lollipop stems)
    for _, row in top20.iterrows():
        fig2.add_trace(go.Scatter(
            x=[0, row['gross_yield_pct']],
            y=[row['suburb'], row['suburb']],
            mode='lines',
            line=dict(color='rgba(138, 111, 63, 0.25)', width=1.5),
            showlegend=False,
            hoverinfo='skip'
        ))
    
    # Yield dots (forest green)
    fig2.add_trace(go.Scatter(
        x=top20['gross_yield_pct'],
        y=top20['suburb'],
        mode='markers',
        marker=dict(
            size=14,
            color=FOREST,
            line=dict(color='white', width=2)
        ),
        name='Gross Yield (%)',
        customdata=top20[['median_price', 'median_weekly_rent']],
        hovertemplate="<b>%{y}</b><br>Yield: %{x:.2f}%<br>Price: $%{customdata[0]:,.0f}<br>Weekly rent: $%{customdata[1]:,.0f}<extra></extra>"
    ))
    
    fig2.update_xaxes(ticksuffix="%", title=None, showgrid=True)
    fig2.update_yaxes(title=None, showgrid=False)
    fig2.update_layout(
        showlegend=False,
        height=420
    )
    style_chart(fig2, title="Top 20 suburbs by yield — ranked")
    st.plotly_chart(fig2, use_container_width=True)

# ──────────────────────── Section 2: Investment Score ────────────────────────
st.markdown("""
<div class="section">
    <span class="section-num">— 02</span>
    <span class="section-title">Investment <em>score</em></span>
    <div class="section-line"></div>
</div>
""", unsafe_allow_html=True)

col3, col4 = st.columns(2)

with col3:
    # INVESTMENT SCORE — vertical bars in gold
    top15 = df.nlargest(15, "investment_score")
    fig3 = go.Figure(go.Bar(
        x=top15["suburb"],
        y=top15["investment_score"],
        marker=dict(
            color=top15["investment_score"],
            colorscale=[[0, "#e8d4a8"], [0.5, "#c8a96a"], [1, "#8a6f3f"]],
            line=dict(width=0)
        ),
        text=[f"{v:.1f}" for v in top15["investment_score"]],
        textposition="outside",
        textfont=dict(size=10, color=INK, family="Fraunces"),
        hovertemplate="<b>%{x}</b><br>Score: %{y:.2f}<extra></extra>"
    ))
    fig3.update_xaxes(tickangle=-35, tickfont=dict(size=9), title=None)
    fig3.update_yaxes(title=None)
    fig3.update_layout(showlegend=False)
    style_chart(fig3, title="Top 15 by composite score (yield 60% + affordability 40%)")
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    # REGIONAL HEATMAP-STYLE — average yield by region with suburb counts
    region_avg = df.groupby("region").agg(
        avg_yield=("gross_yield_pct", "mean"),
        avg_price=("median_price", "mean"),
        count=("suburb", "count")
    ).reset_index().sort_values("avg_yield", ascending=True)

    fig4 = go.Figure()
    
    # Background bars (count)
    max_count = region_avg["count"].max()
    fig4.add_trace(go.Bar(
        x=region_avg["avg_yield"],
        y=region_avg["region"],
        orientation="h",
        marker=dict(
            color=region_avg["avg_yield"],
            colorscale=[[0, "#e8d4d0"], [0.4, "#d4a89e"], [0.7, "#a85d3a"], [1, "#7a3a1a"]],
            line=dict(width=0),
            showscale=False
        ),
        text=[f"{v:.2f}% · {int(c)} suburbs" for v, c in zip(region_avg["avg_yield"], region_avg["count"])],
        textposition="outside",
        textfont=dict(size=10, color=INK, family="Fraunces"),
        hovertemplate="<b>%{y}</b><br>Avg yield: %{x:.2f}%<br>Suburbs: %{customdata}<extra></extra>",
        customdata=region_avg["count"]
    ))
    fig4.update_xaxes(ticksuffix="%", showgrid=True, title=None)
    fig4.update_yaxes(showgrid=False, title=None)
    fig4.update_layout(showlegend=False)
    style_chart(fig4, title="Regional yield map — avg yield + suburb count")
    st.plotly_chart(fig4, use_container_width=True)

# ──────────────────────── Section 3: Market Distribution ────────────────────────
st.markdown("""
<div class="section">
    <span class="section-num">— 03</span>
    <span class="section-title">Market <em>distribution</em></span>
    <div class="section-line"></div>
</div>
""", unsafe_allow_html=True)

col5, col6 = st.columns(2)

with col5:
    # PRICE DISTRIBUTION — clean histogram in terracotta
    fig5 = go.Figure(go.Histogram(
        x=df["median_price"] / 1000,
        nbinsx=25,
        marker=dict(
            color=TERRA,
            line=dict(color=PAPER, width=1)
        ),
        opacity=0.85,
        hovertemplate="Price range: $%{x:.0f}k<br>Suburbs: %{y}<extra></extra>"
    ))
    fig5.update_xaxes(tickprefix="$", ticksuffix="k", title="Median price", showgrid=True)
    fig5.update_yaxes(title="Number of suburbs", showgrid=True)
    style_chart(fig5, title="Price distribution across Sydney")
    st.plotly_chart(fig5, use_container_width=True)

with col6:
    # YIELD CATEGORY BREAKDOWN — donut chart
    yield_cat_counts = df["yield_category"].value_counts().reset_index()
    yield_cat_counts.columns = ["Category", "Count"]
    
    # Order categories logically
    order_map = {"High (5%+)": 0, "Good (4-5%)": 1, "Medium (3-4%)": 2, "Low (<3%)": 3}
    yield_cat_counts["order"] = yield_cat_counts["Category"].map(order_map)
    yield_cat_counts = yield_cat_counts.sort_values("order")
    
    cat_colours = {
        "High (5%+)": "#3a6d44",
        "Good (4-5%)": "#6ba076",
        "Medium (3-4%)": "#c8a96a",
        "Low (<3%)": "#a85d3a"
    }
    
    fig6 = go.Figure(go.Pie(
        labels=yield_cat_counts["Category"],
        values=yield_cat_counts["Count"],
        hole=0.6,
        marker=dict(
            colors=[cat_colours.get(c, GOLD) for c in yield_cat_counts["Category"]],
            line=dict(color=PAPER, width=3)
        ),
        textfont=dict(family="Fraunces, serif", size=12, color=INK),
        textinfo="label+percent",
        textposition="outside",
        hovertemplate="<b>%{label}</b><br>%{value} suburbs (%{percent})<extra></extra>"
    ))
    fig6.update_layout(
        showlegend=False,
        annotations=[dict(
            text=f"<b>{len(df)}</b><br><span style='font-size:11px;color:#6b5d4a;font-style:italic'>suburbs</span>",
            x=0.5, y=0.5,
            font=dict(family="Fraunces, serif", size=28, color=INK),
            showarrow=False
        )]
    )
    style_chart(fig6, title="Yield distribution by category")
    st.plotly_chart(fig6, use_container_width=True)

# ──────────────────────── Section 4: Suburb Register ────────────────────────
st.markdown("""
<div class="section">
    <span class="section-num">— 04</span>
    <span class="section-title">Suburb <em>register</em></span>
    <div class="section-line"></div>
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

st.dataframe(display_df, use_container_width=True, height=460, hide_index=True)

# ──────────────────────── Footer ────────────────────────
st.markdown("""
<div class="proplens-footer">
    <div>
        <div class="label">— Data Provenance</div>
        <div class="value">
            Rental — NSW Fair Trading · Mar 2026 Q&nbsp;&nbsp;|&nbsp;&nbsp;
            Sales — NSW Valuer General · Dec 2025 Q
        </div>
    </div>
    <div style="text-align:right;">
        <div class="label">— Built by</div>
        <div class="brand-foot">Prop<em>Lens</em></div>
    </div>
</div>
""", unsafe_allow_html=True)
