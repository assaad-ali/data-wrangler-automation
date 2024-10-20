import streamlit as st
from sklearn.impute import SimpleImputer, KNNImputer
from modules.utils.logger import get_logger
import seaborn as sns
import matplotlib.pyplot as plt

logger = get_logger(__name__)

class DataCleaner:
    @staticmethod
    @st.cache_data
    def handle_missing_values(df, strategy, fill_value):
        """
        Handle missing values separately for numeric and categorical columns.

        Parameters:
        - df: Pandas DataFrame
        - strategy: Strategy for numeric imputation ('mean', 'median', 'knn', 'iterative') 
                    and categorical imputation ('most_frequent', 'constant').
        - fill_value: Value to replace missing values with when strategy='constant' (for categorical columns).

        Returns:
        - df_cleaned: DataFrame with missing values handled
        """
        try:
            # Separate numeric and categorical columns
            numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
            categorical_cols = df.select_dtypes(include=['object', 'category']).columns

            # Handle numerical columns with numeric strategies
            if not numeric_cols.empty:

                if strategy in ['mean', 'median', 'knn', 'iterative']:
                    if numeric_cols.empty:
                        st.error("No numeric columns available for the selected imputation strategy.")
                        return df

                    if df[numeric_cols].isnull().sum().sum() == 0:
                        st.error("No missing values found in the selected numeric columns.")
                        return df

                    if strategy == 'knn':
                        # Apply KNN Imputation for numeric columns
                        imputer = KNNImputer()
                        df[numeric_cols] = imputer.fit_transform(df[numeric_cols])

                    elif strategy == 'iterative':
                        # Apply Iterative Imputation for numeric columns
                        imputer = IterativeImputer()
                        df[numeric_cols] = imputer.fit_transform(df[numeric_cols])

                    else:
                        # Apply SimpleImputer for 'mean' and 'median' strategies
                        num_imputer = SimpleImputer(strategy=strategy)
                        df[numeric_cols] = num_imputer.fit_transform(df[numeric_cols])

            # Handle categorical columns with categorical strategies
            if not categorical_cols.empty:

                if strategy in ['most_frequent', 'constant']:
                    if categorical_cols.empty:
                        st.error("No categorical columns available for the selected imputation strategy.")
                        return df

                    if df[categorical_cols].isnull().sum().sum() == 0:
                        st.error("No missing values found in the selected categorical columns.")
                        return df

                    # Apply 'most_frequent' or 'constant' for categorical columns
                    cat_imputer = SimpleImputer(strategy=strategy, fill_value=fill_value)
                    df[categorical_cols] = cat_imputer.fit_transform(df[categorical_cols])

            logger.info(f"Missing values handled using strategy: {strategy} and fill_value: {fill_value}")
            return df

        except Exception as e:
            logger.error(f"Error in handling missing values: {e}")
            st.error(f"Error in handling missing values: {e}")
            return df

    @staticmethod
    @st.cache_data
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
    @st.cache_data
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
    @st.cache_data
    def visualize_outliers(df):
        for col in df.columns:
            fig, ax = plt.subplots()
            sns.boxplot(data=df, x=col, ax=ax)
            st.pyplot(fig)
