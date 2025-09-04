from pydantic import BaseModel, EmailStr, Field
from typing import Dict, Any, Optional

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    full_name: str | None = None
    role: Optional[str] = "user"  # valeur par défaut 'user'

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    role: Optional[str] = None  # "user" ou "admin"
    password: Optional[str] = Field(None, min_length=8)

class UserInfo(BaseModel):
    id: str
    email: str
    full_name: str | None
    role: str
    created_at: str
    predictions_count: int


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


class AdminStats(BaseModel):
    total_users: int
    total_predictions: int
    predictions_by_class: Dict[str, int]
    recent_users: int  # derniers 7 jours