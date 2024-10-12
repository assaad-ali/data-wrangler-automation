import streamlit as st
from modules.preprocessing.data_cleaning import DataCleaner
from modules.preprocessing.scaling import Scaler
from modules.preprocessing.encoding import Encoder
from modules.utils.logger import get_logger

logger = get_logger(__name__)

class PreprocessingService:
    @staticmethod
    def preprocess_data(df):
        """
        Manage the data preprocessing steps.

        Parameters:
        - df: Pandas DataFrame

        Returns:
        - df_preprocessed: Preprocessed DataFrame
        """
        st.header("Data Preprocessing")

        # Missing Value Handling
        st.subheader("Missing Value Handling")
        missing_value_handling = st.checkbox("Handle Missing Values?")
        if missing_value_handling:
            strategy = st.selectbox("Select Imputation Strategy", ['mean', 'median', 'most_frequent', 'constant', 'knn'])
            fill_value = None
            if strategy == 'constant':
                fill_value = st.text_input("Enter the constant value to fill missing values with", value=0)
            df = DataCleaner.handle_missing_values(df, strategy=strategy, fill_value=fill_value)

        # Remove Duplicates
        remove_duplicates = st.checkbox("Remove Duplicate Rows?")
        if remove_duplicates:
            df = DataCleaner.remove_duplicates(df)

        # Outlier Handling
        st.subheader("Outlier Handling")
        outlier_handling = st.checkbox("Handle Outliers?")
        if outlier_handling:
            method = st.selectbox("Select Outlier Detection Method", ['zscore', 'iqr'])
            threshold = st.slider("Select Threshold", min_value=1.0, max_value=5.0, value=3.0)
            df = DataCleaner.handle_outliers(df, method=method, threshold=threshold)

        # Feature Scaling
        st.subheader("Feature Scaling")
        scaling = st.checkbox("Scale Features?")
        if scaling:
            method = st.selectbox("Select Scaling Method", ['standard', 'minmax', 'robust'])
            df = Scaler.scale_features(df, method=method)

        # Encoding Categorical Variables
        st.subheader("Encoding Categorical Variables")
        encoding = st.checkbox("Encode Categorical Variables?")
        if encoding:
            method = st.selectbox("Select Encoding Method", ['label', 'onehot'])
            df = Encoder.encode_features(df, method=method)

        st.success("Data preprocessing completed.")
        st.write("Preview of Preprocessed Data:")
        st.write(df.head())

        return df
