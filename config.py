from pydantic import BaseModel
import os


class Settings(BaseModel):
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change_me")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
    DATABASE_URL: str = (
    f"postgresql+psycopg://{os.getenv('PGUSER','app')}:{os.getenv('PGPASSWORD','app')}@"
    f"{os.getenv('PGHOST','db')}:{os.getenv('PGPORT','5432')}/{os.getenv('PGDATABASE','obesity')}"
    )
    MODEL_PATH: str = os.getenv("MODEL_PATH", "/app/ml/model_artifacts/model.pkl")


settings = Settings()