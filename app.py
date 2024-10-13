import streamlit as st
from modules.data_access.data_loader import load_user_dataset, load_builtin_dataset
from modules.utils.logger import get_logger
from modules.visualization import eda
from modules.services.preprocessing_service import PreprocessingService

logger = get_logger(__name__)

def main():
    st.title("Data Wrangling App")
    st.markdown("""
        This app allows you to:
        - Upload or select a built-in dataset
        - Perform Exploratory Data Analysis (EDA)
        - Preprocess your data before modeling
    """)

    # Sidebar for dataset selection
    st.sidebar.header("📂 Dataset Options")
    dataset_source = st.sidebar.radio("Select Dataset Source", ('Upload Your Own Dataset', 'Use Built-in Dataset'))

    if dataset_source == 'Upload Your Own Dataset':
        df = load_user_dataset()
        dataset_name = 'User Dataset'
    else:
        builtin_datasets = ['Iris', 'Wine', 'Breast Cancer', 'Diabetes', 'California Housing']
        dataset_name = st.sidebar.selectbox("Select a Built-in Dataset", builtin_datasets)
        df = load_builtin_dataset(dataset_name)
    
    if df is not None:

        # Radio button in the sidebar for selecting between EDA and Preprocessing
        process_choice = st.sidebar.radio("Choose a Task", ["🔍 Exploratory Data Analysis", "⚙️ Data Preprocessing"])

        col1, col2, col3, col4= st.columns([4, 1, 1, 1])

        # Subheader in the first column with more space
        col1.subheader(f"📊 {dataset_name} Dataset Preview")

        # Button for showing the head of the dataset
        if col2.button("Head", key="preview_head"):
            st.write(df.head())

        # Button for showing the tail of the dataset
        if col3.button("Tail", key="preview_tail"):
            st.write(df.tail())

        # Button for showing a random sample from the dataset
        if col4.button("Random", key="preview_sample"):
            st.write(df.sample(5))
        
        st.write(f"Dataset Shape: {df.shape}")

        # Store the DataFrame in session state for later use
        st.session_state['df'] = df

        # Conditional rendering based on radio button choice
        if process_choice == "🔍 Exploratory Data Analysis":
            with st.spinner("Loading EDA..."):
                eda.run_eda(df)

        elif process_choice == "⚙️ Data Preprocessing":
            # Data Preprocessing
            df_preprocessed = PreprocessingService.preprocess_data(df)

            # Update the DataFrame in session state
            st.session_state['df_preprocessed'] = df_preprocessed


    else:
        st.warning("No dataset loaded. Please upload a dataset or select a built-in one.")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        logger.error(f"Unexpected error: {e}")
