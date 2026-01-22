import streamlit as st
import polars as pl

reasons = pl.read_csv("../reasons.csv").sort("Count of appearances", descending=True)

st.header("Popularity of Visit Reasons")

st.dataframe(reasons)