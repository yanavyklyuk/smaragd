from fastapi import HTTPException
from backend.services.ml_service import ml_service
from backend.models.patient import PatientBase
from backend.models.ml_schemas import PredictionResponse, ExplainResponse

def _handle_prediction(predict_func, patient: PatientBase, labels: list):
    result = predict_func(patient)
    if result is None:
        raise HTTPException(status_code=500, detail="ML Model not loaded correctly")

    pred_class, prob = result

    msg = labels[pred_class] if pred_class < len(labels) else "Unknown status"

    return PredictionResponse(
        prediction=pred_class,
        probability=prob,
        message=msg
    )

def predict_hosp(patient: PatientBase):
    return _handle_prediction(
        ml_service.predict_hospitalization,
        patient,
        labels=["Низький ризик подовженої госпіталізації", "Високий ризик подовженої госпіталізації"]
    )


def explain_hosp(patient: PatientBase):
    res = ml_service.explain_hospitalization(patient)
    if not res: raise HTTPException(status_code=500, detail="Explanation failed")
    return ExplainResponse(**res)


def predict_comp(patient: PatientBase):
    return _handle_prediction(
        ml_service.predict_complication,
        patient,
        labels=["Низький ризик легеневих ускладнень", "Високий ризик легеневих ускладнень"]
    )


def explain_comp(patient: PatientBase):
    res = ml_service.explain_complication(patient)
    if not res: raise HTTPException(status_code=500, detail="Explanation failed")
    return ExplainResponse(**res)