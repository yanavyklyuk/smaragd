from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from backend.config import get_db
from backend.controllers import patient_controller
from backend.models.patient import PatientResponse, PatientBase

router = APIRouter(
    prefix="/patients",
    tags=["Patients"]
)

@router.get("/", response_model=List[PatientResponse])
def get_patients(db: Session = Depends(get_db)):
    return patient_controller.read_patients(db)

@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    return patient_controller.read_patient(patient_id, db)

@router.post("/", response_model=PatientResponse)
def create_patient(patient: PatientBase, db: Session = Depends(get_db)):
    return patient_controller.add_patient(patient, db)

@router.put("/{patient_id}", response_model=PatientResponse)
def update_patient(patient_id: int, patient: PatientBase, db: Session = Depends(get_db)):
    return patient_controller.edit_patient(patient_id, patient, db)