# **Data Wrangler Automation**

## **Introduction**

This project is a **Streamlit-based application** to automate tasks of data wrangling, preprocessing, and exploratory data analysis (EDA). The app allows users to upload datasets or select from built-in datasets for analysis, and then apply preprocessing techniques to clean and transform the data for machine learning (ML) model development.


## Features

- **Dataset Upload and Selection**
  - Upload your own dataset in CSV, Excel, or JSON format.
  - Choose from built-in datasets: Iris, Wine, Breast Cancer, Diabetes, and California Housing.

- **Exploratory Data Analysis (EDA)**
  - **Data Overview**: View dataset shape, data types, missing values, and duplicate rows.
  - **Statistical Summaries**: Get descriptive statistics for numerical and categorical features.
  - **Data Visualization**: Generate histograms, box plots, correlation matrices, scatter plots, pair plots, and categorical vs numerical analyses.
  - **Data Filtering**: Filter data based on numerical ranges, categorical values, date ranges, or string patterns.

- **Data Preprocessing**
  - **Handle Missing Values**: Impute missing values using strategies like mean, median, most frequent, constant, KNN, or iterative imputation.
  - **Handle Outliers**: Detect and handle outliers using methods like Z-score, IQR, or quantile-based methods.
  - **Remove Duplicates**: Identify and remove duplicate rows from the dataset.
  - **Feature Scaling**: Scale numerical features using StandardScaler, MinMaxScaler, RobustScaler, or MaxAbsScaler.
  - **Encode Categorical Variables**: Encode categorical features using label encoding or one-hot encoding.
  - **Data Version Control**: Track preprocessing steps using DVC with options to configure remote storage.

- **Data Drift Detection**
  - Detect data drift between reference and current datasets using the Evidently library.
  - Visualize data drift reports within the app.

- **DVC Integration**
  - Initialize and configure DVC directly from the app.
  - Add and commit datasets to DVC tracking.
  - Configure remote storage with S3 or Google Drive.
  - Push changes to remote repositories.
  

## **Project Structure**

```
data-wrangler-automation/
├── app.py                
├── requirements.txt      
├── README.md             
├── configs/
│   └── config.py
├── modules/
│   ├── data_access/
│   │   └── data_loader.py
│   ├── preprocessing/
│   │   ├── data_cleaning.py
│   │   ├── encoding.py
│   │   └── scaling.py
│   ├── services/
│   │   ├── dvc_service.py
│   │   └── preprocessing_service.py
│   ├── utils/
│   │   ├── dvc_utils.py
│   │   └── logger.py
│   └── visualization/
│       └── eda.py

```


## Installation

### Prerequisites

#### **External Tools**
    - [Git](https://git-scm.com/downloads)
    - [DVC](https://dvc.org/doc/install)
    - Python 3.7 or higher
    - pip package manager


### Clone the Repository

```bash
git clone <https://github.com/assaad-ali/data-wrangler-automation.git>
cd data-wrangling-app
```

### Create a Virtual Environment

It's recommended to use a virtual environment to manage dependencies.

```bash
python -m venv venv
# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the root directory to store environment variables like `MONGODB_URI`:

```env
MONGODB_URI=your_mongodb_connection_string
```

## **How to Use**

### Running the App

```bash
streamlit run app.py
```

This will start the Streamlit app, and you can access it in your web browser at `http://localhost:8501`.

### Using the App

1. **Dataset Selection**
   - In the sidebar, choose to upload your own dataset or select a built-in dataset.
   - If uploading, select your dataset file (CSV, Excel, or JSON).
   - If using a built-in dataset, select one from the dropdown menu.

2. **Data Preview**
   - View a preview of your dataset (head, tail, or random sample).
   - See the dataset shape and basic information.

3. **Task Selection**
   - Choose between **Exploratory Data Analysis** and **Data Preprocessing** from the sidebar.

4. **Exploratory Data Analysis**
   - **Data Overview**: Get insights into data types, missing values, and duplicates.
   - **Statistical Summaries**: View descriptive statistics.
   - **Visualizations**: Generate various plots to understand data distributions and relationships.
   - **Data Filtering**: Apply filters to focus on specific subsets of data.

5. **Data Preprocessing**
   - **Select Columns**: Choose which columns to include in preprocessing.
   - **Handle Missing Values**: Impute missing values with various strategies.
   - **Handle Outliers**: Detect and handle outliers using Z-score, IQR, or quantile methods.
   - **Remove Duplicates**: Eliminate duplicate rows.
   - **Feature Scaling**: Scale numerical features.
   - **Encode Categorical Variables**: Convert categorical data into numerical formats.
   - **DVC Tracking**: Optionally track preprocessing steps using DVC.

6. **Data Drift Detection**
   - Use the Evidently library to detect and visualize data drift between different datasets.

7. **DVC Integration**
   - Initialize DVC and Git repositories directly from the app.
   - Configure remote storage options (S3 or Google Drive).
   - Add, commit, and push changes to remote repositories.


## Logging

Logs are saved in the `logs` directory as specified in `configs/config.py`. Logging is configured in `modules/utils/logger.py`.


## **Contributing**

Contributions are welcome! Here's how you can help:

1. Fork the repository

2. Create a new branch 
    ```bash
    git checkout -b feature/my-feature`
    ```
3. Make your changes and commit them 
    ```bash
        git commit -m 'Add some feature'`
    ```
4. Push to the branch 
    ```bash
    git push origin feature/my-feature`
    ```
5. Create a Pull Request


## **Contact**

For any questions or suggestions, feel free to open an issue or [reach out](mailto:assaad.n.ali@gmail.com) via email.


---