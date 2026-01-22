import streamlit as st
import polars as pl

st.title("Sanford Health/DSU Data Competition")
st.set_page_config(
    page_title="Sanford Health/DSU Data Competition Visualizations",
    page_icon="😴"
)
st.sidebar.success("Welcome!")
st.markdown("This is Team No Sleep's Streamlit app to illustrate dataframes and visualizations.")

nums_to_months = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}

data = pl.read_csv("../DSU-Dataset-Monthly-Summary.csv").sort(["Year", "Month"], descending=False)

st.dataframe(data.to_pandas().style.format({"Month": lambda x: nums_to_months[x]}))

data = data.with_columns(
    pl.datetime(pl.col("Year"), pl.col("Month"), pl.lit(1)).alias("Date")
).drop(["Year", "Month"])

st.line_chart(data, x="Date", y=["ED Enc", "ED Enc Admitted"])