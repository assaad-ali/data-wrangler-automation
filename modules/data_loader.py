import pandas as pd
import streamlit as st


def load_user_dataset():
    """
    Allows the user to upload a dataset in various formats and returns a DataFrame.
    """
    uploaded_file = st.sidebar.file_uploader("Upload Your Dataset", type=['csv', 'xlsx', 'xls', 'json'])
    if uploaded_file is not None:
        file_type = uploaded_file.type
        try:
            if file_type == 'text/csv':
                df = pd.read_csv(uploaded_file)
            elif file_type in ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/vnd.ms-excel']:
                df = pd.read_excel(uploaded_file)
            elif file_type == 'application/json':
                df = pd.read_json(uploaded_file)
            else:
                st.error("Unsupported file type.")
                return None
            st.success("Dataset loaded successfully!")
            return df
        except Exception as e:
            st.error(f"Error loading dataset: {e}")
            return None
    else:
        st.info("Awaiting file upload.")
        return None