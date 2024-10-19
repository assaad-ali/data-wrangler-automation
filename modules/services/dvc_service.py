# modules/services/dvc_service.py

import os
from modules.utils import dvc_utils
from modules.utils.logger import get_logger
import streamlit as st

logger = get_logger(__name__)

class DVCService:
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        self.ensure_data_directory()

    def ensure_data_directory(self):
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            logger.info(f"Data directory created at {self.data_dir}")

    def initialize_dvc(self):
        if not dvc_utils.check_git_initialized():
            if dvc_utils.git_init() == 0:
                logger.info("Git initialized.")
            else:
                logger.error("Failed to initialize Git.")
        else:
            logger.info("Git is already initialized.")

        if not dvc_utils.check_dvc_initialized():
            if dvc_utils.dvc_init() == 0:
                logger.info("DVC initialized.")
            else:
                logger.error("Failed to initialize DVC.")
        else:
            logger.info("DVC is already initialized.")

    def add_and_commit_dataset(self, dataset_path, message):
        if dvc_utils.dvc_add(dataset_path) == 0:
            logger.info(f"Dataset {dataset_path} added to DVC tracking.")
            if dvc_utils.git_add(f"{dataset_path}.dvc") == 0:
                logger.info("DVC files added to Git staging area.")
                if dvc_utils.git_commit(message) == 0:
                    logger.info(f"Changes committed with message: {message}")
                else:
                    logger.error("Failed to commit changes.")
            else:
                logger.error("Failed to add DVC files to Git.")
        else:
            logger.error(f"Failed to add dataset {dataset_path} to DVC.")

    def push_changes(self):
        if dvc_utils.git_push() == 0:
            logger.info("Git changes pushed to remote.")
        else:
            logger.error("Failed to push Git changes.")
        if dvc_utils.dvc_push() == 0:
            logger.info("DVC data pushed to remote.")
        else:
            logger.error("Failed to push DVC data.")

    def configure_remote(self):
        st.header("Configure DVC Remote Storage")
        remote_name = st.text_input("Enter remote name", value="myremote")
        remote_type = st.selectbox("Select remote type", ["S3", "Google Drive"])
        
        if remote_type == "S3":
            bucket_name = st.text_input("Enter S3 bucket name")
            region = st.text_input("Enter S3 bucket region", value="us-east-1")
            if st.button("Configure S3 Remote"):
                if remote_name and bucket_name and region:
                    if not dvc_utils.check_s3_configured(remote_name):
                        dvc_utils.configure_s3_remote(remote_name, bucket_name, region)
                        st.success(f"S3 remote '{remote_name}' configured.")
                    else:
                        st.info(f"S3 remote '{remote_name}' is already configured.")
                else:
                    st.error("Please provide remote name, bucket name, and region.")
        elif remote_type == "Google Drive":
            folder_id = st.text_input("Enter Google Drive folder ID")
            client_id = st.text_input("Enter Google Drive client ID")
            client_secret = st.text_input("Enter Google Drive client secret", type="password")
            if st.button("Configure Google Drive Remote"):
                if remote_name and folder_id:
                    if not dvc_utils.check_gdrive_configured(remote_name):
                        dvc_utils.setup_gdrive_remote(remote_name, folder_id)
                        if client_id and client_secret:
                            dvc_utils.modify_gdrive_remote(remote_name, client_id, client_secret)
                        st.success(f"Google Drive remote '{remote_name}' configured.")
                    else:
                        st.info(f"Google Drive remote '{remote_name}' is already configured.")
                else:
                    st.error("Please provide remote name and folder ID.")