# Global Mobility Application Analyzer

End-to-end Machine Learning pipeline to predict US visa approval (Certified / Denied) using the EasyVisa dataset.

## Project Structure

```
visa/
├── components/          # data_ingestion, validation, transformation, model_trainer, etc.
├── pipeline/             # training_pipeline.py, prediction_pipeline.py
├── entity/               # config_entity.py, artifact_entity.py
├── configuration/        # MongoDB & AWS connections
├── cloud_storage/        # AWS S3 helpers
├── constants/
├── utils/
├── logger/
└── exception/
config/
app.py                     # FastAPI application
demo.py
Dockerfile
requirements.txt
setup.py
```

## Quick Start (local)

```bash
# Using the existing UV venv
uv pip install -r requirements.txt
python demo.py
```

## Full Production Flow
- Data from MongoDB
- Validation → Transformation → Model Training (KNN / RF / XGBoost)
- Evaluation & Model Pusher to S3
- FastAPI serving + Docker + GitHub Actions CI/CD to EC2

Dataset: EasyVisa (https://www.kaggle.com/datasets/moro23/easyvisa-dataset)
