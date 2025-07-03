import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ─── 1. Load & prepare data ─────────────────────────────────────────────────────
BASE       = Path(__file__).parent
DATA_FP    = BASE / "data" / "processed" / "sales_clean.csv"

# Read in the cleaned sales CSV
df = pd.read_csv(DATA_FP, parse_dates=["ContractDate"])

# ─── 2. Page config & title ────────────────────────────────────────────────────
st.set_page_config(
    page_title="Solar Contract Sales & Invoicing",
    page_icon="☀️",
    layout="wide"
)
st.title("☀️ Solar Contract Sales & Invoicing")
st.markdown(
    "A quick look at total contracts, revenue, and month-over-month performance."
)

# ─── 3. Key metrics ─────────────────────────────────────────────────────────────
total_contracts = len(df)
total_revenue  = df["TotalAmount"].sum()

col1, col2 = st.columns(2)
col1.metric("Total Contracts", f"{total_contracts:,}")
col2.metric("Total Revenue", f"${total_revenue:,.2f}")

st.markdown("---")

# ─── 4. Monthly Revenue Chart ───────────────────────────────────────────────────
# Create a Month column for grouping
df["Month"] = df["ContractDate"].dt.to_period("M").dt.to_timestamp()

revenue_by_month = (
    df
    .groupby("Month", as_index=False)["TotalAmount"]
    .sum()
    .rename(columns={"TotalAmount": "Revenue"})
)

fig = px.bar(
    revenue_by_month,
    x="Month",
    y="Revenue",
    labels={"Month": "Month", "Revenue": "Revenue (USD)"},
    title="Monthly Revenue"
)
st.plotly_chart(fig, use_container_width=True)

# ─── 5. Data table preview ──────────────────────────────────────────────────────
with st.expander("Show raw data"):
    st.dataframe(
        df[[
            "ContractID", "CustomerName", "ContractDate",
            "kWh", "RatePerkWh", "TotalAmount"
        ]].sort_values("ContractDate", ascending=False),
        height=400
    )

# ─── 6. Footer ───────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("Built with Python • Streamlit • Plotly")
