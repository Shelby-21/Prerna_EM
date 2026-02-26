import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="FruitFrost Pricing Intelligence Dashboard",
    layout="wide"
)

st.title("🧊 FruitFrost Pricing & Revenue Intelligence Dashboard")
st.markdown("AI-driven pricing, demand and revenue optimisation for FruitFrost Ice Cubes")

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_data():
    file_path = "FruitFrost_Pricing_Dashboard_Master.xlsx"
    historical = pd.read_excel(file_path, sheet_name="Historical_Sales")
    competitor = pd.read_excel(file_path, sheet_name="Competitor")
    scenario = pd.read_excel(file_path, sheet_name="Scenario_Simulation")
    cost = pd.read_excel(file_path, sheet_name="Cost_Structure")
    return historical, competitor, scenario, cost

historical, competitor, scenario, cost = load_data()

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("Filters")

city_filter = st.sidebar.multiselect(
    "Select City",
    options=historical["City"].unique(),
    default=historical["City"].unique()
)

filtered_data = historical[historical["City"].isin(city_filter)]

# -----------------------------
# KPI Section
# -----------------------------
st.subheader("📊 Executive Summary")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Revenue (₹)", f"{filtered_data['Revenue'].sum():,.0f}")
col2.metric("Total Profit (₹)", f"{filtered_data['Profit'].sum():,.0f}")
col3.metric("Avg Price (₹)", f"{filtered_data['Price_per_Unit'].mean():.2f}")
col4.metric("Total Units Sold", f"{filtered_data['Units_Sold'].sum():,.0f}")

# -----------------------------
# Revenue Trend
# -----------------------------
st.subheader("📈 Revenue & Profit Trend")

trend = filtered_data.groupby("Month")[["Revenue", "Profit"]].sum().reindex(
    ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
)

fig, ax = plt.subplots()
ax.plot(trend.index, trend["Revenue"], label="Revenue")
ax.plot(trend.index, trend["Profit"], label="Profit")
ax.set_ylabel("₹ Value")
ax.set_xlabel("Month")
ax.legend()
st.pyplot(fig)

# -----------------------------
# Pricing vs Demand Analysis
# -----------------------------
st.subheader("💰 Pricing vs Demand Analysis")

fig, ax = plt.subplots()
ax.scatter(
    filtered_data["Price_per_Unit"],
    filtered_data["Units_Sold"]
)
ax.set_xlabel("Price per Unit (₹)")
ax.set_ylabel("Units Sold")
st.pyplot(fig)

# -----------------------------
# Price Elasticity Calculation
# -----------------------------
st.subheader("📉 Price Elasticity Estimation")

price = filtered_data["Price_per_Unit"]
demand = filtered_data["Units_Sold"]

elasticity = np.polyfit(price, demand, 1)[0] * (price.mean() / demand.mean())

st.metric("Estimated Price Elasticity", f"{elasticity:.2f}")

st.caption("Elasticity < -1 indicates price-sensitive demand")

# -----------------------------
# Revenue Optimisation Simulator
# -----------------------------
st.subheader("🧮 Revenue Optimisation Simulator")

price_slider = st.slider(
    "Select Price (₹)",
    min_value=20,
    max_value=35,
    value=25
)

cost_per_unit = st.slider(
    "Cost per Unit (₹)",
    min_value=8,
    max_value=18,
    value=12
)

expected_demand = 15000 - price_slider * 300
expected_revenue = price_slider * expected_demand
expected_profit = (price_slider - cost_per_unit) * expected_demand

col1, col2, col3 = st.columns(3)
col1.metric("Expected Demand", f"{expected_demand:,.0f}")
col2.metric("Expected Revenue (₹)", f"{expected_revenue:,.0f}")
col3.metric("Expected Profit (₹)", f"{expected_profit:,.0f}")

# -----------------------------
# Scenario Simulation
# -----------------------------
st.subheader("📊 Pricing Scenario Analysis")

fig, ax = plt.subplots()
ax.plot(scenario["Price_Option"], scenario["Revenue"], label="Revenue")
ax.plot(scenario["Price_Option"], scenario["Profit"], label="Profit")
ax.set_xlabel("Price Option (₹)")
ax.set_ylabel("₹ Value")
ax.legend()
st.pyplot(fig)

# -----------------------------
# Cost Structure
# -----------------------------
st.subheader("🏭 Cost Structure Breakdown")

fig, ax = plt.subplots()
ax.pie(
    cost["Cost_Percentage"],
    labels=cost["Component"],
    autopct="%1.0f%%"
)
st.pyplot(fig)

# -----------------------------
# Competitive Pricing
# -----------------------------
st.subheader("⚔️ Competitive Pricing Benchmark")

fig, ax = plt.subplots()
ax.plot(
    competitor["Month"],
    competitor["Competitor_Avg_Price"],
    label="Competitor Avg Price"
)
ax.axhline(
    y=filtered_data["Price_per_Unit"].mean(),
    linestyle="--",
    label="FruitFrost Avg Price"
)
ax.legend()
ax.set_ylabel("Price (₹)")
st.pyplot(fig)

# -----------------------------
# Final Insight
# -----------------------------
st.success(
    "📌 Insight: Segment-based pricing outperforms uniform pricing. "
    "Premium outlets tolerate higher prices while high-volume outlets require lower pricing to retain demand."
)
