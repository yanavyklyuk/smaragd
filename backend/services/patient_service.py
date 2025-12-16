from sqlalchemy.orm import Session
from backend.models.patient import PatientModel, PatientBase

def get_all_patients(db: Session):
    return db.query(PatientModel).all()

def get_patient_by_id(db: Session, patient_id: int):
    return db.query(PatientModel).filter(PatientModel.id == patient_id).first()

def create_patient(db: Session, patient_data: PatientBase):
    new_patient = PatientModel(**patient_data.model_dump())

    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    return new_patient

def update_patient(db: Session, patient_id: int, patient_data: PatientBase):
    patient = db.query(PatientModel).filter(PatientModel.id == patient_id).first()
    if patient:
        data_dict = patient_data.model_dump()
        for key, value in data_dict.items():
            setattr(patient, key, value)

        db.commit()
        db.refresh(patient)
    return patient

def delete_patient(db: Session, patient_id: int):
    patient = db.query(PatientModel).filter(PatientModel.id == patient_id).first()
    if patient:
        db.delete(patient)
        db.commit()
    return patient