import os
import jwt
import bcrypt

from fastapi import Depends

from fastapi.security import OAuth2PasswordBearer    

from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from typing import Annotated
from .config import settings 

auth2_scheme = OAuth2PasswordBearer(tokenUrl="login") #слово в ковычках должно совпадать с путем 
                                                        #твоего эндпоинта логина.

def hash_password(plain_password: str) -> str:
    return bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(plain_password:str, hashed_password:str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

def create_jwt_token(data: dict):
    to_encode = data.copy()
    time_expire = datetime.now(timezone.utc) + timedelta(settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": time_expire}) # Добавляем время истечения в данные токена
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    # присутствие моего секретного ключа в токене пользователя подтверждает что:
        # 1) этот токен был выдан моим сервером/клиентом
        # 2) содержимое токена не было изменено после выдачи
        
def decode_token(token: Annotated[str, Depends(auth2_scheme)]):
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
    return payload.get('sub')


