from fastapi import APIRouter
from backend.models.patient import PatientBase
from backend.models.ml_schemas import PredictionResponse, ExplainResponse
from backend.controllers import ml_controller

router = APIRouter(
    prefix="/ml",
    tags=["Machine Learning Analysis"]
)

@router.post("/hospitalization/predict", response_model=PredictionResponse)
def predict_hospitalization(patient: PatientBase):
    return ml_controller.predict_hosp(patient)

@router.post("/hospitalization/explain", response_model=ExplainResponse)
def explain_hospitalization(patient: PatientBase):
    return ml_controller.explain_hosp(patient)

@router.post("/complications/predict", response_model=PredictionResponse)
def predict_bed_days(patient: PatientBase):
    return ml_controller.predict_comp(patient)

@router.post("/complications/explain", response_model=ExplainResponse)
def explain_bed_days(patient: PatientBase):
    return ml_controller.explain_comp(patient)