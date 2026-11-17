from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from visa.pipeline.prediction_pipeline import PredictionPipeline

app = FastAPI(title="Global Mobility Application Analyzer")
pipeline = PredictionPipeline()

FORM_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Visa Approval Predictor</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 650px; margin: 40px auto; padding: 20px; }
        input, select, button { width: 100%; padding: 10px; margin: 6px 0; box-sizing: border-box; }
        button { background: #0066cc; color: white; border: none; cursor: pointer; font-size: 16px; }
        button:hover { background: #004999; }
        label { font-weight: bold; margin-top: 10px; display: block; }
    </style>
</head>
<body>
    <h2>Visa Approval Prediction</h2>
    <form action="/predict" method="post">
        <label>Education of Employee</label>
        <select name="education" required>
            <option value="High School">High School</option>
            <option value="Bachelor's" selected>Bachelor's</option>
            <option value="Master's">Master's</option>
            <option value="Doctorate">Doctorate</option>
        </select>

        <label>Has Job Experience</label>
        <select name="experience" required>
            <option value="Y" selected>Yes</option>
            <option value="N">No</option>
        </select>

        <label>Continent</label>
        <select name="continent" required>
            <option value="Asia" selected>Asia</option>
            <option value="Europe">Europe</option>
            <option value="North America">North America</option>
            <option value="South America">South America</option>
            <option value="Africa">Africa</option>
            <option value="Oceania">Oceania</option>
        </select>

        <label>Region of Employment</label>
        <select name="region" required>
            <option value="Northeast" selected>Northeast</option>
            <option value="South">South</option>
            <option value="West">West</option>
            <option value="Midwest">Midwest</option>
            <option value="Island">Island</option>
        </select>

        <label>Unit of Wage</label>
        <select name="unit" required>
            <option value="Year" selected>Year</option>
            <option value="Hour">Hour</option>
            <option value="Week">Week</option>
            <option value="Month">Month</option>
        </select>

        <label>Full Time Position</label>
        <select name="full_time" required>
            <option value="Y" selected>Yes</option>
            <option value="N">No</option>
        </select>

        <label>Requires Job Training</label>
        <select name="training" required>
            <option value="N" selected>No</option>
            <option value="Y">Yes</option>
        </select>

        <label>Number of Employees</label>
        <input type="number" name="employees" value="500" required>

        <label>Year of Establishment</label>
        <input type="number" name="year" value="2010" required>

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
    region: str = Form(...),
    unit: str = Form(...),
    full_time: str = Form(...),
    training: str = Form(...),
    employees: int = Form(...),
    year: int = Form(...),
    wage: float = Form(...)
):
    data = {
        "education_of_employee": education,
        "has_job_experience": experience,
        "continent": continent,
        "region_of_employment": region,
        "unit_of_wage": unit,
        "full_time_position": full_time,
        "requires_job_training": training,
        "no_of_employees": employees,
        "yr_of_estab": year,
        "prevailing_wage": wage
    }
    result = pipeline.predict(data)

    color = "#d4edda" if result["status"] == "Certified" else "#f8d7da"
    text_color = "#155724" if result["status"] == "Certified" else "#721c24"

    return f"""
    <html>
    <body style="font-family: Arial; max-width: 650px; margin: 40px auto; padding: 20px;">
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
