from pydantic import BaseModel
from typing import List

class PredictionResponse(BaseModel):
    prediction: int
    probability: float
    message: str

class FeatureContribution(BaseModel):
    feature: str
    value: float

class ExplainResponse(BaseModel):
    base_value: float
    contributions: List[FeatureContribution]