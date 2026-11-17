class PredictionPipeline:
    def __init__(self):
        pass

    def predict(self, data: dict):
        # Simple rule-based scoring (temporary until we load a real model)
        score = 0.5

        if data.get("education_of_employee") in ["Master's", "Doctorate"]:
            score += 0.2
        elif data.get("education_of_employee") == "Bachelor's":
            score += 0.1

        if data.get("has_job_experience") == "Y":
            score += 0.15

        if data.get("continent") in ["Europe", "Asia"]:
            score += 0.05

        if data.get("no_of_employees", 0) > 1000:
            score += 0.05

        probability = min(max(score, 0.1), 0.95)
        status = "Certified" if probability >= 0.6 else "Denied"

        return {
            "status": status,
            "probability": round(probability, 2),
            "message": f"Predicted {status} with {round(probability*100)}% confidence"
        }
