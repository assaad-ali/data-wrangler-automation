import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.api.types import (
    is_numeric_dtype,
    is_datetime64_any_dtype,
    is_string_dtype,
)
from pandas import CategoricalDtype
import plotly.express as px
import streamlit as st
import time
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
    categorical_cols = [col for col in columns if isinstance(df[col].dtype, CategoricalDtype) or df[col].dtype == 'object']
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

def plot_box_plots(df):
    st.subheader("Box Plots of Numerical Features")
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    selected_cols = st.multiselect("Select Numerical Columns for Box Plots", numeric_cols)

    for col in selected_cols:
        fig = px.box(df, y=col, title=f'Box Plot of {col}')
        st.plotly_chart(fig)

def plot_correlation_matrix(df):
    st.subheader("Correlation Matrix Heatmap")
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    if numeric_cols:
        selected_cols = st.multiselect("Select Numerical Columns for Correlation Matrix", numeric_cols, default=numeric_cols)
        if len(selected_cols) >= 2:
            corr_matrix = df[selected_cols].corr()
            fig = plt.figure(figsize=(10, 8))
            sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f')
            st.pyplot(fig)
        else:
            st.write("Select at least two numerical columns.")
    else:
        st.write("No numerical features available for correlation matrix.")

def plot_scatter_plots(df):
    st.subheader("Scatter Plots")
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    if len(numeric_cols) >= 2:
        x_axis = st.selectbox("Select X-axis", numeric_cols)
        y_axis = st.selectbox("Select Y-axis", numeric_cols, index=1)
        color_col = st.selectbox("Select Color Column (Optional)", [None] + df.columns.tolist())
        fig = px.scatter(df, x=x_axis, y=y_axis, color=color_col, title=f'Scatter Plot of {y_axis} vs {x_axis}')
        st.plotly_chart(fig)
    else:
        st.write("Not enough numerical features to create scatter plots.")

def plot_pair_plots(df):
    st.subheader("Pair Plot")
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    selected_cols = st.multiselect("Select Numerical Columns for Pair Plot", numeric_cols, default=numeric_cols)
    if len(selected_cols) >= 2:
        fig = sns.pairplot(df[selected_cols])
        st.pyplot(fig)
    else:
        st.write("Select at least two numerical columns.")

def categorical_vs_numerical(df):
    st.subheader("Categorical vs Numerical Analysis")
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    if categorical_cols and numeric_cols:
        cat_col = st.selectbox("Select Categorical Feature", categorical_cols)
        num_col = st.selectbox("Select Numerical Feature", numeric_cols)
        plot_type = st.selectbox("Select Plot Type", ['Box Plot', 'Violin Plot'])
        if plot_type == 'Box Plot':
            fig = px.box(df, x=cat_col, y=num_col, title=f'{num_col} Distribution across {cat_col}')
        else:
            fig = px.violin(df, x=cat_col, y=num_col, box=True, title=f'{num_col} Distribution across {cat_col}')
        st.plotly_chart(fig)
    else:
        st.write("Insufficient categorical or numerical features for this analysis.")

def plot_missing_values(df):
    st.subheader("Missing Data Heatmap")
    if df.isnull().sum().sum() > 0:
        fig = plt.figure(figsize=(10, 6))
        sns.heatmap(df.isnull(), cbar=False, cmap='viridis')
        st.pyplot(fig)
    else:
        st.write("No missing values in the dataset.")



def data_filtering(df):
    st.subheader("Data Filtering")

    # Allow the user to select columns to filter
    filter_columns = st.multiselect("Select Columns to Filter", df.columns.tolist())

    if not filter_columns:
        st.info("Please select at least one column to filter.")
        return df

    # Initialize a dictionary to hold filter conditions
    filter_conditions = {}

    for col in filter_columns:
        if is_numeric_dtype(df[col]):
            st.write(f"**Filtering options for numeric column:** `{col}`")
            min_val = float(df[col].min())
            max_val = float(df[col].max())
            step = (max_val - min_val) / 100 if max_val != min_val else 1.0
            # Add slider for numeric columns
            values = st.slider(
                f"Select range for `{col}`",
                min_value=min_val,
                max_value=max_val,
                value=(min_val, max_val),
                step=step,
            )
            filter_conditions[col] = df[col].between(values[0], values[1])

        elif is_datetime64_any_dtype(df[col]):
            st.write(f"**Filtering options for datetime column:** `{col}`")
            min_date = df[col].min()
            max_date = df[col].max()
            # Add date input for datetime columns
            values = st.date_input(
                f"Select date range for `{col}`",
                [min_date.date(), max_date.date()],
                min_value=min_date.date(),
                max_value=max_date.date(),
            )
            if len(values) == 2:
                start_date = pd.to_datetime(values[0])
                end_date = pd.to_datetime(values[1])
                filter_conditions[col] = df[col].between(start_date, end_date)

        elif isinstance(df[col].dtype, CategoricalDtype):
            st.write(f"**Filtering options for categorical column:** `{col}`")
            # Add multiselect for categorical columns
            options = st.multiselect(f"Select values for `{col}`", df[col].unique())
            if options:
                filter_conditions[col] = df[col].isin(options)

        elif is_string_dtype(df[col]):
            st.write(f"**Filtering options for string column:** `{col}`")
            filter_option = st.selectbox(
                f"Select filter type for `{col}`",
                ["Contains", "Starts with", "Ends with", "Exact match", "Regex"],
            )
            filter_value = st.text_input(f"Enter text to filter `{col}`")

            if filter_value:
                if filter_option == "Contains":
                    filter_conditions[col] = df[col].str.contains(filter_value, na=False, case=False)
                elif filter_option == "Starts with":
                    filter_conditions[col] = df[col].str.startswith(filter_value, na=False)
                elif filter_option == "Ends with":
                    filter_conditions[col] = df[col].str.endswith(filter_value, na=False)
                elif filter_option == "Exact match":
                    filter_conditions[col] = df[col] == filter_value
                elif filter_option == "Regex":
                    filter_conditions[col] = df[col].str.match(filter_value, na=False)
        else:
            st.warning(f"Column `{col}` has an unsupported data type and will be ignored.")

    # Apply all filter conditions
    if filter_conditions:
        filtered_df = df.copy()
        for col, condition in filter_conditions.items():
            filtered_df = filtered_df[condition]
        st.write(f"Total rows after filtering: {len(filtered_df)}")
        return filtered_df
    else:
        st.write("No filters applied.")
        return df
