import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from ml_model.feature_extraction import FEATURE_NAMES, extract_features_from_dict


class DataPreprocessor:
    """Preprocesses raw profile datasets and transforms them for machine learning."""

    def __init__(self):
        self.scaler = StandardScaler()
        self.is_fitted = False

    def process_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Validates columns and engineers features for each row in the DataFrame.
        """
        processed_rows = []
        for _, row in df.iterrows():
            feat_dict = extract_features_from_dict(row.to_dict())
            if 'is_fake' in row:
                feat_dict['is_fake'] = int(row['is_fake'])
            processed_rows.append(feat_dict)
        return pd.DataFrame(processed_rows)

    def fit_transform(self, X: np.ndarray) -> np.ndarray:
        """Fits the StandardScaler on training data and transforms it."""
        self.is_fitted = True
        return self.scaler.fit_transform(X)

    def transform(self, X: np.ndarray) -> np.ndarray:
        """Transforms input feature array using the fitted scaler."""
        if not self.is_fitted:
            raise ValueError("DataPreprocessor scaler has not been fitted yet.")
        return self.scaler.transform(X)
