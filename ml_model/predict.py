from pathlib import Path
import joblib
import numpy as np
from ml_model.feature_extraction import FEATURE_NAMES, extract_feature_vector, extract_features_from_dict

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / 'ml_model' / 'models' / 'fake_profile_rf.joblib'
SCALER_PATH = BASE_DIR / 'ml_model' / 'models' / 'scaler.joblib'


class ProfilePredictor:
    """Predicts fake vs authentic probability for a given profile."""

    _instance = None
    _model = None
    _scaler = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ProfilePredictor, cls).__new__(cls)
            cls._instance._load_model()
        return cls._instance

    def _load_model(self):
        if MODEL_PATH.exists() and SCALER_PATH.exists():
            try:
                self._model = joblib.load(MODEL_PATH)
                self._scaler = joblib.load(SCALER_PATH)
            except Exception:
                self._model = None
                self._scaler = None
        else:
            self._model = None
            self._scaler = None

    def reload(self):
        """Forces reloading the model and scaler from disk."""
        self._load_model()

    def predict_profile(self, profile_data: dict) -> dict:
        """
        Runs ML prediction on profile dictionary.
        Returns:
            - prediction: 'Fake' or 'Authentic'
            - fake_probability: float (0.0 to 1.0)
            - confidence_percentage: float (0.0 to 100.0)
            - feature_importances: dict mapping feature name to importance score
            - extracted_features: dict of raw and engineered features
        """
        extracted = extract_features_from_dict(profile_data)
        feat_vector = np.array([extracted[k] for k in FEATURE_NAMES]).reshape(1, -1)

        if self._model is not None and self._scaler is not None:
            scaled_vec = self._scaler.transform(feat_vector)
            probabilities = self._model.predict_proba(scaled_vec)[0]
            # Class 1 is 'Fake', Class 0 is 'Authentic'
            fake_prob = float(probabilities[1]) if len(probabilities) > 1 else float(probabilities[0])
            pred_class = 'Fake' if fake_prob >= 0.5 else 'Authentic'
            confidence = (fake_prob if pred_class == 'Fake' else (1.0 - fake_prob)) * 100.0

            # Feature importances
            importances = {}
            if hasattr(self._model, 'feature_importances_'):
                for name, imp in zip(FEATURE_NAMES, self._model.feature_importances_):
                    importances[name] = round(float(imp), 4)
        else:
            # Calibrated baseline statistical heuristic if model hasn't been trained yet
            f_ratio = extracted['follower_following_ratio']
            age = extracted['account_age_days']
            has_pic = extracted['has_profile_pic']
            verified = extracted['is_verified']
            engagement = extracted['engagement_rate']

            risk_points = 0.0
            if f_ratio < 0.05:
                risk_points += 0.35
            if not has_pic:
                risk_points += 0.25
            if age < 14:
                risk_points += 0.25
            if verified:
                risk_points -= 0.40
            if engagement < 0.01 and extracted['followers_count'] > 5000:
                risk_points += 0.25

            fake_prob = max(0.02, min(0.98, 0.25 + risk_points))
            pred_class = 'Fake' if fake_prob >= 0.5 else 'Authentic'
            confidence = (fake_prob if pred_class == 'Fake' else (1.0 - fake_prob)) * 100.0
            importances = {name: round(1.0 / len(FEATURE_NAMES), 4) for name in FEATURE_NAMES}

        return {
            'prediction': pred_class,
            'fake_probability': round(fake_prob, 4),
            'confidence_percentage': round(confidence, 2),
            'feature_importances': importances,
            'extracted_features': extracted,
        }
