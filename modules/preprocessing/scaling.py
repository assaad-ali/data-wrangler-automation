import streamlit as st
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from modules.utils.logger import get_logger

logger = get_logger(__name__)

class Scaler:
    @staticmethod
    def scale_features(df, method='standard'):
        """
        Scale numerical features in the DataFrame.

        Parameters:
        - df: Pandas DataFrame
        - method: Scaling method ('standard', 'minmax', 'robust')

        Returns:
        - df_scaled: DataFrame with scaled features
        """
        try:
            numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
            scaler = None

            if method == 'standard':
                scaler = StandardScaler()
            elif method == 'minmax':
                scaler = MinMaxScaler()
            elif method == 'robust':
                scaler = RobustScaler()
            else:
                st.error("Unsupported scaling method.")
                return df

            df[numeric_cols] = scaler.fit_transform(df[numeric_cols])
            logger.info(f"Features scaled using method: {method}")
            return df
        except Exception as e:
            logger.error(f"Error in scaling features: {e}")
            st.error(f"Error in scaling features: {e}")
            return df
