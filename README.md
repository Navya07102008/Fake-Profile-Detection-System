# 🛡️ Fake Profile Detection System (Hybrid AI + Semantic Web Ontology)

A comprehensive, enterprise-grade cybersecurity web application that detects fraudulent, cloned, and automated social media accounts by fusing **Machine Learning (Random Forest)** with **Deterministic Semantic Web Ontology Reasoning (W3C OWL 2 / RDFLib)**.

---

## 🌟 Key Highlights & Architecture

- **Dual-Engine Fusion:**
  - **Machine Learning (55% influence by default):** Scikit-Learn `RandomForestClassifier` trained on 18 engineered features (ratios, engagement rates, activity velocity, handle digit density).
  - **Ontology Semantic Reasoner (45% influence by default):** W3C OWL 2 RDF-XML ontology parsed and inferred using `rdflib`. Evaluates 7 formal forensic rules to infer concept taxonomy (`BotSpammerProfile`, `GhostLurkerProfile`, `VerifiedAuthorityProfile`, etc.).
- **Multi-Tier Risk Assessment:** Classifies profiles into **Low Risk** (0-34), **Medium Risk** (35-69), and **High Risk** (70-100) with explainable reasoning (XAI).
- **Forensic PDF Audit Reports:** Instant on-demand generation of cybersecurity audit certificates with ReportLab.
- **Modern Cyber UI:** Dark navy, electric blue, cyber purple, and emerald aesthetic built on Bootstrap 5 and Chart.js.
- **1-Click Benchmark Personas:** Pre-loaded profiles (Obvious Spam Bot, Verified Authority, Ghost Lurker, Follower Farm) for instant testing.

---

## 🏗️ Project Structure

```text
Fake_Profile_Detection_System/
├── README.md
├── requirements.txt
├── .env
├── manage.py
├── ontology/
│   ├── fake_profile_ontology.owl
│   ├── classes.txt
│   ├── properties.txt
│   ├── individuals.txt
│   └── ontology_documentation.md
├── dataset/
│   ├── generate_dataset.py
│   ├── raw/profiles.csv
│   ├── processed/cleaned_profiles.csv
│   └── sample/test_profiles.csv
├── ml_model/
│   ├── __init__.py
│   ├── preprocessing.py
│   ├── feature_extraction.py
│   ├── train_model.py
│   ├── evaluate_model.py
│   ├── predict.py
│   ├── models/
│   │   ├── fake_profile_rf.joblib
│   │   └── scaler.joblib
│   └── results/
│       ├── evaluation_metrics.json
│       └── evaluation_report.json
├── backend/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── templates/          # All 14 HTML templates
│   └── detector/
│       ├── __init__.py
│       ├── admin.py
│       ├── apps.py
│       ├── models.py
│       ├── views.py
│       ├── urls.py
│       ├── forms.py
│       ├── detector.py     # Hybrid ML + Ontology Detection Engine
│       └── utils.py
├── frontend/
│   ├── css/style.css
│   └── js/main.js
├── database/
│   ├── db.sqlite3
│   └── seed_data.py
├── ontology_engine/
│   ├── __init__.py
│   ├── ontology_loader.py
│   ├── profile_mapper.py
│   ├── rule_engine.py
│   └── reasoner.py
├── reports/
│   ├── __init__.py
│   └── detection_report.py
└── tests/
    ├── test_detection.py
    ├── test_features.py
    ├── test_ontology.py
    └── test_views.py
```

---

## 🚀 Setup & Execution Guide

### 1. Activate Virtual Environment
```powershell
# On Windows (PowerShell)
.\myvenv\Scripts\Activate.ps1
```

### 2. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 3. Generate Dataset & Train Machine Learning Model
```powershell
# Generate realistic datasets (2,500 records)
python dataset/generate_dataset.py

# Train Random Forest classifier and output metrics
python ml_model/train_model.py

# Run evaluation report
python ml_model/evaluate_model.py
```

### 4. Database Setup & Initial Seeding
```powershell
# Run database migrations
python manage.py makemigrations detector
python manage.py migrate

# Seed database with default admin user and benchmark sample analyses
python database/seed_data.py
```

**Default Credentials:**
- **Username:** `admin`
- **Password:** `admin123`

### 5. Run the Server
```powershell
python manage.py runserver
```
Visit the application in your browser at: **`http://127.0.0.1:8000/`**

---

## 🧪 Running Automated Tests

Run the complete 18-test unit and integration suite:
```powershell
python manage.py test tests
```
The test suite validates:
- Feature extraction calculations and zero-division resilience (`tests/test_features.py`)
- OWL ontology parsing and semantic rule triggering (`tests/test_ontology.py`)
- Hybrid ML + Ontology weighting and scoring (`tests/test_detection.py`)
- All 14 Django view controllers, authentication, and ReportLab PDF downloads (`tests/test_views.py`)

---

## 📋 Complete Application Modules & Views

| URL Route | Module / View | Description |
|---|---|---|
| `/` | **Home** | Landing page with hero banner, tech stack overview, and pipeline diagram |
| `/login/` | **Login** | Secure authentication portal |
| `/register/` | **Register** | New security analyst registration |
| `/dashboard/` | **Dashboard** | KPI cards, Chart.js threat distributions, and recent audit table |
| `/analyze/` | **Profile Analysis** | Input form with 1-click benchmark persona loaders and live feature preview |
| `/result/<id>/` | **Detection Result** | Main detection verdict, circular risk gauge meter, and flagged evidence |
| `/features/<id>/` | **Feature Extraction** | Detailed breakdown of raw vs. engineered mathematical feature vectors |
| `/analysis-details/<id>/` | **ML & Ontology Analysis** | Comparative side-by-side view of Random Forest probability vs OWL reasoning |
| `/risk-assessment/<id>/` | **Risk Assessment** | Multi-tier Low/Medium/High matrix and tactical defensive response protocols |
| `/history/` | **Detection History** | Searchable and filterable archive of past audits with PDF downloads |
| `/analytics/` | **Analytics Hub** | Chart.js visualizations: threat distributions, feature importance, ROC-AUC |
| `/reports/<id>/` | **Audit Reports** | Web view of official cybersecurity audit certificate |
| `/reports/pdf/<id>/` | **PDF Generation** | Instant ReportLab PDF download with audit watermark |
| `/ontology-visual/` | **Ontology Visualizer** | Interactive visual representation of OWL classes, properties, and Protégé import |
| `/settings/` | **Engine Settings** | Threshold tuning sliders (ML vs Ontology weights, risk cut-offs) |

---

## ⚖️ Forensic Intelligence Disclaimer

This system is an automated risk assessment tool synthesizing machine learning probability with semantic web heuristics. Probabilistic scores and rule violations represent indicators of suspicion and do not constitute definitive legal proof of fraudulent identity or malicious impersonation.
