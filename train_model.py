"""
Run this once locally to train and save the model.
Requires: data/EasyVisa.csv in the project folder.
"""
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from lightgbm import LGBMClassifier
from sklearn.metrics import roc_auc_score

# Load data
df = pd.read_csv("data/EasyVisa.csv")
df["approved"] = df["case_status"].map({"Certified": 1, "Denied": 0})

num = ["no_of_employees", "yr_of_estab", "prevailing_wage"]
cat = ["education_of_employee", "has_job_experience", "continent",
       "region_of_employment", "unit_of_wage", "full_time_position",
       "requires_job_training"]

X = df[num + cat]
y = df["approved"]

pre = ColumnTransformer([
    ("num", "passthrough", num),
    ("cat", OneHotEncoder(handle_unknown="ignore"), cat)
])

pipe = Pipeline([
    ("pre", pre),
    ("model", LGBMClassifier(n_estimators=100, random_state=42, verbose=-1))
])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
pipe.fit(X_train, y_train)

auc = roc_auc_score(y_test, pipe.predict_proba(X_test)[:, 1])
print(f"Test ROC-AUC: {auc:.4f}")

# Save the full pipeline
joblib.dump(pipe, "model/visa_model.pkl")
print("Model saved to model/visa_model.pkl")
