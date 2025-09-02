# api/ml/ml_gradient.py
import joblib
import pandas as pd
from typing import Dict, Tuple, Optional
from ..config import settings

_model = None
_label_map = None

# Mapping des classes (identique à train.py)
LABEL_MAP = {
    0: "Insufficient_Weight",
    1: "Normal_Weight", 
    2: "Overweight_Level_I",
    3: "Overweight_Level_II",
    4: "Obesity_Type_I",
    5: "Obesity_Type_II", 
    6: "Obesity_Type_III"
}

def load_model():
    """Charge le modèle ML en mémoire (singleton)"""
    global _model, _label_map
    if _model is None:
        try:
            _model = joblib.load(settings.MODEL_PATH)
            _label_map = LABEL_MAP
            print(f"Modèle chargé depuis : {settings.MODEL_PATH}")
        except Exception as e:
            print(f"Erreur chargement modèle : {e}")
            raise
    return _model, _label_map

def preprocess_input(data: dict) -> pd.DataFrame:
    """Préprocess les données d'entrée pour correspondre au format d'entraînement"""
    # Calculer l'IMC
    imc = data["Weight"] / (data["Height"] ** 2)
    
    # Créer le DataFrame avec les colonnes attendues par le modèle
    processed_data = {
        "IMC": imc,
        "Height": data["Height"],
        "Weight": data["Weight"],
        "FCVC": data["FCVC"]
    }
    
    return pd.DataFrame([processed_data])

def predict_obesity(payload: dict) -> Tuple[str, Optional[Dict[str, float]]]:
    """
    Prédit la classe d'obésité à partir des données utilisateur
    
    Args:
        payload: Dictionnaire avec les données utilisateur
    
    Returns:
        Tuple (classe_predite, probabilités)
    """
    try:
        model, label_map = load_model()
        
        # Préprocessing des données
        X = preprocess_input(payload)
        
        # Prédiction
        prediction = model.predict(X)[0]
        predicted_class = label_map.get(prediction, f"Unknown_{prediction}")
        
        # Probabilités si disponibles
        probabilities = None
        if hasattr(model, "predict_proba"):
            proba_array = model.predict_proba(X)[0]
            probabilities = {
                label_map.get(i, f"Class_{i}"): float(prob) 
                for i, prob in enumerate(proba_array)
            }
        
        return predicted_class, probabilities
        
    except Exception as e:
        print(f"Erreur prédiction : {e}")
        raise