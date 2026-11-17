import joblib
import pandas as pd

class PredictionPipeline:
    def __init__(self):
        try:
            self.model = joblib.load("model/visa_model.pkl")
            print("Model loaded successfully")
        except Exception as e:
            print(f"Could not load model: {e}")
            self.model = None

    def predict(self, data: dict):
        if self.model is None:
            return {"status": "Error", "probability": 0.0, "message": "Model not loaded"}

        # Build a one-row DataFrame with the expected columns
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
            "message": f"Predicted {status} with {round(proba*100)}% confidence"
        }
