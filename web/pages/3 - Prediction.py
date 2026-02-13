import streamlit as st
import polars as pl
import pandas as pd
import matplotlib as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from datetime import datetime, timedelta
import numpy as np
import os
from catboost import CatBoostRegressor

st.title("Predictions for a selected site")
st.write("This uses CatBoost, trained on data after COVID.")
st.set_page_config(
    page_title="Sanford Health/DSU Data Competition Visualizations",
    page_icon="😴"
)

cwd = os.getcwd()
web_dir = os.path.join(cwd, "web")
models_dir = os.path.join(cwd, "models")

siteA_model = CatBoostRegressor().load_model(os.path.join(models_dir, "siteA_catmodel.cbm"))
siteB_model = CatBoostRegressor().load_model(os.path.join(models_dir, "siteB_catmodel.cbm"))
siteC_model = CatBoostRegressor().load_model(os.path.join(models_dir, "siteC_catmodel.cbm"))
siteD_model = CatBoostRegressor().load_model(os.path.join(models_dir, "siteD_catmodel.cbm"))

data = pl.read_csv(os.path.join(web_dir, "DSU-Dataset-Hourly-Blocks-Summary.csv")).sort(["Year", "Month"], descending=False)
last_date = data.select(pl.col("Date").max()).to_numpy()[0][0]
use_date_range = st.checkbox("Predict date range?")
if use_date_range:
    today = datetime.today()
    default_date = (today, today + timedelta(days=7))
else:
    default_date = "today"
predict_date = st.date_input("Select a date to predict ED Encounters and Admissions for each site:", value=default_date, min_value=last_date)
site = st.selectbox("Select a site to view predictions for:", options=["All Sites", "A", "B", "C", "D"])

if use_date_range:
    date_range = pd.date_range(start=predict_date[0], end=predict_date[1])
    predict_data = [
        pl.Series("Year", np.array([[d.year] * 4 for d in date_range]).flatten()),
        pl.Series("Month", np.array([[d.month] * 4 for d in date_range]).flatten()),
        pl.Series("Day", np.array([[d.day] * 4 for d in date_range]).flatten()),
        pl.Series("Hour", [0, 6, 12, 18] * len(date_range)),
        pl.Series("Weekday", np.array([[d.weekday() + 1] * 4 for d in date_range]).flatten()),
    ]
else:
    predict_data = [
        pl.Series("Year", [predict_date.year] * 4),
        pl.Series("Month", [predict_date.month] * 4),
        pl.Series("Day", [predict_date.day] * 4),
        pl.Series("Hour", [0, 6, 12, 18]),
        pl.Series("Weekday", [predict_date.weekday() + 1] * 4),
    ]
predict_X = pl.DataFrame(predict_data)

if (site == "A"):
    st.header("Site A Model:")
if (site == "B"):
    st.header("Site B Model:")
if (site == "C"):
    st.header("Site C Model:")
if (site == "D"):
    st.header("Site D Model:")


if (site == "A" or site == "All Sites"):
    siteA_prediction = pl.DataFrame(siteA_model.predict(predict_X.to_pandas()))

    siteA_prediction = predict_X.with_columns([
        pl.Series("ED Enc", siteA_prediction[:, 0].ceil(), dtype=pl.Int32),
        pl.Series("ED Enc Admitted", siteA_prediction[:, 1].ceil(), dtype=pl.Int32),
        pl.lit("A", dtype=pl.Utf8).alias("Site")
    ]).sort(["Year", "Month", "Day", "Hour"])

if (site == "B" or site == "All Sites"):
    siteB_prediction = pl.DataFrame(siteB_model.predict(predict_X.to_pandas()))

    siteB_prediction = predict_X.with_columns([
        pl.Series("ED Enc", siteB_prediction[:, 0].ceil(), dtype=pl.Int32),
        pl.Series("ED Enc Admitted", siteB_prediction[:, 1].ceil(), dtype=pl.Int32),
        pl.lit("B", dtype=pl.Utf8).alias("Site")
    ]).sort(["Year", "Month", "Day", "Hour"])

