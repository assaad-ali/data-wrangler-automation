import os
import streamlit as st
from modules.preprocessing.data_cleaning import DataCleaner
from modules.preprocessing.scaling import Scaler
from modules.preprocessing.encoding import Encoder
from modules.utils.logger import get_logger
from modules.services.dvc_service import DVCService

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
        st.title("⚙️ Data Preprocessing")

        # Initialize session state for df_processed and df_selected if not already set
        if 'df_processed' not in st.session_state:
            st.session_state['df_processed'] = df.copy()

        df_processed = st.session_state['df_processed']

        # Section to select columns for preprocessing
        st.header("Select Columns for Preprocessing")
        all_columns = df.columns.tolist()
        selected_columns = st.multiselect(
            "Select Columns to Include in Preprocessing", 
            all_columns, 
            default=all_columns,
            on_change=lambda: st.session_state.update({'df_selected': df_processed[selected_columns]})
        )

        if not selected_columns:
            st.warning("Please select at least one column to proceed.")
            return df_processed

        # Work with session state for df_selected
        if 'df_selected' not in st.session_state:
            st.session_state['df_selected'] = df_processed[selected_columns]

        df_selected = st.session_state['df_selected']

        # Initialize a flag to track if any preprocessing was performed
        preprocessing_performed = False
        # DVC Tracking Option
        st.header("DVC Tracking")
        track_with_dvc = st.checkbox("Track preprocessing with DVC?")
        if track_with_dvc:
            dvc_service = DVCService()
            dvc_service.initialize_dvc()

            # Option to configure remote
            st.subheader("DVC Remote Configuration")
            dvc_service.configure_remote()
        
        # Missing Value Handling
        st.header("Missing Value Handling")
        missing_value_handling = st.checkbox("Handle Missing Values?")
        if missing_value_handling:
            # Show missing value statistics
            st.subheader("Missing Value Statistics")
            missing_values = df_selected.isnull().sum()
            st.write(missing_values[missing_values > 0])

            # Select columns to impute
            cols_to_impute = st.multiselect(
                "Select Columns to Impute",
                df_selected.columns[df_selected.isnull().any()].tolist()
            )
            if cols_to_impute:
                # Separate strategies for numeric and categorical columns
                strategy_options = ['Select...','mean', 'median', 'most_frequent', 'constant', 'knn', 'iterative']
                strategy = st.selectbox("Select Imputation Strategy", strategy_options)
                fill_value = None

                if strategy == 'Select...':
                    st.warning("Please select an imputation strategy.")
                else:

                    if strategy == 'constant':
                        fill_value = st.text_input("Enter the constant value to fill missing values with", value='unknown')

                    # Use handle_missing_values from DataCleaner with caching to avoid re-running heavy logic
                    df_selected[cols_to_impute] = DataCleaner.handle_missing_values(
                        df_selected[cols_to_impute],
                        strategy=strategy,
                        fill_value=fill_value
                    )
                    st.success("Missing values imputed successfully.")
                    preprocessing_performed = True
                    st.session_state['df_selected'] = df_selected
            else:
                st.info("No columns selected for imputation.")

        # Remove Duplicates
        st.header("Duplicate Rows Handling")
        remove_duplicates = st.checkbox("Remove Duplicate Rows?")
        if remove_duplicates:
            before_shape = df_selected.shape
            df_selected = DataCleaner.remove_duplicates(df_selected)
            after_shape = df_selected.shape
            st.write(f"Duplicates removed. Data shape changed from {before_shape} to {after_shape}.")
            preprocessing_performed = True
            st.session_state['df_selected'] = df_selected

        # Outlier Handling
        st.header("Outlier Handling")
        outlier_handling = st.checkbox("Handle Outliers?")
        if outlier_handling:
            numeric_cols = df_selected.select_dtypes(include=['float64', 'int64']).columns.tolist()
            if numeric_cols:
                cols_to_handle_outliers = st.multiselect(
                    "Select Numerical Columns for Outlier Handling",
                    numeric_cols
                )
                if cols_to_handle_outliers:
                    method = st.selectbox("Select Outlier Detection Method", ['zscore', 'iqr', 'quantile'])
                    if method == 'zscore':
                        threshold = st.slider(
                            "Select Z-score Threshold",
                            min_value=1.0, max_value=5.0, value=3.0, step=0.1
                        )
                    elif method == 'iqr':
                        threshold = st.slider(
                            "Select IQR Multiplier",
                            min_value=1.0, max_value=3.0, value=1.5, step=0.1
                        )
                    elif method == 'quantile':
                        lower_quantile = st.slider(
                            "Select Lower Quantile",
                            min_value=0.0, max_value=0.5, value=0.05, step=0.01
                        )
                        upper_quantile = st.slider(
                            "Select Upper Quantile",
                            min_value=0.5, max_value=1.0, value=0.95, step=0.01
                        )
                        threshold = (lower_quantile, upper_quantile)
                    else:
                        threshold = None


                    # Visualize outliers before handling
                    st.subheader("Outliers Before Handling")
                    DataCleaner.visualize_outliers(df_selected[cols_to_handle_outliers])

                    df_selected[cols_to_handle_outliers] = DataCleaner.handle_outliers(
                        df_selected[cols_to_handle_outliers],
                        method=method,
                        threshold=threshold
                    )

                    # Visualize outliers after handling
                    st.subheader("Outliers After Handling")
                    DataCleaner.visualize_outliers(df_selected[cols_to_handle_outliers])

                    preprocessing_performed = True
                    st.session_state['df_selected'] = df_selected
                else:
                    st.info("No numerical columns selected for outlier handling.")
            else:
                st.info("No numerical columns available for outlier handling.")

        # Feature Scaling
        st.header("Feature Scaling")
        scaling = st.checkbox("Scale Features?")
        if scaling:
            numeric_cols = df_selected.select_dtypes(include=['float64', 'int64']).columns.tolist()
            if numeric_cols:
                # Select Scaling Method
                method = st.selectbox("Select Scaling Method", ['standard', 'minmax', 'robust', 'maxabs'])

                # Select Columns to Scale
                cols_to_scale = st.multiselect("Select Numerical Columns to Scale", numeric_cols)
                if cols_to_scale:
                    # Visualize distributions before scaling
                    st.subheader("Distributions Before Scaling")
                    Scaler.visualize_distributions(df_selected[cols_to_scale])

                    # Perform Scaling
                    df_selected[cols_to_scale] = Scaler.scale_features(
                        df_selected[cols_to_scale],
                        method=method
                    )

                    # Visualize distributions after scaling
                    st.subheader("Distributions After Scaling")
                    Scaler.visualize_distributions(df_selected[cols_to_scale])

                    preprocessing_performed = True
                    st.session_state['df_selected'] = df_selected
                else:
                    st.info("Please select at least one numerical column to scale.")
            else:
                st.info("No numerical columns available for scaling.")

        # Encoding Categorical Variables
        st.header("Encoding Categorical Variables")
        encoding = st.checkbox("Encode Categorical Variables?")
        if encoding:
            categorical_cols = df_selected.select_dtypes(include=['object', 'category']).columns.tolist()
            if categorical_cols:
                cols_to_encode = st.multiselect("Select Categorical Columns to Encode", categorical_cols)
                if cols_to_encode:
                    encoding_methods = ['label', 'onehot', 'ordinal', 'binary']
                    method = st.selectbox("Select Encoding Method", encoding_methods)
                    df_selected = Encoder.encode_features(df_selected, cols_to_encode, method=method)
                    preprocessing_performed = True
                    st.session_state['df_selected'] = df_selected
                else:
                    st.info("No categorical columns selected for encoding.")
            else:
                st.info("No categorical columns available for encoding.")

        # Add a button for the user to declare that preprocessing is complete
        finish_preprocessing = st.button("Finish Preprocessing")

        # Condition to check if preprocessing was performed and the user clicked the button
        if finish_preprocessing:
            if preprocessing_performed:
                st.success("Data preprocessing completed.")
                st.write("Preview of Preprocessed Data:")
                st.write(df_selected.head())

                if track_with_dvc:
                    # Save preprocessed data
                    preprocessed_dataset_path = os.path.join(dvc_service.data_dir, 'preprocessed_data.csv')
                    df_selected.to_csv(preprocessed_dataset_path, index=False)
                    # Add and commit dataset
                    dvc_service.add_and_commit_dataset(preprocessed_dataset_path, "Updated preprocessed data.")
                    # Option to push to remote
                    if st.button("Push DVC and Git changes to remote"):
                        dvc_service.push_changes()
                else:
                    st.info("DVC tracking not enabled.")

                # Return the processed DataFrame
                return df_selected
            else:
                st.info("No preprocessing actions were performed.")
                st.write("Preview of Original Data:")
                st.write(df_selected.head())

                # Return the DataFrame (even though it's unchanged)
                return df_selected
        else:
            st.info("Configure preprocessing options and click 'Finish Preprocessing' when done.")
            # Return the DataFrame (in its current state)
            return df_selected
