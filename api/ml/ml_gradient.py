import joblib
import pandas as pd
from typing import Dict, Tuple, Optional
from ..config import settings

_model = None
_label_map = {
    0: "Insufficient_Weight",
    1: "Normal_Weight",
    2: "Overweight_Level_I",
    3: "Overweight_Level_II",
    4: "Obesity_Type_I",
    5: "Obesity_Type_II",
    6: "Obesity_Type_III"
}

def load_model():
    global _model
    if _model is None:
        try:
            _model = joblib.load(settings.MODEL_PATH)
            print(f"Modèle chargé depuis : {settings.MODEL_PATH}")
        except Exception as e:
            print(f"Erreur chargement modèle : {e}")
            raise
    return _model

def preprocess_input(data: dict) -> pd.DataFrame:
    """Préprocess complet pour le modèle GradientBoosting"""
    df = pd.DataFrame([data])
    df["IMC"] = df["Weight"] / (df["Height"] ** 2)
    # Colonnes utilisées dans train.py
    return df[["IMC", "Height", "Weight", "FCVC"]]

def predict_obesity(payload: dict) -> Tuple[str, Optional[Dict[str, float]]]:
    model = load_model()
    X = preprocess_input(payload)
    pred = model.predict(X)[0]
    probabilities = None
    if hasattr(model, "predict_proba"):
        proba_array = model.predict_proba(X)[0]
        probabilities = { _label_map[i]: float(p) for i, p in enumerate(proba_array) }
    return _label_map[pred], probabilities
