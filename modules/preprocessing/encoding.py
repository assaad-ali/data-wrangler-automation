import pandas as pd
import streamlit as st
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from modules.utils.logger import get_logger

logger = get_logger(__name__)

class Encoder:
    @staticmethod
    def encode_features(df, method='label'):
        """
        Encode categorical features in the DataFrame.

        Parameters:
        - df: Pandas DataFrame
        - method: Encoding method ('label', 'onehot')

        Returns:
        - df_encoded: DataFrame with encoded features
        """
        try:
            # Copy DataFrame to avoid modifying original data
            df_encoded = df.copy()
            categorical_cols = df.select_dtypes(include=['object', 'category']).columns

            if method == 'label':
                # Use LabelEncoder from sklearn
                label_encoder = LabelEncoder()
                for col in categorical_cols:
                    # Ensure consistent label encoding across columns
                    df_encoded[col] = label_encoder.fit_transform(df_encoded[col].astype(str))
            elif method == 'onehot':
                # Use OneHotEncoder from sklearn 
                one_hot_encoder = OneHotEncoder(sparse=False, drop='first')
                encoded_cols = one_hot_encoder.fit_transform(df_encoded[categorical_cols])
                encoded_df = pd.DataFrame(encoded_cols, columns=one_hot_encoder.get_feature_names_out(categorical_cols))
                df_encoded = df_encoded.drop(columns=categorical_cols).join(encoded_df)
            else:
                st.error("Unsupported encoding method.")
                return df

            logger.info(f"Categorical features encoded using method: {method}")
            return df_encoded
        except Exception as e:
            logger.error(f"Error in encoding features: {e}")
            st.error(f"Error in encoding features: {e}")
            return df
