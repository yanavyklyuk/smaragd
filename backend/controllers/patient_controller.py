from sqlalchemy.orm import Session
from fastapi import HTTPException
from backend.services import patient_service
from backend.models.patient import PatientBase

def read_patients(db: Session):
    return patient_service.get_all_patients(db)

def read_patient(patient_id: int, db: Session):
    patient = patient_service.get_patient_by_id(db, patient_id)
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

def add_patient(patient_data: PatientBase, db: Session):
    return patient_service.create_patient(db, patient_data)

def edit_patient(patient_id: int, patient_data: PatientBase, db: Session):
    updated_patient = patient_service.update_patient(db, patient_id, patient_data)
    if updated_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return updated_patient