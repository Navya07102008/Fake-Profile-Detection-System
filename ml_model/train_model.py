import sys
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
from sklearn.preprocessing import StandardScaler

from ml_model.feature_extraction import FEATURE_NAMES, extract_features_from_dict

DATASET_PATH = BASE_DIR / 'dataset' / 'processed' / 'cleaned_profiles.csv'
MODELS_DIR = BASE_DIR / 'ml_model' / 'models'
RESULTS_DIR = BASE_DIR / 'ml_model' / 'results'

MODELS_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def load_and_prepare_data():
    df = pd.read_csv(DATASET_PATH)
    rows = []
    targets = []
    for _, row in df.iterrows():
        feat = extract_features_from_dict(row.to_dict())
        rows.append([feat[k] for k in FEATURE_NAMES])
        targets.append(int(row['is_fake']))
    return np.array(rows), np.array(targets)


def train():
    print("Loading dataset from:", DATASET_PATH)
    X, y = load_and_prepare_data()
    print(f"Dataset shape: {X.shape}, Authentic: {np.sum(y == 0)}, Fake: {np.sum(y == 1)}")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    # Fit scaler
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Train Random Forest
    rf = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        min_samples_split=4,
        random_state=42,
        class_weight='balanced',
        n_jobs=-1
    )
    rf.fit(X_train_scaled, y_train)

    # Cross validation
    cv_scores = cross_val_score(rf, X_train_scaled, y_train, cv=5, scoring='f1')

    # Evaluation
    y_pred = rf.predict(X_test_scaled)
    y_proba = rf.predict_proba(X_test_scaled)[:, 1]

    acc = float(accuracy_score(y_test, y_pred))
    prec = float(precision_score(y_test, y_pred))
    rec = float(recall_score(y_test, y_pred))
    f1 = float(f1_score(y_test, y_pred))
    auc = float(roc_auc_score(y_test, y_proba))
    cm = confusion_matrix(y_test, y_pred).tolist()

    feature_importances = {
        name: round(float(imp), 4)
        for name, imp in sorted(
            zip(FEATURE_NAMES, rf.feature_importances_),
            key=lambda x: x[1],
            reverse=True
        )
    }

    metrics = {
        "accuracy": round(acc, 4),
        "precision": round(prec, 4),
        "recall": round(rec, 4),
        "f1_score": round(f1, 4),
        "roc_auc": round(auc, 4),
        "cv_f1_mean": round(float(np.mean(cv_scores)), 4),
        "confusion_matrix": {
            "true_negative": cm[0][0],
            "false_positive": cm[0][1],
            "false_negative": cm[1][0],
            "true_positive": cm[1][1]
        },
        "feature_importances": feature_importances,
        "sample_count": len(y),
        "train_samples": len(y_train),
        "test_samples": len(y_test)
    }

    model_file = MODELS_DIR / 'fake_profile_rf.joblib'
    scaler_file = MODELS_DIR / 'scaler.joblib'
    joblib.dump(rf, model_file)
    joblib.dump(scaler, scaler_file)
    print(f"Model saved to: {model_file}")
    print(f"Scaler saved to: {scaler_file}")

    metrics_file = RESULTS_DIR / 'evaluation_metrics.json'
    with open(metrics_file, 'w', encoding='utf-8') as f:
        json.dump(metrics, f, indent=2)
    print(f"Metrics saved to: {metrics_file}")

    print("\n--- Model Training Summary ---")
    print(f"Accuracy:  {acc*100:.2f}%")
    print(f"Precision: {prec*100:.2f}%")
    print(f"Recall:    {rec*100:.2f}%")
    print(f"F1 Score:  {f1*100:.2f}%")
    print(f"ROC-AUC:   {auc*100:.2f}%")
    print(f"CV F1:     {np.mean(cv_scores)*100:.2f}%")
    return metrics


if __name__ == '__main__':
    train()
