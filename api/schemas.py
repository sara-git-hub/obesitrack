from pydantic import BaseModel, EmailStr, Field
from typing import Dict, Any


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    full_name: str | None = None


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class PredictionRequest(BaseModel):
    Gender: str
    Age: float
    Height: float
    Weight: float
    family_history_with_overweight: str
    FAVC: str
    FCVC: float
    NCP: float
    CAEC: str
    SMOKE: str
    CH2O: float
    SCC: str
    FAF: float
    TUE: float
    CALC: str
    MTRANS: str


class PredictionResponse(BaseModel):
    predicted_class: str
    proba: Dict[str, float] | None = None
    id: str | None = None