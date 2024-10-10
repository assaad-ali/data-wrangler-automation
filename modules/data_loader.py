# modules/data_access/data_loader.py

import pandas as pd
import streamlit as st
from sklearn import datasets
import os
import json
import logging
from ..utils.logger import get_logger
from ..utils.exceptions import DataLoaderException
from ...configs.config import DATA_DIRECTORY

logger = get_logger(__name__)

def load_user_dataset():
    """
    Allows the user to upload a dataset in various formats and returns a DataFrame.
    """
    uploaded_file = st.sidebar.file_uploader("Upload Your Dataset", type=['csv', 'xlsx', 'xls', 'json'])
    if uploaded_file is not None:
        file_name = uploaded_file.name
        file_extension = os.path.splitext(file_name)[1].lower()
        try:
            # Save the uploaded file to the data directory
            save_uploaded_file(uploaded_file)

            # Read the file into a DataFrame
            file_path = os.path.join(DATA_DIRECTORY, file_name)
            if file_extension == '.csv':
                df = pd.read_csv(file_path)
            elif file_extension in ['.xlsx', '.xls']:
                df = pd.read_excel(file_path)
            elif file_extension == '.json':
                df = pd.read_json(file_path)
            else:
                st.error("Unsupported file type.")
                raise DataLoaderException(f"Unsupported file type: {file_extension}")
            st.success("Dataset loaded successfully!")
            logger.info(f"User dataset '{file_name}' loaded successfully.")
            return df
        except Exception as e:
            st.error(f"Error loading dataset: {e}")
            logger.error(f"Error loading user dataset '{file_name}': {e}")
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
            'Boston Housing': datasets.load_boston,
            'California Housing': datasets.fetch_california_housing
        }

        if name not in data_loaders:
            st.error("Dataset not found.")
            raise DataLoaderException(f"Dataset '{name}' not found.")

        data = data_loaders[name]()
        if hasattr(data, 'data'):
            X = pd.DataFrame(data.data, columns=data.feature_names)
        else:
            X = pd.DataFrame(data['data'], columns=data['feature_names'])
        y = pd.Series(data.target, name='target')
        df = pd.concat([X, y], axis=1)
        st.success(f"{name} dataset loaded successfully!")
        logger.info(f"Built-in dataset '{name}' loaded successfully.")
        return df
    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        logger.error(f"Error loading built-in dataset '{name}': {e}")
        return None