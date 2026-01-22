import streamlit as st
import polars as pl

nums_to_months = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}
month_site_data = pl.read_csv("../DSU-Dataset-Monthly-Site-Summary.csv").sort(["Year", "Month"], descending=False)
month_data = pl.read_csv("../DSU-Dataset-Monthly-Summary.csv").sort(["Year", "Month"], descending=False)

month_day_site_data = pl.read_csv("../DSU-Dataset-Monthly-Day-Site-Summary.csv").sort(["Year", "Month"], descending=False)
month_day_data = pl.read_csv("../DSU-Dataset-Monthly-Day-Summary.csv").sort(["Year", "Month"], descending=False)

show_sites = st.checkbox("Aggregate Sites?")
if show_sites:
    st.header("Monthly Site Summary Data")
else:
    st.header("Monthly Summary Data")

year = st.radio(
    "Select a year:",
    options=month_data["Year"].unique().sort().to_list(),
    key="month_site_data"
)

if show_sites:
    site = st.radio(
        "Select a site:",
        options=month_site_data["Site"].unique().sort().to_list(),
    )

if show_sites:
    st.dataframe(month_site_data.filter(pl.col("Site") == site).filter(pl.col("Year") == year).to_pandas().style.format({"Month": lambda x: nums_to_months[x]}))
else:
    st.dataframe(month_data.filter(pl.col("Year") == year).to_pandas().style.format({"Month": lambda x: nums_to_months[x]}))

show_col = st.pills("Show: ", options=["ED Enc", "ED Enc Admitted"], selection_mode="multi", default=["ED Enc", "ED Enc Admitted"])
smooth_lines = st.checkbox("Smoother lines?")

if show_sites:
    if smooth_lines:
        st.line_chart(month_site_data.filter(pl.col("Site") == site).filter(pl.col("Year") == year), x="Month", y=show_col)
    else:
        st.line_chart(month_day_site_data.filter(pl.col("Site") == site).filter(pl.col("Year") == year), x="Month", y=show_col)
elif smooth_lines:
    st.line_chart(month_data.filter(pl.col("Year") == year), x="Month", y=show_col)
else:
    st.line_chart(month_day_data.filter(pl.col("Year") == year), x="Month", y=show_col)