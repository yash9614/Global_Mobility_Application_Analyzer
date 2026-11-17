from fastapi import FastAPI
from visa.pipeline.prediction_pipeline import PredictionPipeline

app = FastAPI(title="Global Mobility Application Analyzer")

@app.get("/")
def home():
    return {"message": "Visa Approval Prediction API is running"}

@app.post("/predict")
def predict(data: dict):
    pipeline = PredictionPipeline()
    result = pipeline.predict(data)
    return {"prediction": result}
