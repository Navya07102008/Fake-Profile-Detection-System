import sys
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import joblib
import pandas as pd
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score

from ml_model.feature_extraction import FEATURE_NAMES, extract_features_from_dict

MODEL_PATH = BASE_DIR / 'ml_model' / 'models' / 'fake_profile_rf.joblib'
SCALER_PATH = BASE_DIR / 'ml_model' / 'models' / 'scaler.joblib'
DATASET_PATH = BASE_DIR / 'dataset' / 'processed' / 'cleaned_profiles.csv'
RESULTS_DIR = BASE_DIR / 'ml_model' / 'results'


def evaluate():
    if not MODEL_PATH.exists() or not SCALER_PATH.exists():
        print("Model or scaler not found. Please train the model first.")
        return

    rf = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    df = pd.read_csv(DATASET_PATH)

    rows = []
    targets = []
    for _, row in df.iterrows():
        feat = extract_features_from_dict(row.to_dict())
        rows.append([feat[k] for k in FEATURE_NAMES])
        targets.append(int(row['is_fake']))

    X = np.array(rows)
    y = np.array(targets)
    X_scaled = scaler.transform(X)

    y_pred = rf.predict(X_scaled)
    y_proba = rf.predict_proba(X_scaled)[:, 1]

    report = classification_report(y, y_pred, target_names=['Authentic', 'Fake'], output_dict=True)
    cm = confusion_matrix(y, y_pred)
    roc_auc = float(roc_auc_score(y, y_proba))

    summary = {
        "classification_report": report,
        "confusion_matrix": cm.tolist(),
        "roc_auc": round(roc_auc, 4),
        "total_evaluated": len(y)
    }

    eval_file = RESULTS_DIR / 'evaluation_report.json'
    with open(eval_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)

    print("\n================ CLASSIFICATION REPORT ================")
    print(classification_report(y, y_pred, target_names=['Authentic', 'Fake']))
    print("Confusion Matrix:\n", cm)
    print(f"ROC-AUC: {roc_auc:.4f}")
    print(f"Report saved to: {eval_file}")
    return summary


if __name__ == '__main__':
    evaluate()
