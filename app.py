import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from data import get_sydney_data

# Page config
st.set_page_config(
    page_title="Sydney Rental Yield Analyser",
    page_icon="🏠",
    layout="wide"
)

# Load data
df = get_sydney_data()

# Header
st.title("🏠 Sydney Rental Yield Analyser")
st.markdown("*Analyse rental yields across Sydney suburbs to find the best investment opportunities*")
st.divider()

# Sidebar filters
st.sidebar.header("🔍 Filter Suburbs")

regions = ["All Regions"] + sorted(df["region"].unique().tolist())
selected_region = st.sidebar.selectbox("Select Region", regions)

min_yield, max_yield = st.sidebar.slider(
    "Gross Yield Range (%)",
    min_value=float(df["gross_yield_pct"].min()),
    max_value=float(df["gross_yield_pct"].max()),
    value=(float(df["gross_yield_pct"].min()), float(df["gross_yield_pct"].max())),
    step=0.1
)

max_price = st.sidebar.slider(
    "Max Property Price ($)",
    min_value=int(df["median_price"].min()),
    max_value=int(df["median_price"].max()),
    value=int(df["median_price"].max()),
    step=50000,
    format="$%d"
)

# Apply filters
filtered_df = df.copy()
if selected_region != "All Regions":
    filtered_df = filtered_df[filtered_df["region"] == selected_region]
filtered_df = filtered_df[
    (filtered_df["gross_yield_pct"] >= min_yield) &
    (filtered_df["gross_yield_pct"] <= max_yield) &
    (filtered_df["median_price"] <= max_price)
]

# KPI metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Suburbs Shown", len(filtered_df))
with col2:
    st.metric("Avg Gross Yield", f"{filtered_df['gross_yield_pct'].mean():.2f}%")
with col3:
    st.metric("Avg Median Price", f"${filtered_df['median_price'].mean():,.0f}")
with col4:
    st.metric("Avg Weekly Rent", f"${filtered_df['median_weekly_rent'].mean():,.0f}")

st.divider()

# Charts row
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("📊 Top 10 Suburbs by Gross Yield")
    top10 = filtered_df.nlargest(10, "gross_yield_pct")
    fig1 = px.bar(
        top10,
        x="gross_yield_pct",
        y="suburb",
        orientation="h",
        color="gross_yield_pct",
        color_continuous_scale="Greens",
        labels={"gross_yield_pct": "Gross Yield (%)", "suburb": "Suburb"},
        text="gross_yield_pct"
    )
    fig1.update_traces(texttemplate="%{text:.2f}%", textposition="outside")
    fig1.update_layout(height=400, showlegend=False, coloraxis_showscale=False)
    st.plotly_chart(fig1, use_container_width=True)

with col_right:
    st.subheader("💰 Price vs Yield by Region")
    fig2 = px.scatter(
        filtered_df,
        x="median_price",
        y="gross_yield_pct",
        color="region",
        hover_name="suburb",
        size="median_weekly_rent",
        labels={
            "median_price": "Median Property Price ($)",
            "gross_yield_pct": "Gross Yield (%)",
            "region": "Region"
        }
    )
    fig2.update_layout(height=400)
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# Investment score chart
st.subheader("⭐ Investment Score — Top 15 Suburbs")
st.caption("Score combines rental yield (60%) and affordability (40%)")
top15 = filtered_df.nlargest(15, "investment_score")
fig3 = px.bar(
    top15,
    x="suburb",
    y="investment_score",
    color="region",
    labels={"investment_score": "Investment Score", "suburb": "Suburb"},
    text="investment_score"
)
fig3.update_traces(texttemplate="%{text:.2f}", textposition="outside")
fig3.update_layout(height=400, xaxis_tickangle=-35)
st.plotly_chart(fig3, use_container_width=True)

st.divider()

# Yield by region box
st.subheader("📍 Yield Distribution by Region")
fig4 = px.box(
    filtered_df,
    x="region",
    y="gross_yield_pct",
    color="region",
    labels={"gross_yield_pct": "Gross Yield (%)", "region": "Region"}
)
fig4.update_layout(height=400, showlegend=False, xaxis_tickangle=-20)
st.plotly_chart(fig4, use_container_width=True)

st.divider()

# Full data table
st.subheader("📋 Full Suburb Data")
display_df = filtered_df[[
    "suburb", "region", "median_price", "median_weekly_rent",
    "gross_yield_pct", "yield_category", "investment_score"
]].sort_values("gross_yield_pct", ascending=False).reset_index(drop=True)

display_df.columns = [
    "Suburb", "Region", "Median Price ($)", "Weekly Rent ($)",
    "Gross Yield (%)", "Yield Category", "Investment Score"
]
display_df["Median Price ($)"] = display_df["Median Price ($)"].apply(lambda x: f"${x:,}")
display_df["Weekly Rent ($)"] = display_df["Weekly Rent ($)"].apply(lambda x: f"${x:,}")

st.dataframe(display_df, use_container_width=True, height=400)

# Footer
st.divider()
st.caption("⚠️ Data shown is for demonstration purposes. Connect to NSW Valuer General and NSW Fair Trading APIs for live data.")