from fastapi import APIRouter, HTTPException, Request

from app.db import database
from app.models import Register, LogIn
from app.security import hash_password, verify_password, create_jwt_token
from app.crud import create_user, update_last_login, get_user_by_email


router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
async def register(user: Register):
    hashed_password = hash_password(user.password)    
    await create_user(user.name, hashed_password, user.email, user.age)
    return {"message": "User created successfully"}
        
@router.post("/login")
async def login(user: LogIn, request: Request):
    db_user = await get_user_by_email(user.email)
    if not db_user or not verify_password(user.password, db_user['hashed_password']):
        raise HTTPException(status_code=401, detail="Invalid credentials")
        
    client_ip = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("user-agent", "unknown")
    await update_last_login(db_user['id'], client_ip, user_agent)
    
    token = create_jwt_token({"sub": db_user["email"], "user_id": db_user["id"]})
    
    return {"access_token": token, "token_type": "bearer", "user_id": db_user["id"], "email": db_user["id"]}  

  