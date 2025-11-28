import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()                                                   

class Settings(BaseSettings):
    SECRET_KEY: str= os.getenv("SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    
    model_config = {"env_file": ".env"}
    
settings = Settings()