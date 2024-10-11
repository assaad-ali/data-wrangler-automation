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

def plot_histograms(df):
    st.subheader("Histograms of Numerical Features")
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    selected_cols = st.multiselect("Select Numerical Columns for Histograms", numeric_cols)
    bins = st.slider("Number of Bins", min_value=5, max_value=100, value=30)

    for col in selected_cols:
        fig = px.histogram(df, x=col, nbins=bins, title=f'Histogram of {col}')
        st.plotly_chart(fig)

def statistical_summaries(df):
    st.subheader("Statistical Summaries")

    # Select columns
    columns = st.multiselect("Select Columns", df.columns.tolist(), default=df.columns.tolist())

    # Numerical features
    numeric_cols = [col for col in columns if is_numeric_dtype(df[col])]
    if numeric_cols:
        if st.checkbox("Show Numerical Features Summary"):
            st.write(df[numeric_cols].describe().T)
    else:
        st.write("No numerical features selected.")

    # Categorical features
    categorical_cols = [col for col in columns if is_categorical_dtype(df[col]) or df[col].dtype == 'object']
    if categorical_cols:
        if st.checkbox("Show Categorical Features Summary"):
            for col in categorical_cols:
                st.write(f"**{col}**")
                st.write(df[col].value_counts())
    else:
        st.write("No categorical features selected.")

def plot_histograms(df):
    st.subheader("Histograms of Numerical Features")
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    selected_cols = st.multiselect("Select Numerical Columns for Histograms", numeric_cols)
    bins = st.slider("Number of Bins", min_value=5, max_value=100, value=30)

    for col in selected_cols:
        fig = px.histogram(df, x=col, nbins=bins, title=f'Histogram of {col}')
        st.plotly_chart(fig)
