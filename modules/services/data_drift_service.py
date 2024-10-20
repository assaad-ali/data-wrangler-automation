from evidently.report import Report
from evidently.metric_preset import DataDriftPreset
import streamlit as st

def detect_data_drift(reference_data, current_data):
    """
    Detect data drift between the reference dataset and the current dataset using Evidently.

    Parameters:
    - reference_data: Pandas DataFrame (reference dataset)
    - current_data: Pandas DataFrame (current dataset)

    Returns:
    - drift_detected: Dictionary containing data drift results
    - report: Evidently Report object containing detailed drift information
    """
    report = Report(metrics=[DataDriftPreset()])
    report.run(reference_data=reference_data, current_data=current_data)
    
    # Extract drift detection result
    drift_result = report.as_dict()
    dataset_drift = drift_result['metrics'][0]['result']['dataset_drift']
    drift_detected = dataset_drift

    return drift_detected, report

def display_drift_report(report):
    """
    Display the Evidently data drift report in Streamlit.

    Parameters:
    - report: Evidently Report object
    """
    st.subheader("Data Drift Report")
    # Generate the HTML report
    report_html = report.to_html()
    # Display the report in Streamlit
    st.components.v1.html(report_html, height=1000, scrolling=True)