from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from visa.pipeline.prediction_pipeline import PredictionPipeline

app = FastAPI(title="Global Mobility Application Analyzer")

FORM_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Visa Approval Predictor</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 600px; margin: 40px auto; padding: 20px; }
        input, select, button { width: 100%; padding: 10px; margin: 8px 0; box-sizing: border-box; }
        button { background: #0066cc; color: white; border: none; cursor: pointer; }
        button:hover { background: #004999; }
    </style>
</head>
<body>
    <h2>Visa Approval Prediction</h2>
    <form action="/predict" method="post">
        <label>Education</label>
        <select name="education" required>
            <option value="High School">High School</option>
            <option value="Bachelor's">Bachelor's</option>
            <option value="Master's">Master's</option>
            <option value="Doctorate">Doctorate</option>
        </select>

        <label>Job Experience</label>
        <select name="experience" required>
            <option value="Y">Yes</option>
            <option value="N">No</option>
        </select>

        <label>Continent</label>
        <select name="continent" required>
            <option value="Asia">Asia</option>
            <option value="Europe">Europe</option>
            <option value="North America">North America</option>
            <option value="South America">South America</option>
            <option value="Africa">Africa</option>
            <option value="Oceania">Oceania</option>
        </select>

        <label>Number of Employees</label>
        <input type="number" name="employees" value="500" required>

        <label>Prevailing Wage</label>
        <input type="number" name="wage" step="0.01" value="80000" required>

        <button type="submit">Predict</button>
    </form>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def home():
    return FORM_HTML

@app.post("/predict", response_class=HTMLResponse)
def predict(
    education: str = Form(...),
    experience: str = Form(...),
    continent: str = Form(...),
    employees: int = Form(...),
    wage: float = Form(...)
):
    data = {
        "education_of_employee": education,
        "has_job_experience": experience,
        "continent": continent,
        "no_of_employees": employees,
        "prevailing_wage": wage
    }
    pipeline = PredictionPipeline()
    result = pipeline.predict(data)

    color = "#d4edda" if result["status"] == "Certified" else "#f8d7da"
    text_color = "#155724" if result["status"] == "Certified" else "#721c24"

    return f"""
    <html>
    <body style="font-family: Arial; max-width: 600px; margin: 40px auto;">
        <h2>Prediction Result</h2>
        <div style="background: {color}; color: {text_color}; padding: 20px; border-radius: 8px;">
            <h3>{result["message"]}</h3>
            <p><strong>Status:</strong> {result["status"]}</p>
            <p><strong>Probability:</strong> {result["probability"]}</p>
        </div>
        <p><a href="/">← Try another prediction</a></p>
    </body>
    </html>
    """
