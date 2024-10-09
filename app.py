import streamlit as st
from modules.data_loader import load_user_dataset, load_builtin_dataset

def main():
    st.title("Machine Learning and Deep Learning App")
    st.write("Upload your dataset or select a built-in dataset to get started.")

    # Sidebar for dataset selection
    st.sidebar.header("Dataset Options")
    dataset_source = st.sidebar.radio("Select Dataset Source", ('Upload Your Own Dataset', 'Use Built-in Dataset'))

    if dataset_source == 'Upload Your Own Dataset':
        df = load_user_dataset()
    else:
        builtin_datasets = ['Iris', 'Wine', 'Breast Cancer', 'Diabetes', 'California Housing']
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

if __name__ == '__main__':
    main()
