from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration des paramètres de l'application
class Settings(BaseModel):
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change_me")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    MODEL_PATH: str = os.getenv("MODEL_PATH")

settings = Settings()


