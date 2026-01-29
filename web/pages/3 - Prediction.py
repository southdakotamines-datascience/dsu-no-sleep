import streamlit as st
import polars as pl
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

st.title("Predictions for a selected site")
st.set_page_config(
    page_title="Sanford Health/DSU Data Competition Visualizations",
    page_icon="😴"
)

data = pl.read_csv("../DSU-Dataset-Hourly-Blocks-Summary.csv")
last_date = data.select(pl.col("Date").max()).to_numpy()[0][0]
nums_to_months = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}
nums_to_hours = {1: "0-5", 2: "6-11", 3: "12-17", 4: "18-23"}
nums_to_weekdays = {1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday", 7: "Sunday"}

predict_date = st.date_input("Select a date to predict ED Encounters and Admissions for each site:", min_value=last_date)
site = st.selectbox("Select a site to view predictions for:", options=["A", "B", "C", "D"])
predict_data = [
    pl.Series("Year", [predict_date.year] * 4),
    pl.Series("Month", [predict_date.month] * 4),
    pl.Series("Day", [predict_date.day] * 4),
    pl.Series("Hour", [1, 2, 3, 4]),
    pl.Series("Weekday", [predict_date.weekday() + 1] * 4),
]
predict_X = pl.DataFrame(predict_data)

if (site == "A"):
    # Site A
    siteA_X = data.filter(pl.col("Site") == "A").select(["Year", "Month", "Day", "Hour", "Weekday"]).to_numpy()
    siteA_Y = data.filter(pl.col("Site") == "A").select(["ED Enc", "ED Enc Admitted"]).to_numpy()
    siteA_model = LinearRegression().fit(siteA_X, siteA_Y)

    siteA_X_train, siteA_X_test, siteA_Y_train, siteA_Y_test = train_test_split(siteA_X, siteA_Y, test_size=0.2, random_state=42)
    st.header("Site A Model Performance:")
    st.write(f"R^2 Score: {siteA_model.score(siteA_X_test, siteA_Y_test):.4f}")

    siteA_prediction = pl.DataFrame(siteA_model.predict(predict_X))

    siteA_prediction = predict_X.with_columns([
        pl.Series("ED Enc", siteA_prediction[:, 0]),
        pl.Series("ED Enc Admitted", siteA_prediction[:, 1])
    ])
    st.dataframe(siteA_prediction.to_pandas().style.format({"Month": lambda x: nums_to_months[x], "Hour": lambda x: nums_to_hours[x], "Weekday": lambda x: nums_to_weekdays[x]}))
    st.bar_chart(data=siteA_prediction, x="Hour", y=["ED Enc", "ED Enc Admitted"], stack=False)

if (site == "B"):
    # Site B
    siteB_X = data.filter(pl.col("Site") == "B").select(["Year", "Month", "Day", "Hour", "Weekday"]).to_numpy()
    siteB_Y = data.filter(pl.col("Site") == "B").select(["ED Enc", "ED Enc Admitted"]).to_numpy()
    siteB_model = LinearRegression().fit(siteB_X, siteB_Y)

    siteB_X_train, siteB_X_test, siteB_Y_train, siteB_Y_test = train_test_split(siteB_X, siteB_Y, test_size=0.2, random_state=42)
    st.header("Site B Model Performance:")
    st.write(f"R^2 Score: {siteB_model.score(siteB_X_test, siteB_Y_test):.4f}")

    siteB_prediction = pl.DataFrame(siteB_model.predict(predict_X))

    siteB_prediction = predict_X.with_columns([
        pl.Series("ED Enc", siteB_prediction[:, 0]),
        pl.Series("ED Enc Admitted", siteB_prediction[:, 1])
    ])
    st.dataframe(siteB_prediction.to_pandas().style.format({"Month": lambda x: nums_to_months[x], "Hour": lambda x: nums_to_hours[x], "Weekday": lambda x: nums_to_weekdays[x]}))
    st.bar_chart(data=siteB_prediction, x="Hour", y=["ED Enc", "ED Enc Admitted"], stack=False)

if (site == "C"):
    # Site C
    siteC_X = data.filter(pl.col("Site") == "C").select(["Year", "Month", "Day", "Hour", "Weekday"]).to_numpy()
    siteC_Y = data.filter(pl.col("Site") == "C").select(["ED Enc", "ED Enc Admitted"]).to_numpy()
    siteC_model = LinearRegression().fit(siteC_X, siteC_Y)

    siteC_X_train, siteC_X_test, siteC_Y_train, siteC_Y_test = train_test_split(siteC_X, siteC_Y, test_size=0.2, random_state=42)
    st.header("Site C Model Performance:")
    st.write(f"R^2 Score: {siteC_model.score(siteC_X_test, siteC_Y_test):.4f}")

    siteC_prediction = pl.DataFrame(siteC_model.predict(predict_X))

    siteC_prediction = predict_X.with_columns([
        pl.Series("ED Enc", siteC_prediction[:, 0]),
        pl.Series("ED Enc Admitted", siteC_prediction[:, 1])
    ])
    st.dataframe(siteC_prediction.to_pandas().style.format({"Month": lambda x: nums_to_months[x], "Hour": lambda x: nums_to_hours[x], "Weekday": lambda x: nums_to_weekdays[x]}))
    st.bar_chart(data=siteC_prediction, x="Hour", y=["ED Enc", "ED Enc Admitted"], stack=False)

if (site == "D"):
    # Site D
    siteD_X = data.filter(pl.col("Site") == "D").select(["Year", "Month", "Day", "Hour", "Weekday"]).to_numpy()
    siteD_Y = data.filter(pl.col("Site") == "D").select(["ED Enc", "ED Enc Admitted"]).to_numpy()
    siteD_model = LinearRegression().fit(siteD_X, siteD_Y)

    siteD_X_train, siteD_X_test, siteD_Y_train, siteD_Y_test = train_test_split(siteD_X, siteD_Y, test_size=0.2, random_state=42)
    st.header("Site D Model Performance:")
    st.write(f"R^2 Score: {siteD_model.score(siteD_X_test, siteD_Y_test):.4f}")

    siteD_prediction = pl.DataFrame(siteD_model.predict(predict_X))

    siteD_prediction = predict_X.with_columns([
        pl.Series("ED Enc", siteD_prediction[:, 0]),
        pl.Series("ED Enc Admitted", siteD_prediction[:, 1])
    ])

    st.dataframe(siteD_prediction.to_pandas().style.format({"Month": lambda x: nums_to_months[x], "Hour": lambda x: nums_to_hours[x], "Weekday": lambda x: nums_to_weekdays[x]}))
    st.bar_chart(data=siteD_prediction, x="Hour", y=["ED Enc", "ED Enc Admitted"], stack=False)
