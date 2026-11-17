import pandas as pd
import joblib
import os
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from lightgbm import LGBMClassifier

class PredictionPipeline:
    def __init__(self):
        self.model = None
        model_path = "model/visa_model.pkl"

        if os.path.exists(model_path):
            try:
                self.model = joblib.load(model_path)
                print("Loaded saved model")
            except Exception as e:
                print(f"Failed to load model: {e}")

        if self.model is None:
            print("No saved model found. Building a simple in-memory model...")
            self.model = self._build_simple_model()

    def _build_simple_model(self):
        # Tiny synthetic training data so the app works out of the box
        data = {
            "no_of_employees": [100, 500, 2000, 50, 1000, 300, 5000, 200],
            "yr_of_estab": [2000, 2010, 1995, 2015, 2005, 2018, 1990, 2012],
            "prevailing_wage": [50000, 80000, 120000, 40000, 90000, 70000, 150000, 60000],
            "education_of_employee": ["Bachelor's", "Master's", "Doctorate", "High School", "Bachelor's", "Master's", "Doctorate", "Bachelor's"],
            "has_job_experience": ["Y", "Y", "Y", "N", "Y", "N", "Y", "Y"],
            "continent": ["Asia", "Europe", "Asia", "Africa", "North America", "Asia", "Europe", "Asia"],
            "region_of_employment": ["Northeast", "South", "West", "Midwest", "Northeast", "South", "West", "Island"],
            "unit_of_wage": ["Year", "Year", "Year", "Hour", "Year", "Year", "Year", "Year"],
            "full_time_position": ["Y", "Y", "Y", "N", "Y", "Y", "Y", "Y"],
            "requires_job_training": ["N", "N", "Y", "N", "N", "Y", "N", "N"],
            "approved": [1, 1, 1, 0, 1, 0, 1, 1]
        }
        df = pd.DataFrame(data)

        num = ["no_of_employees", "yr_of_estab", "prevailing_wage"]
        cat = ["education_of_employee", "has_job_experience", "continent",
               "region_of_employment", "unit_of_wage", "full_time_position",
               "requires_job_training"]

        pre = ColumnTransformer([
            ("num", "passthrough", num),
            ("cat", OneHotEncoder(handle_unknown="ignore"), cat)
        ])

        pipe = Pipeline([
            ("pre", pre),
            ("model", LGBMClassifier(n_estimators=50, random_state=42, verbose=-1))
        ])

        pipe.fit(df[num + cat], df["approved"])
        return pipe

    def predict(self, data: dict):
        if self.model is None:
            return {"status": "Error", "probability": 0.0, "message": "Model not available"}

        row = {
            "no_of_employees": data.get("no_of_employees", 500),
            "yr_of_estab": data.get("yr_of_estab", 2010),
            "prevailing_wage": data.get("prevailing_wage", 80000),
            "education_of_employee": data.get("education_of_employee", "Bachelor's"),
            "has_job_experience": data.get("has_job_experience", "Y"),
            "continent": data.get("continent", "Asia"),
            "region_of_employment": data.get("region_of_employment", "Northeast"),
            "unit_of_wage": data.get("unit_of_wage", "Year"),
            "full_time_position": data.get("full_time_position", "Y"),
            "requires_job_training": data.get("requires_job_training", "N")
        }
        df = pd.DataFrame([row])

        proba = self.model.predict_proba(df)[0, 1]
        status = "Certified" if proba >= 0.5 else "Denied"

        return {
            "status": status,
            "probability": round(float(proba), 2),
            "message": f"Predicted {status} with {round(proba * 100)}% confidence"
        }
