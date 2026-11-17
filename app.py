from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from visa.pipeline.prediction_pipeline import PredictionPipeline

app = FastAPI(title="Global Mobility Application Analyzer")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict", response_class=HTMLResponse)
def predict(
    request: Request,
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
    return templates.TemplateResponse(
        "result.html",
        {"request": request, "result": result, "data": data}
    )
