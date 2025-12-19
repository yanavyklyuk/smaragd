import joblib
import pandas as pd
import shap
import numpy as np
from typing import Dict, Any
from pathlib import Path
from backend.models.patient import PatientBase

CURRENT_DIR = Path(__file__).resolve().parent
MODELS_DIR = CURRENT_DIR.parent / "ml_models"

HOSP_MODEL_PATH = MODELS_DIR / "model_hospitalisation.pkl"
BED_MODEL_PATH = MODELS_DIR / "model_complication.pkl"

COLUMN_MAPPING = {
    "full_name": "ПІБ",
    "phone": "Телефон",
    "age": "Вік ",
    "gender": "Стать",
    "bmi": "ІМТ",
    "vch_pl": "вч п+л",
    "nch_pl": "Нч п+л",
    "pT": "pT",
    "pN": "pN",
    "pM": "pM",
    "histology_type": "Тип гістології",
    "fvc": "фжел",
    "vc_in": "жел.вд",
    "fev1": "офв1",
    "ppo_fev1": "PPO офв1",
    "it_index": "ІТ",
    "sos_25_75": "сос25-75",
    "pef": "пос",
    "leukocytes": "Лейкоцити",
    "hemoglobin": "Гемоглобін",
    "fev1_fvc_ratio": "ОФВ1/ФЖЕЛ",
    "copd": "COPD",
    "tbc": "TBC",
    "chest_trauma": "Травма грудної клітки",
    "emphysema": "Емфізема, булли і т.д.",
    "hypertension": "Гіпертонія",
    "arrhythmia": "Аритмія",
    "ef": "ФВ",
    "ihd": "ІХС значима",
    "ecg_changes": "ЕКГ без клініки",
    "neurology": "Неврологія",
    "diabetes": "Діабет",
    "kidney_issues_creat": "Проблеми з нирками з креатиніном",
    "kidney_issues_norm": "Проблеми з нирками без порушень лабораторних показників",
    "gi_disease": "ШКТ захворювання",
    "vascular_disorders": "Судинні порушення",
    "other_diseases": "Інші хвороби",
    "second_cancer": "Другий рак",
    "pi": "ПІ",
    "fibrinogen": "фібриноген",
    "removed_ln_index": "Індекс видалених л/в",
    "extension": "Розширення - резекція перикарда, ребер, діафрагми, страв",
    "pulmon": "Пульмон",
    "free_segments": "Вільні сегменти",
    "total_quantity": "Загальна кількість",
    "min_vol": "хв"
}

class MLService:
    def __init__(self):
        self.hosp_artifact = {}
        self.comp_artifact = {}
        self._load_models()

    def _load_models(self):
        try:
            if HOSP_MODEL_PATH.exists():
                self.hosp_artifact = joblib.load(HOSP_MODEL_PATH)
                print(f"Hospitalization model loaded: {self.hosp_artifact.get('model_name')}")
            else:
                print(f"File not found: {HOSP_MODEL_PATH}")

            if BED_MODEL_PATH.exists():
                self.comp_artifact = joblib.load(BED_MODEL_PATH)
                print(f"Complication model loaded: {self.comp_artifact.get('model_name')}")
            else:
                print(f"File not found: {BED_MODEL_PATH}")

        except Exception as e:
            print(f"Error loading ML models: {e}")
            self.hosp_artifact = None
            self.comp_artifact = None

    def _prepare_data(self, patient_data: PatientBase, feature_list: list) -> pd.DataFrame:
        raw_data = patient_data.model_dump()

        mapped_data = {}
        for eng_key, value in raw_data.items():
            cyr_key = COLUMN_MAPPING.get(eng_key, eng_key)
            mapped_data[cyr_key] = value

        for feature in feature_list:
            if feature not in mapped_data:
                if feature in raw_data:
                    mapped_data[feature] = raw_data[feature]
                else:
                    mapped_data[feature] = 0
                    print(f"Warning: Missing value for '{feature}', filling with 0")

        try:
            df = pd.DataFrame([mapped_data])
            df_final = df[feature_list]
            return df_final
        except KeyError as e:
            print(f"Critical Error: Model expects column {e}, but mapping failed.")
            print(f"Available mapped columns: {list(mapped_data.keys())}")
            raise e

    def _predict_from_artifact(self, artifact: Dict[str, Any], patient_data: PatientBase):
        if not artifact or "pipeline" not in artifact:
            return None

        pipeline = artifact["pipeline"]
        threshold = artifact["threshold"]
        features = artifact["features"]

        df = self._prepare_data(patient_data, features)

        try:
            if hasattr(pipeline, "predict_proba"):
                probs = pipeline.predict_proba(df)
                probability = probs[0][1]
            else:
                pred = pipeline.predict(df)[0]
                probability = 1.0 if pred == 1 else 0.0
        except Exception as e:
            print(f"Prediction logic error: {e}")
            raise e

        pred_class = 1 if probability >= threshold else 0

        return int(pred_class), float(probability)

    def _explain_from_artifact(self, artifact: Dict[str, Any], patient_data: PatientBase):
        if not artifact or "pipeline" not in artifact:
            return None

        pipeline = artifact["pipeline"]
        features = artifact["features"]

        df = self._prepare_data(patient_data, features)

        model = pipeline.named_steps['classifier']
        preprocessor = pipeline.named_steps['preprocessor']

        transformed_data = preprocessor.transform(df)

        if hasattr(transformed_data, "toarray"):
            transformed_data = transformed_data.toarray()

        feature_names = []
        try:
            feature_names = list(preprocessor.get_feature_names_out())
        except Exception:
            try:
                feature_names = list(preprocessor.get_feature_names_out(features))
            except Exception:
                if transformed_data.shape[1] == len(features):
                    feature_names = features
                else:
                    feature_names = [f"feat_{i}" for i in range(transformed_data.shape[1])]

        clean_names = []
        for name in feature_names:
            name = str(name).replace("numerical__", "").replace("categorical__", "") \
                .replace("remainder__", "").replace("ord_encoder__", "")
            clean_names.append(name)
        feature_names = clean_names

        background = np.zeros((1, transformed_data.shape[1]))

        explainer = shap.LinearExplainer(model, background)
        shap_values = explainer.shap_values(transformed_data)

        vals = shap_values
        if isinstance(shap_values, list):
            vals = shap_values[1]

        if len(vals.shape) > 1:
            vals = vals[0]

        explanation_list = []

        limit = min(len(feature_names), len(vals))

        for i in range(limit):
            name = feature_names[i]
            value = vals[i]

            if abs(value) > 1e-9:
                explanation_list.append({
                    "feature": name,
                    "value": float(value)
                })

        explanation_list.sort(key=lambda x: abs(x["value"]), reverse=True)

        base_val = explainer.expected_value
        if isinstance(base_val, list) or isinstance(base_val, np.ndarray):
            base_val = base_val[1]

        return {
            "base_value": float(base_val),
            "contributions": explanation_list[:20]
        }

    def predict_hospitalization(self, patient: PatientBase):
        return self._predict_from_artifact(self.hosp_artifact, patient)

    def explain_hospitalization(self, patient: PatientBase):
        return self._explain_from_artifact(self.hosp_artifact, patient)

    def predict_complication(self, patient: PatientBase):
        return self._predict_from_artifact(self.comp_artifact, patient)

    def explain_complication(self, patient: PatientBase):
        return self._explain_from_artifact(self.comp_artifact, patient)


ml_service = MLService()