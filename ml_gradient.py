import joblib
from .config import settings


_model = None
_classes = None


def load_model():
    global _model, _classes
    if _model is None:
        _model = joblib.load(settings.MODEL_PATH)
        _classes = list(getattr(_model, "classes_", []))
    return _model, _classes


def predict_proba(payload: dict):
    model, classes = load_model()
    import pandas as pd
    X = pd.DataFrame([payload])
    if hasattr(model, "predict_proba"):
        proba = model.predict_proba(X)[0]
        y = model.predict(X)[0]
        return y, dict(zip(classes, map(float, proba)))
    else:
        y = model.predict(X)[0]
        return y, None