if (site == "C" or site == "All Sites"):
    siteC_prediction = pl.DataFrame(siteC_model.predict(predict_X.to_pandas()))

    siteC_prediction = predict_X.with_columns([
        pl.Series("ED Enc", siteC_prediction[:, 0].ceil(), dtype=pl.Int32),
        pl.Series("ED Enc Admitted", siteC_prediction[:, 1].ceil(), dtype=pl.Int32),
        pl.lit("C", dtype=pl.Utf8).alias("Site")
    ]).sort(["Year", "Month", "Day", "Hour"])

if (site == "D" or site == "All Sites"):
    siteD_prediction = pl.DataFrame(siteD_model.predict(predict_X.to_pandas()))

    siteD_prediction = predict_X.with_columns([
        pl.Series("ED Enc", siteD_prediction[:, 0].ceil(), dtype=pl.Int32),
        pl.Series("ED Enc Admitted", siteD_prediction[:, 1].ceil(), dtype=pl.Int32),
        pl.lit("D", dtype=pl.Utf8).alias("Site")
    ]).sort(["Year", "Month", "Day", "Hour"])

nums_to_months = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}
nums_to_weekdays = {1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday", 7: "Sunday"}

if (site == "A"):
    st.dataframe(siteA_prediction.to_pandas().style.format({"Month": lambda x: nums_to_months[x], "Weekday": lambda x: nums_to_weekdays[x]}))
    st.bar_chart(data=siteA_prediction, x="Hour", y=["ED Enc", "ED Enc Admitted"], stack=False)
if (site == "B"):
    st.dataframe(siteB_prediction.to_pandas().style.format({"Month": lambda x: nums_to_months[x], "Weekday": lambda x: nums_to_weekdays[x]}))
    st.bar_chart(data=siteB_prediction, x="Hour", y=["ED Enc", "ED Enc Admitted"], stack=False)
if (site == "C"):
    st.dataframe(siteC_prediction.to_pandas().style.format({"Month": lambda x: nums_to_months[x], "Weekday": lambda x: nums_to_weekdays[x]}))
    st.bar_chart(data=siteC_prediction, x="Hour", y=["ED Enc", "ED Enc Admitted"], stack=False)
if (site == "D"):
    st.dataframe(siteD_prediction.to_pandas().style.format({"Month": lambda x: nums_to_months[x], "Weekday": lambda x: nums_to_weekdays[x]}))
    st.bar_chart(data=siteD_prediction, x="Hour", y=["ED Enc", "ED Enc Admitted"], stack=False)

if (site == "All Sites"):
    overall_prediction = pl.concat([siteA_prediction, siteB_prediction, siteC_prediction, siteD_prediction])
    overall_prediction_csv = overall_prediction.with_columns(
        pl.datetime(year=pl.col("Year"), month=pl.col("Month"), day=pl.col("Day"), hour=pl.col("Hour")).alias("Date")
    ).drop(["Year", "Month", "Day", "Weekday", "Hour"]).select(["Site", "Date", "ED Enc", "ED Enc Admitted"])
    st.dataframe(overall_prediction.to_pandas().style.format({"Month": lambda x: nums_to_months[x], "Weekday": lambda x: nums_to_weekdays[x]}))
    st.download_button("Download CSV", overall_prediction_csv.to_pandas().to_csv(index=False).encode("utf-8"), "overall_prediction.csv", "text/csv")

    if (use_date_range):
        plot_df = overall_prediction.with_columns(
            pl.date(year=pl.col("Year"), month=pl.col("Month"), day=pl.col("Day")).alias("Date")
        ).group_by("Date").agg(pl.col("ED Enc").sum().alias("ED Enc"), pl.col("ED Enc Admitted").sum().alias("ED Enc Admitted"))

        st.write("This graph sums the ED Enc and ED Enc Admitted by date and site.")
        st.line_chart(data=plot_df, x="Date", y=["ED Enc", "ED Enc Admitted"])
    else:
        st.write("Where hour is the start of the 6 hour block.")
        st.bar_chart(data=overall_prediction, x="Hour", y=["ED Enc", "ED Enc Admitted"], stack=False)