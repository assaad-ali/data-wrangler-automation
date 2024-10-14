# **Data Wrangler Automation**

## **Introduction**

This project is a **Streamlit-based application** designed to automate various steps of data wrangling, preprocessing, and exploratory data analysis (EDA). The app allows users to upload datasets or select built-in datasets for analysis, and then apply a variety of preprocessing techniques to clean and transform the data for machine learning (ML) model development.

Key features include:
- **Data Ingestion**: Support for user-uploaded datasets in various formats and built-in datasets.
- **EDA**: Perform interactive data exploration, filtering, and visualize missing values, distributions, and correlations.
- **Data Preprocessing**: Handle missing values, remove duplicates, detect outliers, apply feature scaling, and encode categorical variables.

This project is suitable for data scientists and ML engineers looking to streamline their data preparation workflows.

---

## **Installation**

1. Clone the repository:

```bash
git clone https://github.com/assaad-ali/data-wrangler-automation.git
```

2. Navigate to the project directory:

```bash
cd data-wrangler-automation
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

4. Run the Streamlit app:

```bash
streamlit run app.py
```

---

## **How to Use**

### **1. Data Ingestion**

- **Upload a Dataset**: You can upload your own dataset in `.csv`, `.xls`, `.xlsx`, or `.json` formats.
- **Use a Built-in Dataset**: Select from preloaded datasets like Iris, Wine, Breast Cancer, Diabetes, and California Housing.

### **2. Exploratory Data Analysis (EDA)**

- **Data Preview**: View a preview of your dataset's head, tail, and random samples.
- **Visualizations**:
  - Histograms, Box Plots, Scatter Plots, and Correlation Matrix.
  - Explore relationships between categorical and numerical features.
  - Visualize missing data with heatmaps.

### **3. Data Preprocessing**

- **Handle Missing Values**: Choose from various imputation strategies such as mean, median, most frequent, and more.
- **Remove Duplicates**: Automatically remove duplicate rows.
- **Handle Outliers**: Detect and handle outliers using Z-score, IQR, or quantiles.
- **Feature Scaling**: Apply standard scaling, min-max scaling, robust scaling, or max-abs scaling.
- **Encode Categorical Variables**: Label encode or one-hot encode categorical features.

### **4. Finishing Preprocessing**

Once preprocessing is complete, the app will display a preview of the preprocessed data. You can then download the dataset and proceed to further steps in your data science workflow, such as feature engineering or model building.

---

## **Contributing**

Contributions are welcome! Here's how you can help:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/my-feature`).
3. Make your changes and commit them (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/my-feature`).
5. Create a Pull Request.

---

## **Contact**

For any questions or suggestions, please feel free to open an issue or reach out at [assaad.n.ali@gmail.com]

---