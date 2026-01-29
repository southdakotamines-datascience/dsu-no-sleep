import streamlit as st
import polars as pl

st.title("Daily Summary Data")
st.set_page_config(
    page_title="Sanford Health/DSU Data Competition Visualizations",
    page_icon="😴"
)

data = pl.read_csv("../DSU-Dataset-Hourly-Blocks-Summary.csv")

nums_to_hours = {1: "0-5", 2: "6-11", 3: "12-17", 4: "18-23"}

d = st.date_input("Select a date to view:", min_value=data["Date"].min(), max_value=data["Date"].max())
site = st.selectbox(
    "Select a site:",
    options=["All Sites", *data["Site"].unique().sort().to_list()],
)

if site == "All Sites":
    day_data = data.filter(pl.col("Year") == pl.lit(d.year)).filter(pl.col("Month") == pl.lit(d.month)).filter(pl.col("Day") == pl.lit(d.day))
    day_data = day_data.select("Site", "Hour", "ED Enc", "ED Enc Admitted")
    day_data = day_data.sort(["Site", "Hour"])

    st.dataframe(day_data.to_pandas().style.format({"Hour": lambda x: nums_to_hours[x]}))
    show_col = st.pills("Show: ", options=["ED Enc", "ED Enc Admitted"], selection_mode="single", default="ED Enc")
    st.bar_chart(day_data, x="Hour", y=show_col, color="Site", stack=False)
else:
    site_data = data.filter(pl.col("Site") == site)
    site_day_data = site_data.filter(pl.col("Year") == pl.lit(d.year)).filter(pl.col("Month") == pl.lit(d.month)).filter(pl.col("Day") == pl.lit(d.day))
    site_day_data = site_day_data.select("Site", "Hour", "ED Enc", "ED Enc Admitted")
    site_day_data = site_day_data.sort(["Site", "Hour"])
    st.dataframe(site_day_data.to_pandas().style.format({"Hour": lambda x: nums_to_hours[x]}))
    st.bar_chart(site_day_data, x="Hour", y=["ED Enc", "ED Enc Admitted"], stack=False)
