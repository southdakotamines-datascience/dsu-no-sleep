import streamlit as st
import polars as pl
import os

cwd = os.getcwd()

data = pl.read_csv(os.path.join(cwd, "DSU-Dataset-Hourly-Blocks-Summary.csv")).sort(["Year", "Month"], descending=False)\
      .group_by(["Year", "Month"])\
      .agg(\
          pl.col("ED Enc").sum().alias("ED Enc"),\
          pl.col("ED Enc Admitted").sum().alias("ED Enc Admitted"),\
          pl.col("Date").first())
st.title("Sanford Health/DSU Data Competition")
st.set_page_config(
    page_title="Sanford Health/DSU Data Competition Visualizations",
    page_icon="😴"
)
st.markdown("This is Team No Sleep's Streamlit app to illustrate dataframes and visualizations.")
st.header("This is the overall data with all 4 sites combined and months are summed together.")

nums_to_months = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}
data = data.sort(["Date"])

st.dataframe(data.drop("Date").to_pandas().style.format({"Month": lambda x: nums_to_months[x]}))

st.line_chart(data, x="Date", y=["ED Enc", "ED Enc Admitted"])