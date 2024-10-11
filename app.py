# app.py

import streamlit as st
from modules.data_access.data_loader import load_user_dataset, load_builtin_dataset
from modules.utils.logger import get_logger
from modules.utils.exceptions import DataLoaderException

logger = get_logger(__name__)

def main():
    st.title("Machine Learning and Deep Learning App")
    st.write("Upload your dataset or select a built-in dataset to get started.")

    # Sidebar for dataset selection
    st.sidebar.header("Dataset Options")
    dataset_source = st.sidebar.radio("Select Dataset Source", ('Upload Your Own Dataset', 'Use Built-in Dataset'))

    if dataset_source == 'Upload Your Own Dataset':
        df = load_user_dataset()
        dataset_name = 'User Dataset'
    else:
        builtin_datasets = ['Iris', 'Wine', 'Breast Cancer', 'Diabetes', 'Boston Housing', 'California Housing']
        dataset_name = st.sidebar.selectbox("Select a Built-in Dataset", builtin_datasets)
        df = load_builtin_dataset(dataset_name)

    if df is not None:
        st.subheader("Dataset Preview")
        st.write(df.head())
        st.write(f"Dataset Shape: {df.shape}")
        if st.checkbox("Show Summary Statistics"):
            st.write(df.describe())
        if st.checkbox("Show Dataset Columns"):
            st.write(df.columns.tolist())

        # Proceed with further steps (e.g., preprocessing, modeling)
        # ...

    else:
        st.warning("No dataset loaded. Please upload a dataset or select a built-in one.")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        logger.error(f"Unexpected error: {e}")
