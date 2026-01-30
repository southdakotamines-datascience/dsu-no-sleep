import streamlit as st
import polars as pl
import os

cwd = os.getcwd()

reasons = pl.read_csv(os.path.join(cwd, "reasons.csv")).sort("Count of appearances", descending=True)

st.header("Popularity of Visit Reasons (for fun)")

st.dataframe(reasons)
st.bar_chart(reasons, x="REASON_VISIT_NAME", y="Total ED Enc", horizontal=True, sort="-Total ED Enc")