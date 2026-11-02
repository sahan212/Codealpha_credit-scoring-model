import os
import joblib
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

MODEL_FILE = os.path.join(os.path.dirname(__file__), 'credit_model.joblib')
CANDIDATE_DATASETS = [
    os.path.join(os.path.dirname(__file__), '..', 'finance.csv'),
    '/Users/pranithreddy/Desktop/sahan/finance.csv'
]

class CreditFeatureEngineer(BaseEstimator, TransformerMixin):
    """Safely calculates debt_to_income and loan_to_income ratios."""
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()
        income = X['annual_income'].replace(0, np.nan)
        X['debt_to_income'] = (X['total_debt'] / income).fillna(0)
        X['loan_to_income'] = (X['loan_amount'] / income).fillna(0)
        return X

def get_or_train_model():
    if os.path.exists(MODEL_FILE):
        print(f"[+] Loaded existing model from {MODEL_FILE}")
        return joblib.load(MODEL_FILE)

    # Locate dataset
    dataset_path = None
    for p in CANDIDATE_DATASETS:
        if os.path.exists(p):
            dataset_path = p
            break

    if not dataset_path:
        raise FileNotFoundError("Could not find finance.csv in credit-app or /Desktop/sahan/.")

    print(f"[+] Training model from dataset: {dataset_path} ...")
    df = pd.read_csv(dataset_path, sep=None, engine='python')
    if 'customer_id' in df.columns:
        df = df.drop(columns=['customer_id'])

    X = df.drop(columns=['default'])
    y = df['default']

    cat_cols = ['education', 'home_ownership']
    num_cols = [c for c in X.columns if c not in cat_cols] + ['debt_to_income', 'loan_to_income']

    num_pipeline = Pipeline([('imputer', SimpleImputer(strategy='median'))])
    cat_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('encoder', OneHotEncoder(drop='first', handle_unknown='ignore', sparse_output=False))
    ])

    preprocessor = ColumnTransformer([
        ('num', num_pipeline, num_cols),
        ('cat', cat_pipeline, cat_cols)
    ])

    pipeline = Pipeline([
        ('engineer', CreditFeatureEngineer()),
        ('preprocessor', preprocessor),
        ('clf', RandomForestClassifier(n_estimators=150, max_depth=6, class_weight='balanced', random_state=42))
    ])

    pipeline.fit(X, y)
    joblib.dump(pipeline, MODEL_FILE)
    print(f"[✓] Model trained and cached to {MODEL_FILE}")
    return pipeline

def predict_applicant(applicant_dict: dict, model, risk_threshold: float = 0.40) -> dict:
    df_applicant = pd.DataFrame([applicant_dict])
    prob_default = float(model.predict_proba(df_applicant)[0, 1])

    income = applicant_dict.get('annual_income', 0)
    dti = round(applicant_dict.get('total_debt', 0) / income, 2) if income > 0 else 0
    lti = round(applicant_dict.get('loan_amount', 0) / income, 2) if income > 0 else 0

    is_approved = prob_default < risk_threshold

    # Explainability factors
    factors = []
    if dti > 0.45:
        factors.append(f"High Debt-to-Income ({dti:.2f} > 0.45)")
    else:
        factors.append(f"Healthy Debt-to-Income ({dti:.2f})")

    if applicant_dict.get('credit_utilization', 0) > 0.50:
        factors.append(f"Elevated Credit Utilization ({applicant_dict['credit_utilization']*100:.0f}%)")

    late_12m = applicant_dict.get('late_payments_12m', 0)
    if late_12m > 1:
        factors.append(f"{late_12m} Late payments in the past 12 months")
    elif late_12m == 0:
        factors.append("Clean 12-month payment record")

    if prob_default < 0.20:
        risk_level = "Low Risk (Preferred)"
    elif prob_default < 0.40:
        risk_level = "Moderate Risk (Standard)"
    else:
        risk_level = "High Risk (Subprime / Elevated)"

    return {
        "verdict": "APPROVED" if is_approved else "REJECTED",
        "is_creditworthy": is_approved,
        "risk_score_pct": round(prob_default * 100, 1),
        "debt_to_income": dti,
        "loan_to_income": lti,
        "risk_level": risk_level,
        "key_factors": factors
    }
