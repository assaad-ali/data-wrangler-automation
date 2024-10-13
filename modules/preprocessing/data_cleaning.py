import streamlit as st
from sklearn.impute import SimpleImputer, KNNImputer
from modules.utils.logger import get_logger
import seaborn as sns
import matplotlib.pyplot as plt

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

    @staticmethod
    def handle_outliers(df, method='zscore', threshold=3):
        """
        Handle outliers in the DataFrame.

        Parameters:
        - df: Pandas DataFrame
        - method: Method to detect outliers ('zscore', 'iqr')
        - threshold: Threshold for outlier detection

        Returns:
        - df_outliers_handled: DataFrame with outliers handled
        """
        try:
            numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
            if method == 'zscore':
                from scipy import stats
                z_scores = stats.zscore(df[numeric_cols])
                abs_z_scores = abs(z_scores)
                filtered_entries = (abs_z_scores < threshold).all(axis=1)
                df = df[filtered_entries]
            elif method == 'iqr':
                Q1 = df[numeric_cols].quantile(0.25)
                Q3 = df[numeric_cols].quantile(0.75)
                IQR = Q3 - Q1
                df = df[~((df[numeric_cols] < (Q1 - threshold * IQR)) | (df[numeric_cols] > (Q3 + threshold * IQR))).any(axis=1)]
            logger.info(f"Outliers handled using method: {method}")
            return df
        except Exception as e:
            logger.error(f"Error in handling outliers: {e}")
            st.error(f"Error in handling outliers: {e}")
            return df
    @staticmethod
    def visualize_outliers(df):
        for col in df.columns:
            fig, ax = plt.subplots()
            sns.boxplot(data=df, x=col, ax=ax)
            st.pyplot(fig)
