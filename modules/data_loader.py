import pandas as pd
import streamlit as st
from sklearn import datasets


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

def load_builtin_dataset(name):
    """
    Loads a built-in dataset from scikit-learn by name and returns a DataFrame.
    """
    try:
        data_loaders = {
            'Iris': datasets.load_iris,
            'Wine': datasets.load_wine,
            'Breast Cancer': datasets.load_breast_cancer,
            'Diabetes': datasets.load_diabetes,
            'California Housing': datasets.fetch_california_housing
        }

        if name not in data_loaders:
            st.error("Dataset not found.")
            return None

        data = data_loaders[name]()
        if hasattr(data, 'data'):
            X = pd.DataFrame(data.data, columns=data.feature_names)
        else:
            X = pd.DataFrame(data['data'], columns=data['feature_names'])
        y = pd.Series(data.target, name='target')
        df = pd.concat([X, y], axis=1)
        st.success(f"{name} dataset loaded successfully!")
        return df
    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        return None
