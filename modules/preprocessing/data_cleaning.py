import streamlit as st
from sklearn.impute import SimpleImputer, KNNImputer
from modules.utils.logger import get_logger

logger = get_logger(__name__)

class DataCleaner:
    @staticmethod
    def handle_missing_values(df, strategy='mean', fill_value=None):
        """
        Handle missing values in the DataFrame.

        Parameters:
        - df: Pandas DataFrame
        - strategy: Strategy for imputation ('mean', 'median', 'most_frequent', 'constant', 'knn')
        - fill_value: Value to replace missing values with when strategy='constant'

        Returns:
        - df_cleaned: DataFrame with missing values handled
        """
        try:
            numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
            categorical_cols = df.select_dtypes(include=['object', 'category']).columns

            if strategy == 'knn':
                imputer = KNNImputer()
                df[numeric_cols] = imputer.fit_transform(df[numeric_cols])
            else:
                # For numeric columns
                num_imputer = SimpleImputer(strategy=strategy, fill_value=fill_value)
                df[numeric_cols] = num_imputer.fit_transform(df[numeric_cols])

                # For categorical columns
                cat_imputer = SimpleImputer(strategy='most_frequent', fill_value=fill_value)
                df[categorical_cols] = cat_imputer.fit_transform(df[categorical_cols])

            logger.info(f"Missing values handled using strategy: {strategy}")
            return df
        except Exception as e:
            logger.error(f"Error in handling missing values: {e}")
            st.error(f"Error in handling missing values: {e}")
            return df

    @staticmethod
    def remove_duplicates(df):
        """
        Remove duplicate rows from the DataFrame.

        Parameters:
        - df: Pandas DataFrame

        Returns:
        - df_deduped: DataFrame without duplicate rows
        """
        try:
            initial_shape = df.shape
            df = df.drop_duplicates()
            final_shape = df.shape
            logger.info(f"Removed duplicates. Shape changed from {initial_shape} to {final_shape}.")
            return df
        except Exception as e:
            logger.error(f"Error in removing duplicates: {e}")
            st.error(f"Error in removing duplicates: {e}")
            return df
