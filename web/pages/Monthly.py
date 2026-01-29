import streamlit as st
import polars as pl

nums_to_months = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}
data = pl.read_csv("../DSU-Dataset-Hourly-Blocks-Summary.csv")
site_data = data.group_by("Site", "Year", "Month", "Date").agg(pl.col("ED Enc").sum().alias("ED Enc"), pl.col("ED Enc Admitted").sum().alias("ED Enc Admitted")).sort("Date")
overall_data = site_data.group_by("Year", "Month", "Date").agg(pl.col("ED Enc").sum().alias("ED Enc"), pl.col("ED Enc Admitted").sum().alias("ED Enc Admitted")).sort("Date")

st.header("Monthly Summary Data")
st.set_page_config(
    page_title="Sanford Health/DSU Data Competition Visualizations",
    page_icon="😴"
)

show_sites = st.checkbox("View an individual site?")

year = st.selectbox(
    "Select a year:",
    options=overall_data["Year"].unique().sort().to_list(),
    key="month_site_data"
)

if show_sites:
    site = st.selectbox(
        "Select a site:",
        options=site_data["Site"].unique().sort().to_list(),
    )

if show_sites:
    st.dataframe(site_data.filter(pl.col("Site") == site).filter(pl.col("Year") == year).to_pandas().style.format({"Month": lambda x: nums_to_months[x]}))
else:
    st.dataframe(overall_data.filter(pl.col("Year") == year).to_pandas().style.format({"Month": lambda x: nums_to_months[x]}))

show_col = st.pills("Show: ", options=["ED Enc", "ED Enc Admitted"], selection_mode="multi", default=["ED Enc", "ED Enc Admitted"])

if show_sites:
    st.line_chart(site_data.filter(pl.col("Site") == site).filter(pl.col("Year") == year), x="Date", y=show_col)
else:
    st.line_chart(overall_data.filter(pl.col("Year") == year), x="Date", y=show_col)