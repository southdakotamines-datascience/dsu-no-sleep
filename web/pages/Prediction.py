import streamlit as st
import polars as pl
from sklearn.linear_model import LinearRegression

st.header("Predictions for a selected site")
st.set_page_config(
    page_title="Sanford Health/DSU Data Competition Visualizations",
    page_icon="😴"
)
