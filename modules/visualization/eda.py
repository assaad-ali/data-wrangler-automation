import streamlit as st
from modules.utils.logger import get_logger

logger = get_logger(__name__)

def data_overview(df):
    st.subheader("Data Overview")
    st.write(f"**Number of rows:** {df.shape[0]}")
    st.write(f"**Number of columns:** {df.shape[1]}")

    if st.checkbox("Show Data Types"):
        st.write(df.dtypes)

    if st.checkbox("Show Missing Values"):
        missing_values = df.isnull().sum()
        st.write(missing_values[missing_values > 0])

    if st.checkbox("Show Duplicate Rows"):
        duplicate_rows = df.duplicated().sum()
        st.write(f"Number of duplicate rows: {duplicate_rows}")
