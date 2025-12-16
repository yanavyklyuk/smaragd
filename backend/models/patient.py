from sqlalchemy import Column, Integer, String, Float
from backend.config import Base
from pydantic import BaseModel

class PatientModel(Base):
    __tablename__ = "patient"

    id = Column("index", Integer, primary_key=True, index=True)

    full_name = Column("ПІБ", String)
    phone = Column("Телефон", String)
    gender = Column("Стать", String)

    age = Column("Вік ", Integer)
    hemoglobin = Column("Гемоглобін", Integer)
    free_segments = Column("Вільні сегменти", Integer)
    total_quantity = Column("Загальна кількість", Integer)
    min_vol = Column("хв", Integer)

    bmi = Column("ІМТ", Float)
    fvc = Column("фжел", Float)
    vc_in = Column("жел.вд", Float)
    fev1 = Column("офв1", Float)
    ppo_fev1 = Column("PPO офв1", Float)
    it_index = Column("ІТ", Float)
    sos_25_75 = Column("сос25-75", Float)
    pef = Column("пос", Float)
    leukocytes = Column("Лейкоцити", Float)
    fev1_fvc_ratio = Column("ОФВ1/ФЖЕЛ", Float)
    pi = Column("ПІ", Float)
    fibrinogen = Column("фібриноген", Float)
    removed_ln_index = Column("Індекс видалених л/в", Float)

    vch_pl = Column("вч п+л", String)
    nch_pl = Column("Нч п+л", String)
    pT = Column("pT", String)
    pN = Column("pN", String)
    pM = Column("pM", String)
    histology_type = Column("Тип гістології", String)

    copd = Column("COPD", String)
    tbc = Column("TBC", String)
    chest_trauma = Column("Травма грудної клітки", String)
    emphysema = Column("Емфізема, булли і т.д.", String)
    hypertension = Column("Гіпертонія", String)
    arrhythmia = Column("Аритмія", String)
    ef = Column("ФВ", String)
    ihd = Column("ІХС значима", String)
    ecg_changes = Column("ЕКГ без клініки", String)
    neurology = Column("Неврологія", String)
    diabetes = Column("Діабет", String)
    kidney_issues_creat = Column("Проблеми з нирками з креатиніном", String)
    kidney_issues_norm = Column("Проблеми з нирками без порушень лабораторних показників", String)
    gi_disease = Column("ШКТ захворювання", String)
    vascular_disorders = Column("Судинні порушення", String)
    other_diseases = Column("Інші хвороби", String)
    second_cancer = Column("Другий рак", String)

    extension = Column("Розширення - резекція перикарда, ребер, діафрагми, страв", String)
    pulmon = Column("Пульмон", String)

class PatientBase(BaseModel):
    full_name: str
    phone: str
    age: int
    gender: str
    bmi: float
    vch_pl: str
    nch_pl: str
    pT: str
    pN: str
    pM: str
    histology_type: str
    fvc: float
    vc_in: float
    fev1: float
    ppo_fev1: float
    it_index: float
    sos_25_75: float
    pef: float
    leukocytes: float
    hemoglobin: int
    fev1_fvc_ratio: float
    copd: str
    tbc: str
    chest_trauma: str
    emphysema: str
    hypertension: str
    arrhythmia: str
    ef: str
    ihd: str
    ecg_changes: str
    neurology: str
    diabetes: str
    kidney_issues_creat: str
    kidney_issues_norm: str
    gi_disease: str
    vascular_disorders: str
    other_diseases: str
    second_cancer: str
    pi: float
    fibrinogen: float
    removed_ln_index: float
    extension: str
    pulmon: str
    free_segments: int
    total_quantity: int
    min_vol: int

class PatientResponse(PatientBase):
    id: int

    class Config:
        from_attributes = True