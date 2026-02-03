import streamlit as st
import polars as pl
import os

st.set_page_config(
    page_title="Sanford Health/DSU Data Competition Visualizations",
    page_icon="😴"
)

cwd = os.getcwd()
web_dir = os.path.join(cwd, "web")

reasons = pl.read_csv(os.path.join(web_dir, "reasons.csv"))
nums_to_months = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}
seasons = {"Winter": [12, 1, 2], "Spring": [3, 4, 5], "Summer": [6, 7, 8], "Fall": [9, 10, 11]}

st.header("Popularity of Visit Reasons")
timeframe = st.selectbox("Select a timeframe:", options=["All time", "Yearly", "Monthly", "Seasonal"])
site = st.selectbox("Select a site:", options=["Across All Sites", "A", "B", "C", "D"])
if site != "Across All Sites":
    reasons = reasons.filter(pl.col("Site") == site)

if timeframe == "All time":
    df_all = reasons.group_by("REASON_VISIT_NAME").agg(
        pl.col("Total ED Enc").sum().alias("Total ED Enc"),
        pl.col("Total ED Enc Admitted").sum().alias("Total ED Enc Admitted")
    ).with_columns(
        (pl.col("Total ED Enc Admitted") / pl.col("Total ED Enc")).alias("Percentage admitted to floor")
    ).sort("Total ED Enc", descending=True)
    st.dataframe(df_all,
                 column_config={
                     "Percentage admitted to floor": st.column_config.NumberColumn(format="percent")
                 })
    st.bar_chart(df_all, x="REASON_VISIT_NAME", y="Total ED Enc", horizontal=True, sort="-Total ED Enc")

if timeframe == "Yearly":
    year = st.selectbox("Select a year:", options=range(2018, 2026))
    df_yearly = reasons.filter(pl.col("Year") == year)
    df_yearly = df_yearly.group_by("REASON_VISIT_NAME").agg(
        pl.col("Total ED Enc").sum().alias("Total ED Enc"),
        pl.col("Total ED Enc Admitted").sum().alias("Total ED Enc Admitted")
    ).with_columns(
        (pl.col("Total ED Enc Admitted") / pl.col("Total ED Enc")).alias("Percentage admitted to floor")
    ).sort("Total ED Enc", descending=True)
    st.dataframe(df_yearly,
                 column_config={
                     "Percentage admitted to floor": st.column_config.NumberColumn(format="percent")
                 })
    st.bar_chart(df_yearly, x="REASON_VISIT_NAME", y="Total ED Enc", horizontal=True, sort="-Total ED Enc")

if timeframe == "Monthly":
    month = st.selectbox("Select a month:", options=range(1, 13), format_func=lambda x: nums_to_months[x])
    st.markdown("This finds the sum of all visits for each reason in the selected month across all years.")
    df_monthly = reasons.filter(pl.col("Month") == month)
    df_monthly = df_monthly.group_by("REASON_VISIT_NAME").agg(
        pl.col("Total ED Enc").sum().alias("Total ED Enc"),
        pl.col("Total ED Enc Admitted").sum().alias("Total ED Enc Admitted")
    ).with_columns(
        (pl.col("Total ED Enc Admitted") / pl.col("Total ED Enc")).alias("Percentage admitted to floor")
    ).sort("Total ED Enc", descending=True)
    st.dataframe(df_monthly,
                 column_config={
                     "Percentage admitted to floor": st.column_config.NumberColumn(format="percent")
                 })
    st.bar_chart(df_monthly, x="REASON_VISIT_NAME", y="Total ED Enc", horizontal=True, sort="-Total ED Enc")

if timeframe == "Seasonal":
    season = st.selectbox("Select a season:", options=["Winter", "Spring", "Summer", "Fall"])
    st.markdown('''This finds the sum of all visits for each reason in the selected season across all years.
                
                Winter is December, January, February
                
                Spring is March, April, May
                
                Summer is June, July, August
                
                Fall is September, October, November.''')

    df_seasonal = reasons.filter(pl.col("Month").is_in(seasons[season]))
    df_seasonal = df_seasonal.group_by("REASON_VISIT_NAME").agg(
        pl.col("Total ED Enc").sum().alias("Total ED Enc"),
        pl.col("Total ED Enc Admitted").sum().alias("Total ED Enc Admitted")
    ).with_columns(
        (pl.col("Total ED Enc Admitted") / pl.col("Total ED Enc")).alias("Percentage admitted to floor")
    ).sort("Total ED Enc", descending=True)
    st.dataframe(df_seasonal,
                 column_config={
                     "Percentage admitted to floor": st.column_config.NumberColumn(format="percent")
                 })
    st.bar_chart(df_seasonal, x="REASON_VISIT_NAME", y="Total ED Enc", horizontal=True, sort="-Total ED Enc")